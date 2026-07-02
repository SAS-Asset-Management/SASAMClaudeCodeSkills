# SASAMClaudeCodeSkills — Comprehensive Skills Review

**Date:** 02/07/2026 · **Reviewed against:** worktree at v1.20.1 (commit 1d1351a) · **Method:** six parallel review agents (one per plugin family) applying a shared rubric — efficiency (context economy), effectiveness (trigger quality, executable steps), accuracy (broken references, drift, script defects) — plus one agent surveying all git activity since 01/06/2026 for new skill candidates.

---

## 1. Critical fixes (do these first)

### 1.1 SECURITY — committed SSH password
`sas-content-hub/1.0.0/skills/email-gate/scripts/deployGate.py:29` hardcodes the Cortex4 SSH password in plaintext (`SERVER_PASS`), repeated six or more times in `references/server-deployment.md`. It is in git history. **Rotate the credential**, switch to SSH keys (already provisioned per the Tailscale setup) or an env var, and scrub the reference doc.

### 1.2 Registration breakers — skills that cannot fire or install
| Defect | Location | Effect |
| --- | --- | --- |
| Invalid YAML in frontmatter description | `analytics/1.0.0/skills/website-analytics/SKILL.md:3-15` | Description collapses to "Website Analytics Skill"; the entire GA4/Clarity/Grafana trigger list is invisible to the router. One edit (block scalar) fixes it. |
| Unquoted `#002244` truncates description | `nano-banana-2/1.1.0/skills/nano-banana-2/SKILL.md:3` | YAML comment marker cuts the registered description mid sentence at "deep navy". Quote the string. |
| `sas-am-docs` absent from root registry | `.claude-plugin/marketplace.json` | The flagship document hub is uninstallable and undiscoverable. Add `"source": "./sas-am-docs/1.0.0"`. |
| `handoff-proposal` absent from root registry | same | Uninstallable; it carries a stray in‑plugin marketplace.json the loader never reads. |
| `project-manager` absent from root registry | same | Same class. |
| sed double substitution | `register-commands.sh:45-47` | Every registered command file gets doubled, broken absolute reference paths (verified live in `~/.claude/commands/push-notifications.md`). Fix and re‑run registration. |

### 1.3 Broken workflows
- **/handoff recovery wedges** — `ensemble/.../handoff.sh:155-189` + SKILL.md:115-117: the documented remedy after a failed push ("just re‑run") is guaranteed to abort on the id collision scan because the failed run already committed the packet to local `queue`. Skip collision hits matching the pending local packet, or reset local `queue` first.
- **fmeca references all 404** — `fmeca/SKILL.md:34-41` points at `references/*` but all eight files sit flat beside SKILL.md in every deployed copy. Also: no plugin.json, no versioned dir, and it is registered twice (plugin + legacy `~/.claude/skills/fmeca`), doubling its 168 word description in every session.
- **amEngine not invocable** — `sas-am-docs/.../_engine-guide/ENGINE.md:4` pins the engine to `/home/cortext4/repos/sas-am-engine` (remote server only); all four sub‑skills use broken relative paths to `_engine-guide/` and `standards-library/`. None of the sas-am-docs pipeline can run as written on the consultant machine.
- **BEAM → project-manager handoff broken on paper** — `project-manager/.../SKILL.md:272-279` extracts fields that do not exist in `beam-state-template.json` (`findings`, `agreed_scope`, contract value/pricing, `buying_committee` vs actual `stakeholders`). The sales to delivery handoff pre‑populates almost nothing.
- **sas-presentation canvas contradiction** — SKILL.md:395 and presentation-types.md:733 say 1920×1080; the authoritative scaffold uses 1760×990 (SKILL.md:96 agrees). Decks built from the SKILL config render ~9% off scale.
- **sasxlsx / saspptx have no input spec** — both instruct the agent to author GridDocument / IntermediateDocument JSON but ship no schema or example for it, while forbidding reading the engine paths that document it. Add `grid-document.md` + example to sasxlsx; sync `block-catalog.md` + an example IDoc into saspptx.

### 1.4 Duplicate plugin registrations (nondeterministic triggering)
- `webflow-content-creator` standalone has **drifted badly** from the hub copy: still MCP based (contradicting the recorded "no heavy MCP" preference), names a nonexistent tool (`mcp__webflow__assets`), stale cms-schema. Hub copy is canonical. Retire or stub the standalone.
- `linkedin-post-generator` standalone is byte identical to the hub copy today — pure future drift risk plus a doubled 8,900 word trigger registration. Retire one.
- 11 per‑plugin `.claude-plugin/marketplace.json` files duplicate metadata nonstandardly and are already drifting (wrong GitHub org in two). Delete them; keep root registry + plugin.json only.

