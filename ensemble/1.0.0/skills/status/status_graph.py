#!/usr/bin/env python3
"""status_graph — render a tethered engagement repo's git + PR state as the project git tree.

Powers `/status --graph`. The graph IS the status view: every claim, draft, QA event, fix,
steering comment and gate merge is already a commit or PR event, so there is no new data
store — we derive the whole view from `git log` (+ `gh` for PR state) and render it to a
self-contained HTML page (the docs/mockups/ensemble-handoff/git-tree.html rendering, data
injected). Stdlib + git + gh only.

The graph-derivation core (classify / derive) is pure and unit-tested; collect/render are thin.

Usage:  status_graph.py <repo-dir> [--out <file.html>] [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# commit subject prefix → node type (mirrors the mockup's colour legend)
_RULES: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"^init:"), "norbert", "norbert"),
    (re.compile(r"^handoff:"), "human", "consultant"),
    (re.compile(r"^claim:"), "norbert", "norbert"),
    (re.compile(r"^merge:|^merge "), "gate", "gate"),
    (re.compile(r"^qa-report:.*FAIL|^qa:.*FAIL", re.I), "qafail", "bayes"),
    (re.compile(r"^qa-report:.*PASS|^qa:.*PASS|^qa:", re.I), "qapass", "bayes"),
    (re.compile(r"^result:|^report:|^fmeca:|^copy:|^render:|^draft:"), "agent", "agent"),
    (re.compile(r"^heartbeat:|^registry:"), "norbert", "norbert"),
]


def classify(subject: str, branch_kind: str) -> tuple[str, str]:
    """(node_type, default_author) for a commit subject. branch_kind ∈ {main, ensemble, draft}."""
    for pat, typ, who in _RULES:
        if pat.search(subject):
            return typ, who
    # fall back by lane: trunk commits are versions/gates, branch commits are agent work
    return ("agent", "agent") if branch_kind != "main" else ("norbert", "norbert")


def _lane_for(branch_kind: str, lane_index: dict[str, int]) -> int:
    if branch_kind == "main":
        return 0
    return lane_index.setdefault(branch_kind, 1 + (len(lane_index) % 2))


def derive(commits: list[dict], prs: dict[str, dict] | None = None) -> dict:
    """Pure: turn ordered commits (oldest-first) + a {branch: pr} map into graph nodes + health.

    Each commit dict: {hash, parents:[...], author, subject, branch_kind, branch}.
    Returns {nodes:[...], health:[...]} where each node matches the git-tree renderer schema
    (l, t, h, w, m, d, f).
    """
    prs = prs or {}
    nodes: list[dict] = []
    lane_index: dict[str, int] = {}
    for c in commits:
        bk = c.get("branch_kind", "main")
        typ, who = classify(c["subject"], bk)
        lane = _lane_for(bk, lane_index)
        node = {
            "l": lane,
            "t": typ,
            "h": c["hash"][:7],
            "w": c.get("author") or who,
            "m": c["subject"],
            "d": _detail(c, prs),
            "f": c.get("files", []),
        }
        nodes.append(node)
    return {"nodes": nodes, "health": _health(commits, prs)}


def _detail(c: dict, prs: dict[str, dict]) -> str:
    bk = c.get("branch", c.get("branch_kind", "main"))
    pr = prs.get(c.get("branch", ""))
    extra = f" · PR #{pr['number']} {pr['state']}" if pr else ""
    return f"{c['subject']} — on {bk}{extra}"


def _health(commits: list[dict], prs: dict[str, dict]) -> list[dict]:
    open_branches = {p["headRefName"] for p in prs.values() if p.get("state") == "OPEN"}
    qa_fail = sum(1 for c in commits if re.search(r"qa.*FAIL", c["subject"], re.I))
    qa_total = sum(1 for c in commits if re.search(r"qa", c["subject"], re.I))
    claims = [c for c in commits if c["subject"].startswith("claim:")]
    merged = [c for c in commits if c["subject"].lower().startswith("merge")]
    return [
        {"k": "Open branches", "v": str(len(open_branches))},
        {"k": "Claims", "v": str(len(claims))},
        {"k": "Gate merges", "v": str(len(merged))},
        {"k": "QA fail rate", "v": f"{qa_fail}/{qa_total}" if qa_total else "0/0"},
    ]


# ── collect (git + gh) ──────────────────────────────────────────────────────
def _git(repo: str, *args: str) -> str:
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True).stdout


def collect(repo: str) -> tuple[list[dict], dict[str, dict]]:
    """Read commits (oldest-first across all branches) + PR state (best-effort via gh)."""
    fmt = "%H%x1f%P%x1f%an%x1f%s%x1f%D"
    raw = _git(repo, "log", "--all", "--date-order", "--reverse", f"--pretty=format:{fmt}")
    commits: list[dict] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        h, parents, author, subject, refs = (line.split("\x1f") + ["", "", "", "", ""])[:5]
        branch = _branch_from_refs(refs)
        commits.append({
            "hash": h, "parents": parents.split(), "author": author, "subject": subject,
            "branch": branch, "branch_kind": _branch_kind(branch),
        })
    prs: dict[str, dict] = {}
    gh = subprocess.run(
        ["gh", "pr", "list", "--repo", repo, "--state", "all", "--json",
         "number,title,headRefName,state"],
        capture_output=True, text=True, cwd=repo,
    )
    if gh.returncode == 0 and gh.stdout.strip():
        try:
            for p in json.loads(gh.stdout):
                prs[p["headRefName"]] = p
        except json.JSONDecodeError:
            pass
    return commits, prs


def _branch_from_refs(refs: str) -> str:
    for r in (refs or "").split(", "):
        r = r.replace("HEAD -> ", "").strip()
        if r and not r.startswith("tag:") and r != "origin/HEAD":
            return r.replace("origin/", "")
    return "main"


def _branch_kind(branch: str) -> str:
    if branch.startswith("ensemble/"):
        return "ensemble"
    if branch.startswith("draft/"):
        return "draft"
    return "main"


# ── render ──────────────────────────────────────────────────────────────────
def render_html(graph: dict, project: str) -> str:
    """Self-contained HTML rendering of the derived graph (compact port of git-tree.html)."""
    data = json.dumps(graph["nodes"])
    health = json.dumps(graph["health"])
    return _HTML.replace("__PROJECT__", project).replace("__DATA__", data).replace("__HEALTH__", health)


_HTML = """<!DOCTYPE html><html lang="en-AU"><head><meta charset="UTF-8">
<title>Git tree — __PROJECT__</title><style>
:root{--bg:#0a0e14;--green:#19c37d;--cyan:#26d8e6;--blue:#7c9cff;--amber:#f0b429;--purple:#c084fc;--red:#ff5d6c;--dim:#6c7d92;--text:#cdd9e6}
body{background:var(--bg);color:var(--text);font-family:ui-monospace,monospace;margin:0;padding:24px}
h1{font-size:16px;letter-spacing:2px}h1 em{color:var(--green);font-style:normal}
.sub{color:var(--dim);font-size:11px;margin-bottom:14px}
.row{display:grid;grid-template-columns:1fr 280px;gap:16px}
.detail{border:1px solid rgba(120,200,220,.2);border-radius:6px;padding:12px;font-size:12px;min-height:120px}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px}
.stat{border:1px solid rgba(120,200,220,.2);border-radius:6px;padding:8px}
.stat .k{font-size:9px;color:var(--dim);text-transform:uppercase}.stat .v{font-size:16px;font-weight:700;color:var(--cyan)}
svg text{font-family:ui-monospace,monospace}.crow{cursor:pointer}
</style></head><body>
<h1>PROJECT <em>GIT TREE</em></h1><div class="sub">__PROJECT__ · /status --graph · the graph is the status view</div>
<div class="row"><svg id="g" width="100%"></svg>
<div><div class="detail" id="d">Click a node.</div><div class="stats" id="s"></div></div></div>
<script>
var C=__DATA__,HEALTH=__HEALTH__;
var LANE_X=[26,50,74],COL={norbert:'#c084fc',agent:'#26d8e6',human:'#7c9cff',qafail:'#ff5d6c',qapass:'#19c37d',gate:'#f0b429'},ROW=26,TOP=18;
var svg=document.getElementById('g'),H=TOP+C.length*ROW+12;svg.setAttribute('viewBox','0 0 520 '+H);svg.setAttribute('height',H);
function lx(l){return LANE_X[Math.min(l,2)]}function y(i){return TOP+i*ROW}
var p=[];for(var i=1;i<C.length;i++){var a=C[i-1],b=C[i];p.push('<line x1="'+lx(a.l)+'" y1="'+y(i-1)+'" x2="'+lx(b.l)+'" y2="'+y(i)+'" stroke="#3a4656" stroke-width="2"/>')}
C.forEach(function(c,i){var col=COL[c.t]||'#19c37d';p.push('<g class="crow" data-i="'+i+'"><rect x="4" y="'+(y(i)-ROW/2+2)+'" width="512" height="'+(ROW-4)+'" fill="transparent"/><circle cx="'+lx(c.l)+'" cy="'+y(i)+'" r="5" fill="'+col+'" fill-opacity=".25" stroke="'+col+'" stroke-width="1.6"/><text x="92" y="'+(y(i)+3)+'" font-size="10" fill="#cdd9e6">'+esc(c.m).slice(0,52)+'</text><text x="514" y="'+(y(i)+3)+'" text-anchor="end" font-size="9" fill="#6c7d92">'+c.h+'</text></g>')});
svg.innerHTML=p.join('');function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;')}
document.getElementById('s').innerHTML=HEALTH.map(function(h){return '<div class="stat"><div class="k">'+h.k+'</div><div class="v">'+h.v+'</div></div>'}).join('');
svg.addEventListener('click',function(e){var g=e.target.closest('.crow');if(!g)return;var c=C[+g.getAttribute('data-i')];document.getElementById('d').innerHTML='<b>'+c.h+' · '+c.w+'</b><br>'+esc(c.m)+'<br><span style="color:#6c7d92">'+esc(c.d)+'</span>'});
</script></body></html>"""


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--out", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    commits, prs = collect(args.repo)
    graph = derive(commits, prs)
    if args.json:
        print(json.dumps(graph, indent=2))
        return 0
    project = Path(args.repo).name
    out = Path(args.out or (Path(args.repo) / "git-tree.html"))
    out.write_text(render_html(graph, project), encoding="utf-8")
    print(f"git tree written: {out}  ({len(graph['nodes'])} events)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
