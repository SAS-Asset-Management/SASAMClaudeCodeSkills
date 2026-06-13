---
name: publish-presentation
description: Publish a finished conference presentation (a sas-presentation reveal.js deck) to the SAS-AM presentations container so it goes live in the team.sas-am.com content library. Use when a consultant says "publish this deck", "publish this presentation", "put this deck on the portal", "publish to team.sas-am.com", "handoff:presentations", "handoff this deck", or has a built conference deck they want live alongside the existing catalogue (maximoLive2025, AMPEAK2024, …). Direct publish over Tailscale — no engagement repo, no fleet.
---

# /publish-presentation — put a finished conference deck live on team.sas-am.com

`/handoff` sends work **to** the fleet; `/submit` brings your engagement work **in**.
**`/publish-presentation` is different again** — it takes a *finished* conference deck
(the standalone HTML a `sas-presentation` build produces) and **publishes it directly**
into the SAS-AM **contentLibrary** container, so it appears in the `team.sas-am.com`
content library next to the existing decks. There is **no engagement repo and no
poller** — it POSTs the deck to the container's publish API over **Tailscale** (the
tailnet is the trust boundary, exactly like the data plane).

You do **not** need to be tethered to an engagement to run this.

## When to use it

- "publish this deck / presentation", "put this on the portal", "publish to team.sas-am.com",
  "handoff:presentations", "handoff this deck" — once a conference deck is built and you
  want it live/shareable.

## How to run it

1. **Find the deck.** Point at the built deck — a single `*.html`, or the deck folder
   (the script looks for `dist/index.html`, `index.html`, `presentation.html`, or a single
   `*.html`). If you just built it with `sas-presentation`, that's the file/folder.

2. **Interview the consultant** conversationally for the catalogue card — don't dump a form:
   - **Title** (`--name`) — how it should read in the library (e.g. "Edge Intelligence for Rail").
   - **Event / audience** (`--event`) — where it's being presented (e.g. "AMPEAK 2026").
   - **Summary** (`--summary`) — one sentence on what it covers.
   - **Tags** (`--tags`) — comma-separated themes (e.g. "edge-ai,rail,asset-management").
   - **Status** (`--status`) — `draft` (default) while in progress; `delivered` once presented.

3. **Confirm, then call the script** with what you gathered:

```bash
bash "$SKILL_DIR/publish_presentation.sh" --name "<deck title>" \
  --deck "<path to .html or deck dir>" \
  --event "<audience/event>" \
  --summary "<one sentence>" \
  --tags "a,b,c" \
  [--status draft|delivered]   # default draft
```

- Use `--dry-run` first to flatten + QA + show the target **without** publishing — good
  for showing the consultant the brand/QA findings before it goes live.
- `--endpoint <url>` overrides the publish endpoint (defaults to the baked tailnet URL,
  overridable via `presentations_endpoint` in `~/.ensemble/config.json`).

## What the script does (deterministic — don't reproduce by hand)

1. **Flattens** the deck to one self-contained HTML — inlines local CSS/JS/images/fonts as
   `data:` URIs (the publish API stores a single file). CDN/remote refs (reveal.js, fonts)
   stay remote. Anything it can't inline is reported (it would 404 on the portal).
2. **QA, warn-only** — checks Australian English (visible text), the SAS palette
   (`#002244`/`#69BE28`), the SAS-AM tagline, `<img>` alt text, slide count, and any
   surviving local refs. It **reports** issues but always **publishes anyway**.
3. **Pre-flight** the endpoint over Tailscale (clear "is Tailscale up?" error if not), and
   refuses if a deck with the same id already exists (the API can't overwrite).
4. **Publishes** — `POST /api/presentations/create` (multipart): saves
   `presentations/<id>/presentation.html`, writes a README, and adds a `content.json`
   catalogue entry. The deck is then live.

## After it runs

- Relay the **live tailnet URL** the script prints (verified reachable), and that the deck
  now appears in the **team.sas-am.com** content-library catalogue.
- If you published as `draft`, remind the consultant to re-run with `--status delivered`
  once it's been presented.

## Limits (known; tracked as roadmap flags)

- **One self-contained HTML per deck.** Decks with un-inlinable local media (e.g. a local
  `<video>`) publish without that asset — the QA step flags it. A bundle/zip upload is a
  logged follow-up.
- **No update-in-place.** Re-publishing the same title 409s; use a new `--name` (e.g. add a
  year/"v2"). An update route is a logged follow-up.

## Exit codes

- `0` — published (or, with `--dry-run`, validated). Prints the deck id on stdout.
- `1` — a flatten / reachability / publish error, or an id collision (relay the stderr message).
- `2` — bad/missing arguments (e.g. no `--name`).