---

## 2. Efficiency — context economy

**Fat SKILL.md files (all loaded in full on every trigger):**

| Skill | Words | Target | Main shard candidates |
| --- | --- | --- | --- |
| b2b-research-agent | 9,785 | ~3,000 | Five output templates inlined AND duplicated in references/ (~2,600 words of pure duplication); kanban/session machinery duplicating beam-selling |
| linkedin-post-generator (×2 copies) | 8,921 | ~2,500 | 8 format specs, 20 hook library, 9 example posts, UTM spec → references loaded per format by the parallel subagents |
| sas-presentation | 8,405 | ~2,500 | 10 inline slide type HTML blocks, colour tokens (duplicating base-styles.css), typography, share mode essay, responsive/print CSS |
| beam-selling | 8,042 | ~4,000 | Stage evidence bar tables + gate enforcement → load at gate review time; replace per interaction full kanban HTML regeneration with an injection script |
| data-quality-analysis | 5,067 | ~1,500 | Seven dimension rubrics + 115 line inline Python → ship as a runnable script |
| webflow-content-creator (standalone) | 4,340 | retire | Stale duplicate |
| nano-banana-2 | 3,322 | ~1,700 | Curl plumbing, error templates → references/api-examples.md (already exists) |
| fmeca | 3,106 | ~1,600 | Workflow 5 (context extraction, ~1,500 words) → its own reference |
| email-gate | 2,450 | ~1,800 | Icon SVGs listed twice; template architecture prose |

**Orphaned reference files** (shard targets that already exist but are never cited — wire in or delete): beam-selling ×3 (stage-gate-checklist, engagement-tracker, kanban-board templates), b2b-research-agent ×4, project-manager ×4 (inception, discovery, risk register, gate review templates), linkedin-post-generator ×2, sas-presentation (`winston-prompts.md`, two logo PNGs contradicting the "CDN only" rule), sasdocx (`block-catalog.md` — the authoritative block list — plus qa.md, extraction.md), tender-assessment (output-schema.json, sample-output.json).

**Repeated boilerplate to factor into shared references:** ensemble family re‑explains the queue/main branch model in six skills and the review tier enum three times → one `_lib/WORKFLOW.md`; sasdocx family duplicates the ~45 line visual audit procedure in each SKILL.md despite each shipping `reference/visual-audit.md`.

**Deterministic work done by the model that should be scripts:** beam-selling full kanban HTML regeneration every interaction; portfolio dashboard data injection against a non placeholder `const` literal (use an explicit token).

**Models to copy:** sas-content-hub router (254 words), project-manager structure, sas-amp (2,061 words + 8,800 sharded), the ensemble `_lib` shared library, sasdocx's CI guarded shared prose.

---

## 3. Effectiveness — triggers and executable steps

- **Standardise script invocation on `${CLAUDE_PLUGIN_ROOT}`** everywhere. The ensemble family alone uses four conventions (`$SKILL_DIR`, `$CLAUDE_SKILL_DIR`, `<skill-dir>`, bare `bash status.sh`) — none exists. sasdocx family uses bare `python scripts/cli.py` which fails from any project cwd (also: use `python3`). tender-assessment's scraper path assumes cwd. nano-banana-2 hardcodes the source repo path with a wrong version baked in.
- **Descriptions needing trigger phrases:** tender-assessment (weakest — no "check for new tenders", "bid/no bid", "RFT"), tether, sync, collect (bodies contain the phrases; hoist into the description — that is all the router sees).
- **Disambiguation gaps:** sas-presentation vs revealjs (no boundary sentence — sasdocx's "for one‑off edits use the built in skill" pattern is the model); sas-content-hub router description competes with content-campaign verbatim; the three sasdocx siblings tie on "extract our brand" (differentiate by format).
- **Uninvocable instructions:** sas-am-docs `record_handoff` and the persona critique gates have no mechanism; loopBuilder's second substrate references the `Workflow` tool without gating on its presence.
- **Formula ambiguities:** beam-selling win probability is unclamped (can yield −5% or 110%) with contradictory modifier rules; b2b scope probabilities vs BEAM base rates precedence undefined; tender scoring has three divergent rubrics (SKILL, scoring-matrix.md, assess_tenders.py v2.0.0 with undocumented auto decline lists) — make the script canonical.

---

## 4. Accuracy — drift and script defects (selected)

- **Exit code tables wrong** in tether, submit, publish-presentation (document exit 2 for arg errors; `ens_die` exits 1). Anything scripting against them misclassifies failures. collect returns 0 on id not found despite claiming non zero.
- **Version chaos:** nano-banana-2 is simultaneously 1.1.0 (dir, registry), 1.3.0 (plugin.json), 1.0.0 (package.json). ensemble: dir 1.0.0, registry 1.2.0, plugin.json 1.3.0 ("Seven commands" — there are eight skills). sasdocx family at 0.10.0. sas-amp at 0.1.0. `/sasam-update` string equality comparison also cannot handle local ahead of remote — use `sort -V` and `curl -sf`.
- **ISO 55001 clause conflict:** sas-amp's mapping uses 2024 numbering; sas-am-docs' clause map uses 2014 numbering; both claim 2024. One shared canonical clause map.
- **webflowPublish.py:** random UUID as `fileHash` defeats Webflow asset dedup (every retry uploads a duplicate); `itemCount` populated from `lastUpdated`; `update_item` force flips drafts live; docs promise a retry that does not exist.
- **sasam-update apply flow:** backs up modified files then runs bare `git pull`, which aborts on exactly those files. Stash/checkout after backup.
- **analytics plugin self contradiction:** SKILL mandates querying cortext4 ("local copy frequently weeks stale") while all 7 commands and the agent hardcode the local Mac copy.
- **push-notifications:** live webhook written to per project cwd `.notifications/config.json` which other repos will not gitignore; SKILL still models the retired `outlook.office.com/webhook` URL shape its own setup guide supersedes.
- **data-quality-analysis:** four surfaces say the output is markdown; the skill body mandates HTML. Fix descriptions.
- **fmeca Workflow 5** saves generated context into the plugin's own directory — an update replaced cache and a manifest integrity failure. Save to `./fmeca-context/` in the project.
- **Dead code:** status_graph.py (205 lines, powers a flag that does not exist), tender scraper's unused fetch_page/CSRF paths + tracked `__pycache__`, generate-manifest.sh:56 dead count.
- **Stale metadata sweep (sas-presentation):** "17 types" is actually 18; standards v1.0.0 vs v2.0.0 in three places; `system` theme documented but unreachable; broken Phase 3 question renumbering.

---

## 5. Cross cutting recommendations

1. **Build the release skill (see idea #2 below) before fixing anything else** — half the accuracy findings (registry gaps, version triples, manifest drift, per plugin marketplace.json rot, marketplace clone sync) are symptoms of an 18 release/month manual process.
2. **One repo wide convention pass:** `${CLAUDE_PLUGIN_ROOT}` invocations, `python3`, single root registry, plugin.json as the only version truth, delete per plugin marketplace.json files.
3. **Sharding pass on the five fat skills** (b2b, linkedin, sas-presentation, beam-selling, data-quality-analysis) — roughly 25k words of always loaded context reduced to ~10k, and most of it already has orphaned reference files waiting.
4. **Contract tests for cross plugin interfaces:** BEAM state template vs project-manager extraction map vs b2b writes; nano-banana-2 calling convention across its three callers (`--aspect` flag vs prose vs API config — three conventions today).

---

## 6. New skill ideas from the past month's work (01/06 – 02/07/2026)

Evidence base: 14 active repos, ~140 commits. Strongest themes: content approval galleries rebuilt from scratch eight times, client report issuance chased by hand across six commits, engagement closeout done manually in five commits, 18 plugin releases each touching the same three files.

**Tier 1 — highest evidence density:**

1. **draft-review-gallery** — turn a folder of markdown drafts (+ generated heroes) into one branded HTML approval gallery. *Evidence:* eight near identical throwaway scripts in June (`~/buildMockups.py`, `~/buildSeries.py`, `~/buildEmmaMock.py`, `~/buildApprovedDraft.py`, `aiBuildProspects/_serve/buildGallery.py`, three hero gen wrappers). Slots between nano-banana-2 and webflow-content-creator. ~Half a day saved per content batch.
2. **sasam-release** — one command to cut a plugin release: semver bump, CHANGELOG scaffold, generate-manifest.sh, register-commands.sh, registry/version reconciliation check, commit, marketplace clone sync. *Evidence:* VERSION/CHANGELOG/manifest each touched 18 times this month; v1.20.1 existed solely to fix a manual manifest mistake; this review found the same drift class recurring in ensemble and nano-banana-2. Would mechanically prevent the largest defect class in this report.
3. **client-report-issuance** (report-document-control + print-pdf-qa combined) — single source of truth for version/status injected into chip, document control table, and footers; draft/final gating; a QA check failing on stale version strings; then the print PDF loop (pagination, shadow flattening, native vector logo inlining) with visual verification. *Evidence:* nine mdrAssessment2026 commits chasing exactly this, including a FINAL report nearly shipped with a "Draft v0.1" footer; the shadow lesson was relearned independently in sas-presentation v1.23.0.
4. **engagement-closeout** — the missing bookend to /init-engagement: confirm final deliverable issued, record the invoice milestone, execute retain/discard, archive to MinIO LFS, notify client, schedule the deletion checkpoint. *Evidence:* five manual closing commits in mdrAssessment2026 including an `.lfsconfig` bug; reduces client data retention compliance risk.

**Tier 2 — strong cases:**

5. **client-repo-guard** — initialise or retrofit a client repo safely: client data exclusion .gitignore as first commit (per `gitVersionControl.md`), then a pre push sweep for secrets and credentials. *Evidence:* three first commit .gitignore rituals in June, two credential scrub commits in planningTool — and this review found a live committed SSH password, proving the need.
6. **loop-ops** — operate running loops: health check state, reconcile parallel burst wave branches, refresh stale summaries, harvest LEARNINGS, close out COMPLETE loops. *Evidence:* three manual reconciliation commits in aiBuildProspects, self healing cron work in personalProgramManager. Complements loopBuilder (design) with operations.
7. **claude-sidecar** — scaffold a host sidecar exposing `claude -p` / Agent SDK over HTTP to dockerised apps: spend cap, queueing, nginx timeouts, compose wiring. *Evidence:* familyhub built exactly this across five commits; the pattern repeats in the ai‑build runner and the Ensemble MCP wrapper.
8. **watcher-scaffold** — generate a scheduled scrape → filter → dedupe → notify daemon (watchlist config, state for dedupe, Teams + desktop notify via push-notifications, cron/launchd install). *Evidence:* campingWatcher built from scratch in June; clientDatabase weekly scraper and tender-assessment are the same architecture.

**Tier 3 — worthwhile:**

9. **uat-script-generator** — generate a user facing UAT script (markdown + interactive HTML checklist) from an app's routes/features/tests. *Evidence:* hand authored for planningTool this month; every delivered web tool needs one at handover.
10. **offer-page-builder** — the branded prospect offer HTML page + served gallery index (extension to b2b-research-agent, which covers research but not the offer artefact). *Evidence:* five aiBuildProspects commits iterating the template by hand; 25 offer pages produced this month.
11. **artefact-portal-publish** — generalise publish-presentation: push any HTML artefact to the team content library with an auto maintained index. *Evidence:* teamMeeting minutes, aiBuildProspects `_serve/`, and the artefactSharing standard all solve this ad hoc. Partial overlap with existing skills — lower priority.

---

## Appendix — month's activity summary

| Repo | Commits | Theme |
| --- | --- | --- |
| familyhub | 57 | Family PWA: recipes with AI photo extraction via Claude sidecar, chores, theming |
| aiBuildProspects | 21 | Autonomous daily prospect research loop, branded offer pages over Tailscale |
| SASAMClaudeCodeSkills | 20 | Plugin marketplace: ensemble workflow, sas-am-docs, sasdocx family, loopBuilder — 18 releases |
| yarraTrams/mdrAssessment2026 | 16 | Client report v1.1→FINAL, PDF QA, invoice, retain/discard closeout |
| outlookMCP | 6 | Outlook CLI 2.0.0, Graph defect fixes, DMARC ingestion |
| personalProgramManager | 5 | Daily BEAM advance automation (cron + MCP wrapper + self heal) |
| yarraTrams/planningTool | 4 | Pipeline repair, test/lint gates, credential scrub, UAT script |
| Others | ~10 | Two new engagement repos, client work product repos, meeting minutes, Mainstream 2026 deck |

Uncommitted June work: campingWatcher daemon; seven hero image/mockup gallery scripts in `~`; clientDatabase weekly scraper output.
