# Changelog

All notable changes to SASAMClaudeCodeSkills will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.37.0] - 2026-07-14

### Added
- **Microsoft 365 email tooling bundled into sasam-core (plugin 1.1.0 to 1.2.0).** The Outlook and M365 toolchain is now one harmonious plugin. The `microsoft365` hub (the `outlook` CLI reference plus the mandatory composition rules) and the new `emailVoice` sub skill join the existing `sendAndLog` under `sasam-core/skills`, so the three ship and version together.
  - **`microsoft365` skill** moved from a hand authored slash command into the plugin. It now carries two mandatory composition rules on top of the existing HTML and approval before send rules: **Always Arial** (every outbound body wrapped in an Arial container that matches the signature) and **Voice** (read `~/.outlook-cli/voiceProfile.md` before composing and match the user's writing voice).
  - **`emailVoice` skill (new)** samples roughly 100 of the user's sent messages via the `outlook` CLI, classifies their writing voice (register, openings, closings, rhythm, punctuation, idiom, tone by recipient) and captures it in `~/.outlook-cli/voiceProfile.md`, which the `microsoft365` hub reads before every draft. `sendAndLog` inherits the voice automatically because it drafts through the hub. The profile stays local and personal; only the mechanism ships. After writing the profile the skill drafts a sample email in the captured voice and calibrates it against the user's feedback, folding any corrections back into the profile (skill 1.0.0 to 1.1.0).

## [1.36.0] - 2026-07-12

### Changed
- **sas-presentation — resources showcase as hero + QR cards, and a nav-rail gutter (plugin 1.2.0 → 1.3.0).** Refinement lifting the updated reference deck's two changes, preserving everything from 1.35.0:
  - **Resources showcase = max TWO, both hero + QR cards (no text-list variant).** `references/resources-showcase.md` and the `SKILL.md` Phase 3b rule now cap the showcase at two resources on one slide, each rendered as a white card with the article hero image on top, the title below, and a navy QR code (encoding the article URL) overlapping the hero's bottom-right with a "Scan to read" label. The old 2–4 text-list/callout variant is removed. Added the QR-generation recipe (`qrencode -t SVG -m 2 --foreground=002244 --background=ffffff`, with a python `qrcode`/`segno` fallback and base64-embedding), the hero fetch-and-downscale recipe (`curl` + `sips -Z 760` + base64), and the exact card CSS (`.resrow`, `.rescard`, `.reshero`, `.resqr` absolute bottom-right overlap, `.restitle` with 214px right padding to clear the QR, `.resmeta`).
  - **Nav-rail gutter for wide content.** `references/nav-rail.md` and the `SKILL.md` structural rules now require edge-to-edge blocks (KPI rows, bar charts, column grids, resource card rows) to reserve a ~172px right gutter — `.kpis,.bars,.cols,.resrow{margin-right:172px}` — so wide content never crowds or slides under the right navigation rail.
  - Verified with a zero-dependency sample deck rendered at desktop (1280×720), phone (390×844), and as a headless-Chromium PDF: two hero + QR cards render with sharp navy QR codes, KPI row and card row clear the nav rail, and the PDF shows no grey boxes or shadows with furniture hidden. `base-styles.css` was not touched (its CRLF line endings preserved).

## [1.35.0] - 2026-07-12

### Added
- **sas-presentation — screen-share hardening, shipped logo, nav rail, PDF export, resources showcase (plugin 1.1.0 → 1.2.0).** Second augmentation lifting patterns from a finished reference deck, preserving the SAS brand and marcov-revealjs-standards v1.0.0. Five changes:
  - **Compression-safe typography (mandatory rule).** New explicit rule: no 300/light weights anywhere, base body weight 600, headings 800–900, labels/kickers 700–900, higher-contrast muted ink. Made real in `references/base-styles.css` (body → 600, all six `font-weight:300` → 600, light-mode `--text-muted` `#6b7280` → `#42566a`) and the font imports in `SKILL.md` + `references/scaffold-template.html` (dropped `wght@300`, added `900`). Typography table and colour-system muted value updated to match. Thin strokes and pale greys are the first casualties of Zoom/Teams 4:2:0 chroma subsampling; heavier type survives it.
  - **Ship the SAS logos with the skill.** New `references/assets/sasLogoPrimary.svg` (navy+green, for light slides) and `references/assets/sasLogoReversed.svg` (white+green, for dark slides), plus new `references/logos.md` carrying both base64 data-URI strings, usage guidance (navy on light, white on dark, never a text-only wordmark), and the `currentColor` self-recolour trick. The `Logo Assets` section now leads with the ship-with-deck path (offline safe, works in the zero-dependency deck) ahead of the CDN option.
  - **Subtle right-side navigation rail.** New `references/nav-rail.md`: a very subtle vertical progress rail — current section green + labelled, past filled + dimmed, upcoming faint hollow rings — showing where we are and where we are going. Light/dark aware, `aria-hidden`, hidden in PDF. New `Navigation Rail` subsection in `SKILL.md`.
  - **Headless-Chromium PDF export mode.** New `references/pdf-export.md`: the `chrome --headless --print-to-pdf` flow with `@page{size:1920px 1080px}` and the grey-box/shadow guardrails (`print-color-adjust:exact`, `box-shadow:none`, reveal all slides, un-fade stagger, force bar fills, panels to white-with-border never grey, hide nav rail/controls). Step 6 export section updated; the RENDER VERIFY GATE now includes a mandatory PDF check for grey boxes and shadow halos.
  - **Resources showcase.** New `references/resources-showcase.md` and a `Phase 3b` discovery step: search `sas-am.com/resources` (Webflow blog/case-study CMS via the Webflow MCP CMS tools, or WebFetch/WebSearch) for pages matching the deck's subject/sector, and showcase the 2–4 best as a "Further reading" slide or inline callouts (title + URL). Honesty rules: only cite pages whose URL resolves; never fabricate.
  - Verified with a zero-dependency sample deck exercising all five features, render-checked at desktop (1280×720) and phone (390×844) and as a headless-Chromium PDF — heavy type, correct logo variant per background, nav rail state, and a PDF with no grey boxes or shadows and furniture hidden. Existing Reveal.js generation path otherwise unchanged.

## [1.34.0] - 2026-07-12

### Added
- **sas-presentation — fixed 16:9 scaled stage, density modes, animation library, zero-dependency export (plugin 1.0.0 → 1.1.0).** Cross-pollinated proven techniques from the open-source `zarazhangrui/frontend-slides` skill into the SAS-AM deck skill, preserving the SAS brand and marcov-revealjs-standards v1.0.0 compliance throughout. Seven changes:
  - **Fixed stage + never-`display:none` rule.** New Structural Rules bullet plus a "Rendering Modes" subsection documenting the fixed-canvas guarantee (1760×990 under Reveal.js, 1920×1080 in zero-dependency mode): the whole canvas scales uniformly and letterboxes on narrow screens rather than reflowing slide content, and whole slides are switched only via `.active`/`.visible` (`visibility`/`opacity`/`pointer-events`), never `display:none`/`display:block` (which a later `display:flex` rule silently overrides, exposing every slide at once). The dual-theme image swap is explicitly exempted.
  - **Content-density modes (Phase 1b).** A new early discovery question — speaker-led (low density, default) versus reading-first (high density) — that governs type scale, slide count, words per slide, and layout density. The 10-word rule is clarified as a speaker-led rule; reading-first relaxes it for reports/dashboards/one-pagers while keeping the no-overflow / no-overlap / minimum-readable-size limits.
  - **Effect-to-feeling animation library.** New `references/animation-library.md`: a mood → animation table plus copy-ready, flat-design-safe snippets (entrance reveals, brand gradient mesh, navy grid, green focal halo via gradient not shadow, draw-on data motion, stat count-up) all rebranded to navy `#002244` / lime `#69BE28`, with a reduced-motion block. Pointer added from the Animation Features section.
  - **Anti-generic ("AI slop") quality directives.** New "Distinctive by Default" subsection under Presentation Philosophy: commit to the brand palette, atmosphere over dead fills (flat-safe), vary slide types, hold one feeling, earn every element, real over stock, no typography drift.
  - **Zero-dependency single-file export mode.** New `references/rendering-modes.md` with a full self-contained scaffold (fixed-stage CSS, vanilla stage scaler + slide switcher, print block) for offline / air-gapped / CDN-blocked delivery. Offered, not defaulted; Reveal.js remains the default.
  - **Extended RENDER VERIFY GATE.** Now mandates capture at two viewports (desktop 1280×720 and phone ~390×844) and an explicit panel-overlap check (pixel inspection, since `scrollHeight` alone misses overlapping absolute/grid panels). Declared mode-agnostic.
  - **Sharded SKILL.md (progressive disclosure).** Moved the ten inline slide-type HTML recipes to new `references/slide-recipes.md` (all content preserved verbatim), replacing them in `SKILL.md` with a compact chooser table and pointer. `SKILL.md` reduced from 1,417 to ~1,200 lines while keeping the philosophy, discovery, rules, and selection guides inline.
  - Verified with a zero-dependency sample deck rendered at both viewports: uniform scaling, navy letterbox bars, no reflow, single active slide, correct brand colours. Existing Reveal.js generation path (`scaffold-template.html`, `base-styles.css`) left untouched.

## [1.33.0] - 2026-07-11

### Added
- **sas-content-hub — trend-spotter sub-skill (front of funnel).** New sub-skill at `sas-content-hub/1.0.0/skills/trend-spotter/` that surfaces what is overperforming in the audience's feed right now and turns it into ready-to-use hooks for the existing pipeline. It sits ahead of `linkedin-post-generator` and `content-campaign` — it decides WHAT to say; they decide HOW. Method: for a set of creators/competitors or a topic, across LinkedIn (primary), X, YouTube and Reddit over a default 30 day window, it pulls recent posts, scores each against THAT creator's own median baseline (comments weighted above reactions), flags the outliers that beat the baseline by >= 2x or top decile (stricter on small samples), and reverse-engineers each outlier's hook trigger, format, topic and angle, then clusters recurring patterns across creators into a ranked trend report. Outputs a ranked report, reusable hook/format templates adapted to SAS-AM voice, and a handoff brief that feeds straight into `/linkedin-post-generator` (angle + hook only — the downstream interview still supplies the real story and numbers) or `/content-campaign` (trend becomes the campaign topic). Honest data-sourcing doctrine baked in: a reliable tier (SAS-AM website-analytics stack, the socialContentEngine `linkedin-post-analyser`, `WebSearch`/`WebFetch`, and `claude-in-chrome` logged-in reads) versus an aspirational/gated tier (native LinkedIn/YouTube/Reddit/X APIs — none connected as MCP today), a per-run `ToolSearch` MCP discovery step, per-metric confidence tags, and a hard no-fabricated-numbers rule. Uses Assetivity as the default competitor example (per `sas-seo`). Three progressive-disclosure references: `dataSources.md`, `outlierMethod.md`, `outputTemplates.md`.
- **sas-content-hub — router + manifest wiring.** Registered trend-spotter in the `sas-content-hub` router `SKILL.md` (new workflow-table row, Quick Start option E, description trigger phrases "spot trends", "what's working on LinkedIn", "find viral hooks", "competitor trend scan"). Bumped the `sas-content-hub` plugin 1.0.0 → 1.1.0 in both `plugin.json` and `marketplace.json` with new keywords (trends, trend-spotting, viral-hooks, competitor-scan) and an updated description.

## [1.32.0] - 2026-07-05

### Changed
- **sas-amp — IAM 10-box alignment.** Brought the `sas-amp` skill into line with the authoritative IAM Anatomy of Asset Management v4 (the 10-box / 10 capability model, July 2024), replacing the superseded v3 "6 Groups, 39 Subjects" framing. Changes span the skill's `SKILL.md`, three reference files and the shipped knowledge graph:
  - **Knowledge graph wiring** — the graph already carried all ten `iam_group*` capability nodes but only four (Strategy, Decision Making, Life Cycle Delivery, Risk) had inbound edges. Added edges so the six orphaned boxes — Purpose & Context, Leadership & Governance, Organisation & People, Information Management, Review & Continual Improvement, and Value & Outcomes — are now reachable by the per-section graph queries, each anchored to the relevant section's seed clause (for example Purpose & Context → Clause 4.1, Information Management → Clause 7.6, Review & Continual Improvement → Clause 9.1, Value & Outcomes → Clause 6.2.3 and the Shamrock value dimensions node). All ten boxes are now reachable; JSON re-validated (`references/amp-knowledge-graph.json`, links 168 → 175).
  - **Model relabelled** — every "IAM Anatomy v4 (6 Groups, 39 Subjects)" / "IAM 39 Subjects Coverage" reference across `SKILL.md`, `graph-queries.md` and `amp-template-structure.md` now reads "IAM Anatomy v4 (10 Capabilities / 10-box model, July 2024)".
  - **New reference** — added `references/iam-10box-mapping.md`, the IAM counterpart to `iso55001-amp-mapping.md`: each of the ten boxes plus its sub subjects mapped to the AMP section(s) that cover it, with a line of sight column and box summaries. Registered in the `SKILL.md` reference list and backed by a new **IAM 10-box coverage matrix** cross cutting query (well covered / thin / missing per box, run at engagement start and before finalisation, mirroring the AMAF compliance matrix).
  - **Value & Outcomes close-out** — the Executive Summary and Section 9 content prompts now require an explicit outcomes statement naming the value the plan delivers against objectives, tied to the value dimensions node.
  - **Coverage gaps closed** — added Organisation, Culture & Competence content and an interview question (change readiness / competence); Resilience & Contingency Planning and Incident Management & Response bullets in the Risk section; a risk appetite line inherited from the SAMP; a Sustainability & ESG treatment in Future Demand seeded from the Strategy capability; Configuration Management in the information management bullets; and a note that Shutdown & Outage is sector conditional (required for water, transport and resources; not applicable to buildings or roads).
  - Existing content — the AMAF compliance matrix, GFMAM mapping, financial sustainability ratio, data confidence ratings and the adaptive interview — is retained unchanged.

## [1.31.0] - 2026-07-05

### Changed
- **sas-presentation — flat design, no box shadows.** SAS decks are flat. Set the `--shadow-sm/md/lg` variables to `none` across all three theme blocks (light, dark, share) in `references/base-styles.css`, so cards, tiles and containers no longer cast a box shadow by default. Added an explicit rule to `SKILL.md` Structural Rules ("never add a `box-shadow`; never redefine the shadow variables to a shadow value") and a pre delivery checklist item. Box shadows also degrade badly under Teams/Zoom chroma subsampling; separation now comes from borders and background contrast. (Rebased from unpushed local work.)

## [1.30.0] - 2026-07-05

Uprev from the usage remediation build (WP1/WP2/WP3/WP5), targeting artefacts reported done unseen, a broken download gate, and a missing send and log workflow. Rebased onto origin/main 1.29.0; supersedes the withdrawn 1.28.0 label from the first build attempt.

### Added
- **sas-presentation, htmlStandards, reportStandards — Render Verify Gate.** A mandatory, non optional Render Verify Gate requiring an actual screenshot or headless render check (logos, figures, plots, console errors all confirmed present) before any HTML or presentation deliverable can be reported done. A hard base64 data URI only rule for embedded images was added to `htmlStandards.md` and `reportStandards.md` (sas-presentation's CDN logo convention carved out as a documented exception). A hardened `@media print` block (`box-shadow: none !important`, `page-break-inside: avoid` on cards, figures and tables) extends the existing print styles to kill recurring PDF export shadow artefacts. The htmlStandards.md and reportStandards.md edits live in ~/.claude/standards (personal global config, outside this repo).
- **webflow-content-creator — post publish smoke test.** `~/.claude/hooks/deploy-smoke-test.sh` curls a URL and asserts an HTTP 2xx response plus a minimum byte count, printing a clear PASS or FAIL line. A new mandatory post publish smoke test step requires the agent to run this against both the published page URL and any gated download link after every publish, reporting the PASS or FAIL line verbatim rather than a bare "published". Targets the download gate twice serving 0 KB files while deploys were reported done unchecked.
- **sasam-core — sendAndLog skill.** New skill at `sasam-core/1.0.0/skills/sendAndLog/SKILL.md` that drafts an email, pushes it to Outlook drafts, and waits for explicit "sent" confirmation before logging the outcome against a BEAM opportunity, an Ensemble task, or the engagement hub. Hard rule up front: only ever pushes a draft, never calls send. Configurable per recipient routing rule list.

### Operational (no repo changes)
- **Server automations (WP5).** Scheduled jobs installed directly on cortext4 (outside this repo): a LinkedIn performance export ingest job and a read only weekly inbox hygiene report. The weekly gate DB lead digest was found already built and running in production since 21/03/2026 and left untouched. Out of office and departed contact detection remain documented TODOs pending a mailbox access and enrichment API budget decision.

## [1.29.0] - 2026-07-04

### Changed
- **maturity-assessment** 1.0.0 → 1.0.1 — optimisation pass driven by the simulated end to end engagement road test (NLR-MDR-SIM-2026, 04/07/2026) and the subsequent critique, executed as fourteen OPT items across four parallel work packages (engine, hooks, deliverable, documentation and doctrine). The pass hardens the scoring engine and ledger tooling against the friction the road test surfaced (hand seeded ledger appends, single evidence confidence interval display, compliance track gate coupling), trims the deliverable pipeline weight, tightens the config driven hook battery, and lands the documentation and doctrine corrections: OPT-02 root caused why the fourteen agents never registered as invocable subagent types and why two skill descriptions dropped in a live session — the plugin was never installed, so its `agents/` directory was never auto discovered (the `register-commands.sh` copies in `~/.claude/commands/` surface skills only and never agents, and the two "missing" descriptions traced to stale command copies since regenerated; both frontmatter blocks were verified valid) — remediated with an install step in the plugin README, an Availability and fallback section in `agents/README.md`, and a standard agent fallback guardrail in all eight skills (execute the agent instruction file inline and record it when the subagent type is unavailable); OPT-10 rewrote the qaRules.yaml recommendation concept to match the settled no owners doctrine (a recommendation names the capability or process it acts on, never a person or role as an accountable party); OPT-14 added rubric authoring guidance to `packs/README.md` (write level sentences that practice evidence such as interviews and observations can match, not only document evidence; substance over sentence blessed — score the substance, cite the nearest rubric sentence verbatim, record the mismatch as an epistemic note) with the matching guardrail added to the maturity-score skill; plus the recorded intake workaround for the machine wide camelCase mkdir guard (create pack directories via file writes or a full path `mkdir -p`).

## [1.28.0] - 2026-07-03

### Added
- **maturity-assessment** New plugin (1.0.0) — a framework agnostic maturity assessment suite that generalises the proven evidence based method (intake, parse, score, interview, reconcile, validate, compliance matrix, report) across any assessment framework. Three tier architecture: the plugin holds the method (eight skills, fourteen specialist agents, config driven hooks, a deterministic scoring engine with aggregation and CI maths, a dashboard plus PDF deliverable pipeline); framework packs hold each framework as data (rubrics, evidence types, question bank, optional calc pack, report spec, coverage manifest); the engagement repo holds `engagement.yaml` and all client evidence — the only place client evidence ever lives, with Claude API reasoning under zero data retention terms. This release ships the complete plugin: the scaffold (`.claude-plugin/plugin.json`, progressive disclosure `CLAUDE.md`, plugin `README.md`, `pytest.ini`, the three binding JSON Schemas plus the fictional worked example `engagementExample.yaml`), the eight method skills, the fourteen agents with the eight hook battery, the deterministic scoring engine (`aggregate.py`, `chunker.py`, `orchestrate.py`, `configLoader.py`) with its test suite, the deliverable pipeline (dashboard builder, PDF export, report gate, vendored Plotly, closed four plot catalogue), and the first framework pack `mdr-governance-v3` (25 rubrics across 5 domains, evidence types, question bank, stdlib only calc pack, report spec — the chunked MDR standard itself is generated locally per engagement and never shipped).

## [1.24.0] - 2026-07-03

Uprev from the 02/07/2026 comprehensive skills review (full findings in `test-reports/skillsOptimisationReview.md`).

### Fixed
- **website-analytics** — frontmatter description was invalid YAML (a scalar followed by column-0 list items), so the skill registered with the bare description "Website Analytics Skill" and its entire GA4/Clarity/Grafana trigger vocabulary was invisible to the router. Collapsed to a single flowing description.
- **nano-banana-2** — unquoted ` #002244` in the frontmatter description acted as a YAML comment marker, silently truncating the registered description mid-sentence at "deep navy". Description now quoted. Also reconciled the version triple: registry entry bumped 1.1.0 → 1.3.0 to match plugin.json, and package.json corrected from name "1.1.0" / version "1.0.0" to name "nano-banana-2" / version "1.3.0".
- **register-commands.sh** — the two chained sed expressions double-applied: the second re-matched `references/` inside the absolute path the first inserted, so every registered command file carried doubled, broken reference paths. Collapsed to a single expression; re-registered commands verified clean.
- **fmeca** — SKILL.md pointed at `references/*.md` but all seven reference files sat flat beside it, so every "read the reference" instruction 404'd. Files moved into a real `references/` directory and the plugin given its missing `.claude-plugin/plugin.json`.
- **sas-presentation** — slide canvas corrected to the authoritative 1760×990 (SKILL.md and presentation-types.md said 1920×1080 while the scaffold template and prose said 1760×990, producing ~9% off-scale decks); "17 presentation types" corrected to 18 (the table and reference define 18); standards version unified to marcov-revealjs-standards v1.0.0.
- **ensemble** — exit-code tables in tether/submit/publish-presentation documented an exit `2` for argument errors that `ens_die` never produces (it exits 1); sync SKILL.md said `--remote` defaults to `origin` when sync.py defaults to `ensemble`; tether referenced a nonexistent "packet" skill (renamed `/handoff`); full-width CJK parentheses in submit.sh's PR body fallback replaced with ASCII; stale `deploy/skills/...` path fixed in `_lib/README.md`.
- **sasam-update** — version comparison hardened: `curl -sf` (a 404 body no longer masquerades as a version), sentinel guard before comparing, and `sort -V` semantic comparison so a local copy ahead of remote is no longer reported as an available "update".
- **webflowPublish.py** (sas-content-hub) — `fileHash` now sends the real MD5 of the file instead of a random UUID (the UUID defeated Webflow asset dedup, so every retry uploaded a duplicate asset); collections listing populated `itemCount` from `lastUpdated`; removed a dead `upload_request` block left over from an earlier upload implementation.

### Added
- **Marketplace registry** — registered three plugins that existed in the repo but were absent from `.claude-plugin/marketplace.json` and therefore uninstallable: `sas-am-docs` 1.0.0, `handoff-proposal` 1.0.0, and `project-manager` 1.0.0. Bumped the `ensemble` entry 1.2.0 → 1.3.0 to match its plugin.json and corrected its description to eight commands including `/submit`.
- `.gitignore` — added `sasam-local-patches/` (the `/sasam-update` backup directory) so backups no longer pollute `git status`.

### Removed
- Ten per-plugin `.claude-plugin/marketplace.json` files (b2b-research-agent, beam-selling, data-quality-analysis, handoff-proposal, project-manager, push-notifications, sas-am-docs, sas-amp, sas-presentation, sasdocx). These duplicated plugin.json and the root registry in a location the marketplace loader never reads, and had already drifted. The root registry + each plugin.json are now the only metadata sources.

## [1.23.1] - 2026-07-02

### Security
- **email-gate** — removed the hardcoded Cortex4 SSH password from `scripts/deployGate.py` and `references/server-deployment.md` (it appeared in seven places across the two files). The script now defaults to SSH key auth (`BatchMode=yes`, so a missing key fails fast instead of prompting) with an optional `CORTEX4_SSH_PASS` env var fallback via `sshpass` for machines without provisioned keys. Manual command examples in the reference doc now use plain `ssh`/`scp`; prerequisite notes in the email-gate and content-campaign SKILL.md files updated to match. **The leaked credential remains in git history and must be rotated on the server.** Version numbered 1.23.1 to sit above the in-flight `sas-amp-10box-alignment` branch (1.23.0).

## [1.20.1] - 2026-06-16

### Fixed
- **generate-manifest.sh** now sources its file list from `git ls-files` (tracked files only) instead of walking the filesystem with `find`. The old approach swept untracked local cruft into the release manifest — `.notifications/config.json` (gitignored) and `sasam-local-patches/.../marketplace.json` (the `/sasam-update` backup dir) — producing phantom entries that fail integrity checks for any user who lacks those local dirs. The extension allow-list and path exclusions are preserved. Regenerated the manifest (232 → 230 real, tracked files).
- **marketplace.json** — the `sasam-core` registry entry still advertised `1.0.0` with the pre-loopBuilder description after the plugin bumped to `1.1.0` in 1.20.0. Updated version, description, keywords and tags to match `plugin.json`, so consumers discovering/installing the plugin see consistent metadata.

## [1.20.0] - 2026-06-16

### Added
- **sasam-core / `/loopBuilder`** New skill — designs a well-formed autonomous agent loop for a given subject, then launches it. Built on the Cherny "write loops, not prompts" / Karpathy "autonomy slider" framing: move up a level of abstraction from hand-prompting each step to specifying **outcomes plus verification** and letting the agent run the `context → decide → tool → result` cycle until a stop condition trips. The skill is **inspect-first** — it scans the working directory (repo shape, runnable test/build commands, available skills + tools, git state) and drafts a candidate loop against the five-part anatomy (**goal · context · action policy · verification · stop condition**) before asking the user anything, then confirms only the gaps. It **refuses to launch** without all four mandatory guardrails — explicit stop condition, iteration/budget cap, verification method, and a no-progress/drift detector — directly countering the dominant failure mode (expensive drift, infinite retries). The **design picks the substrate**: an in-session `/loop` for supervised single-prompt cycles, or a multi-agent `Workflow` for parallel fan-out/verify loops (no cron path — loops run now). A **pre-launch gate** renders the full design (approve / edit / cancel) before any autonomous work starts, and the skill pushes back honestly when a task isn't loop-shaped (no verifiable end-state, single-pass work, undefinable stop condition). `sasam-core/1.0.0/skills/loopBuilder/SKILL.md`. sasam-core plugin bumped `1.0.0 → 1.1.0`.

## [1.19.0] - 2026-06-16

### Added
- **ensemble — local-stdio MCP server.** New `ensemble/1.0.0/mcp/ensemble_mcp_server.py` (FastMCP, stdio; `+ requirements.txt + README.md`) gives a tethered consultant's Claude Code session first-class read+write `ensemble_*` tools over the Ensemble operational API — instead of every skill hand-rolling HTTP. It runs **locally** on the consultant's box and calls the Tailscale-only API; secrets (api_url/api_key/import_key/verify_tls) are read from `~/.ensemble/config.json` (the established per-user state file, mode 0600), **never** from the repo-shared `.mcp.json`. Tool catalogue spans approvals (list/transition), HMI tasks (list/assign/update), projects + gate decisions, opportunities + CRM, issue-flags, imports (beam-lead + proposal) and research (submit/list/results). HTTP errors are returned verbatim (a 422 invalid-transition or a 403 scope rejection is actionable, not silent). The server **complements** the git-queue → PR → tier-gate handoff (the audited deliverable path) — it never submits deliverables. Declared per-engagement via the template's `.mcp.json` (launched with `uv run --with mcp --with httpx`). Approvals/research/import-beam-lead tools work today (X-API-Key / X-Import-Key); the hmi/projects/crm/issue-flags tools are gated on theEnsembles' hardened-auth backend change (typed `Principal`/`get_principal` + default-deny route allowlist + per-engagement scoping), and `ensemble_import_proposal` awaits the backend `POST /import/proposal` route. Ensemble plugin bumped `1.2.0 → 1.3.0`.

### Changed
- **ensemble / `/init-engagement`** The placeholder-fill loop now also renders **`.claude/CLAUDE.md`** (the engagement working-agreement doc shipped by the template's new `.claude/` scaffold), so its `{{project_name}}`/`{{scope_tag}}`/`{{founder_handle}}`/`{{tailnet}}` tokens fill at init like the root `CLAUDE.md`/`.ensemble/project.json`/`.lfsconfig`. Without this a new engagement would render the working-guide with raw `{{…}}` placeholders.

## [1.18.0] - 2026-06-15

### Added
- **sasdocx (SASdocX)** New plugin — a SAS-AM on-brand document generator that learns a company's existing Word, PowerPoint or Excel template once into a reusable **Brand Profile**, then generates unlimited on-brand `.docx`/`.pptx`/`.xlsx` from it, with **off-brand output impossible by construction** (no generator writes a literal style name, hex colour or font — those live only in the profile, and `verify` refuses anything the template doesn't contain). Ships **three skills over one shared OOXML engine** — `/sasdocx` (Word), `/saspptx` (PowerPoint), `/sasxlsx` (Excel) — each exposing the same verbs `extract → comprehend (optional, model-driven) → verify → generate`, plus the learning verbs `learn`/`propose-overrides`/`refine`. The deterministic core runs fully offline (no model required); model-assisted verbs sit on top, fail-closed. Excel fills preserve formulas and brand number formats; Word/PowerPoint follow the template's real structural order, masters and layouts. Vendored at `sasdocx/0.10.0/` with the Python engine (`scripts/sasdockit/`, launched via `scripts/cli.py`), reference docs, synthetic example templates, and the full 936-test suite (verified green after rebrand). Requires Python ≥ 3.10 (`python-docx`, `python-pptx`, `openpyxl`, `lxml`, `Pillow`); optional LibreOffice + Poppler enable the visual QA gate (`python sasdocx/0.10.0/scripts/cli.py doctor`).

### Attribution
- **sasdocx** is a SAS-AM rebrand of the MIT-licensed [`brand-docs`](https://github.com/ferdinandobons/brand-docs) project by Ferdinando Bonsegna. Product names, command/skill identifiers (`sasdocx`/`saspptx`/`sasxlsx`), the engine package (`sasdockit`), env var (`SASDOCX_ROOT`) and user-facing text were renamed; the original MIT `LICENSE`, `NOTICE` and `CITATION.cff` are retained in full.

## [1.17.0] - 2026-06-13

### Added
- **ensemble / `/publish-presentation`** New consultant command — publishes a finished conference deck (a `sas-presentation` reveal.js build) straight to the SAS-AM **contentLibrary** container, so it goes live in the `team.sas-am.com` content library alongside the existing catalogue (maximoLive2025, AMPEAK2024, …). Unlike `/handoff` (work *for* the fleet) and `/submit` (engagement work *in*), this is a **direct publish** over Tailscale — no engagement repo, no GitHub control plane, no poller. It reuses the contentLibrary app's existing `POST /api/presentations/create` API (the tailnet is the trust boundary, like the data plane). The skill **flattens** the deck to a single self-contained HTML (inlines local CSS/JS/images/fonts as `data:` URIs; CDN/remote refs stay remote — the publish API stores one file), runs a **warn-only QA** pass (Australian English, SAS palette `#002244`/`#69BE28`, the SAS-AM tagline, `<img>` alt text, slide count, and any surviving local refs that would 404), pre-flights endpoint reachability, refuses on an id collision (the API can't overwrite), then POSTs the deck. Endpoint defaults to the baked tailnet URL (`cortex-t4.<tailnet>.ts.net:8081`), overridable via `presentations_endpoint` in `~/.ensemble/config.json`. Not engagement-scoped (no `/tether` required). `--dry-run` flattens + QAs without publishing. Verified end-to-end against the live container (publish → render → catalogue entry → cleanup). `publish-presentation/{SKILL.md,publish_presentation.sh,flatten_assets.py,presentation_qa.py}`; bash + python3 stdlib + `curl`. Ensemble plugin bumped `1.1.0 → 1.2.0`.

## [1.16.1] - 2026-06-13

### Fixed
- **ensemble / `/init-engagement`** Fixed a template-propagation race: `gh repo create --template` populates the new repo's scaffold **asynchronously**, so the immediate `git clone` could land an empty repo (no `CLAUDE.md`/`.ensemble/project.json`/`scripts/`), which then silently produced an unscaffolded, unprotected engagement. The skill now waits (polls the contents API) for a sentinel template file to appear before cloning, re-pulls if the working clone is still empty, and hard-fails with a re-run hint rather than proceeding without a scaffold. Verified end-to-end (repo created from template, scaffold filled, `queue`+protected `main` with the `tier-gate` check, registry row, tether).

## [1.16.0] - 2026-06-13

### Added
- **ensemble / `/init-engagement`** New consultant command — the onboarding step the protocol was missing. `/tether` and `/handoff` both assume the engagement already exists; when it doesn't, the consultant hit a dead-end (the v1.2 spec's founder-tier `init-project` was never built). `/init-engagement` stands a new engagement up end-to-end: creates `<owner>/sasam-<scope_tag>` from the `sasam-engagement-template`; fills the scaffold (root `CLAUDE.md` from `templates/CLAUDE.md.tmpl`, `.ensemble/project.json`, `.lfsconfig`) and pushes `main`; applies the two-branch model via the repo's `scripts/apply-branch-protection.sh` (the `queue` mailbox + protected `main` + the `tier-gate` required check + `tier:*` labels); registers `{uuid,name,scope_tag,repo,status:active}` in `sasam-registry`; and tethers the session so `/handoff` works immediately. Idempotent / re-runnable (every external mutation is create-if-not-exists); `--dry-run` previews with no changes; `--cleanup <scope_tag>` tears down a throwaway. Founder-run (needs org-admin `gh` + registry push). `init-engagement/{SKILL.md,init_engagement.sh,init_engagement_state.py}`; bash + python3 stdlib + `gh`/`git`. Ensemble plugin bumped `1.0.0 → 1.1.0`.

### Changed
- **ensemble** Dead-end abort messages are now actionable — `ens_require_tethered` (no `.ensemble/project.json`) and `/tether`'s no-match / empty-registry paths now point to `/init-engagement` to stand one up.

## [1.15.0] - 2026-06-13

### Added
- **handoff-proposal** New standalone plugin/skill — the proposal sibling of `import-beam-leads`. Hands an externally-authored proposal **into** the Ensemble opportunities pipeline (the reverse of the normal flow, where a proposal is an *output* of a stage-4 deal). A consultant points it at a finished proposal — a **PDF**, single-page **HTML**, or **structured JSON** (`proposal_sections` / `client_problem_map` / `timeline_weeks` / `case_study_references`) — for a company; the stdlib-only `handoff_proposal.py` base64s the artefact and POSTs to the Ensemble's `POST /api/import/proposal` intake over **Tailscale** (`ENSEMBLE_API_URL` + `ENSEMBLE_IMPORT_KEY`, sent as `X-Import-Key`). The intake finds-or-creates the opportunity by company, advances it to the BEAM **"Propose"** stage (never regressing a Commit/Deliver deal), and attaches the proposal as a `PENDING_APPROVAL` proposal — visible on the opportunity's **Proposals** rail and in the founder's approval queue, with the inbound handoff recorded as a radar-replay beam. Idempotent on company; `--dry-run` previews the body before sending. Pairs with theEnsembles `POST /api/import/proposal` (PR #142). `handoff-proposal/{SKILL.md,handoff_proposal.py}`; stdlib `urllib` only — no pip install.

## [1.14.1] - 2026-06-11

### Fixed
- **ensemble** Hardening from GitHub Copilot's PR review across `/tether`, `/submit`, and the onboarding deck. `/tether`: option parsing shifts by two only when a value is present (a trailing `--query`/`--mode`/`--dir` shows guidance instead of aborting), and `tether_state.py` usage lists the new `list` subcommand. `/submit`: `requested_by` never falls back to `git config user.name` (a name with spaces would make `tier-gate` unsatisfiable) — it requires a valid GitHub login; refuses a stale local `handoffs/outbox/<id>/`; errors when two artefacts share a filename; propagates `submit_state.py`'s own exit code; and fails loudly (no false "PR opened") when `gh pr create` fails; the summary uses its placeholder when evidence is empty. Onboarding deck: the display-only terminal no longer shows a copy cursor, and clipboard copy guards for a missing Clipboard API with an off-screen textarea fallback.

## [1.14.0] - 2026-06-11

### Added
- **ensemble / `/submit`** New consultant command to land work the consultant did **themselves** (offline, in a workshop) as a **reviewed deliverable**. Where `/handoff` queues work *for* the fleet, `/submit` brings finished work *in*: it interviews the consultant, matches the work to the engagement's **deliverables** ("Lars's delivery page" — reads `.ensemble/deliverables.json` when present, otherwise a free interview), and opens a **PR into `main`** carrying a self-contained result set under `handoffs/outbox/<id>/` — a schema-valid `packet.md` (so `tier-gate` reads the right review tier + requester), a human `summary.md`, a structured `submission.json` of the deliverable claims, and the artefact(s) (with a >10MB-non-LFS guard). Defaults to the `full` review tier (the submitter approves). `submit/{submit.sh,submit_state.py,SKILL.md}`; stdlib/bash + `gh`/`git` only.

## [1.13.1] - 2026-06-11

### Fixed
- **ensemble / `/tether`** Made the first tether seamless for a brand-new consultant — three first-run walls removed. **Registry auto-config:** `registry_repo` now defaults to the SAS-AM shared registry (`SAS-Asset-Management/sasam-registry`) and is persisted, so there's no manual `~/.ensemble/config.json` step. **No SSH keys:** the skill runs `gh auth setup-git` before cloning, so private engagement repos clone over HTTPS via the GitHub CLI credential helper — `gh auth login` (already in onboarding) is sufficient. **No-arg listing:** `/tether` with no engagement name (or `--list` / `*` / `all`) now lists the engagements you can tether to instead of erroring. **Auto-mode:** clone-vs-remote is auto-detected (remote if the cwd is a git repo, else clone) — the skill no longer asks. **Forgiving match:** engagement resolution is punctuation/spacing-insensitive with token-subset matching, so `transurban WCX NCX` resolves `Transurban WCX/NCX` / `transurban-wcx-ncx`.

## [1.13.0] - 2026-06-11

### Added
- **ensemble** New consultant workflow plugin packaging the five SAS-AM Ensemble engagement commands — **`/tether`** (bind the session to an engagement repo: clone/remote-add, fetch `main`+`queue`, orient), **`/handoff`** (write a task packet and fast-forward push it to the engagement's `queue` branch for the Norbert-poller to claim; results return as a PR into `main`), **`/sync`** (read-only catch-up: merged results to collect, PRs awaiting review, bounced packets, claims in flight), **`/collect`** (pull merged result sets from `main`, materialise + sha256-verify LFS deliverables, record what was collected), and **`/status`** (registry-wide view across every tethered engagement — open packets, claims with age, open PRs by review tier, last poll heartbeat). Ships a **SessionStart hook** (`hooks/hooks.json` → `skills/hooks/session-start-ensemble.sh`) that prints a hard-time-boxed, read-only `/sync` greeting only inside a tethered engagement repo and is otherwise silent. Bundles the shared `_lib` (stdlib-only bash + Python helpers for packet parsing, schema validation, repo resolution, and `~/.ensemble` state I/O), a reference copy of `schemas/packet.schema.json`, and the "0 → 100" reveal.js onboarding deck. Sourced from the `theEnsembles` monorepo (`deploy/skills/ensemble/`); stdlib/bash + `gh`/`git`/`git-lfs` only, no pip installs, Australian English throughout.

## [1.12.0] - 2026-06-10

### Added
- **sas-am-docs** New asset-management document suite — a composable hub that authors the full ISO 55001 document family (**SAMP, AMP, TMP, RCM**) over a shared, code-grounded analytics engine (`sas-am-engine`). Implements the strategic-to-tactical line of sight (SAMP → AMP → TMP, with RCM/FMECA feeding maintenance tactics) with sub-skills `sas-samp`, `sas-tmp`, `sas-rcm`, an engine guide (`_engine-guide/ENGINE.md`), an enterprise-brain citation hook, and a bundled standards library (ISO 55000 line-of-sight, ISO 55001 clause map, SAE JA1011 / IEC 60812 / ISO 14224 reliability map). Owned by `larsFrederickson`; every document's numbers are computed from real audit/financial data, not estimated. The engine re-derives the reference LHG dataset byte-identically and renders professional, paginated A4 HTML + PDF.

## [1.11.0] - 2026-06-09

### Changed
- **nano-banana-2** Restructured the brand prompt architect into a **router** with four mode sub-files. The earlier abstraction-based modes (Node Network, Structured Progression, Order from Chaos) are removed entirely — they produced glowy tech-icon clichés. Subjects are now always **stylised, simplified real objects**, never pure abstraction.
- **nano-banana-2** New brand frame copy: "clean, sophisticated, intentional — the look of a high-end consultancy report or quality editorial publication. Flat with crisp clean edges; no outer glow, no halo, no soft luminous bloom, no glassy or frosted texture, no glossy 3D render." Green appears only as a precise, deliberate accent — never as a glow, haze, gradient field, starburst, or background light.

### Added
- **nano-banana-2** Four mode sub-files in `modes/`:
  - **Mode 1 — Editorial Diagram** (`mode-1-editorial-diagram.md`): explaining a concept, process, or relationship. Default mode.
  - **Mode 2 — Technical Line** (`mode-2-technical-line.md`): FMECA, reliability, asset hierarchies, Maximo data structure, equipment teardowns.
  - **Mode 3 — Data as Hero** (`mode-3-data-as-hero.md`): maturity assessments, Weibull, fleet simulation, analytics results.
  - **Mode 4 — Architectural** (`mode-4-architectural.md`): sector positioning, infrastructure, "who we serve".
- **nano-banana-2** Each mode sub-file contains: when-to-use criteria, the prompt template with `[FIXED BRAND FRAME]` placeholder, slot definitions, and one fully assembled worked example.
- **nano-banana-2** Plugin version bumped to 1.3.0.
- **b2b-research-agent** Fit-to-services, scope options, and build-out (Phase 6): the skill now assesses fit against our SAS-AM service lines, targets Director-level and above decision-makers, pitches a range of 2–4 engagement scopes each with a win probability, and asks which scope to build out through interview (handing off to beam-selling).
- **b2b-research-agent** Site Locations: a new research step that finds the prospect's physical sites (head office + operational facilities) with addresses and approximate coordinates, surfaced as a Site Locations table in the dossier and **plotted on an interactive map** (Leaflet + OpenStreetMap, no API key) in the HTML report. The map self-removes when there are no plottable sites. Wired into `report-template.html` and `prospect-dossier-template.md`.

## [1.10.0] - 2026-05-19

### Added
- **nano-banana-2** SAS-AM Brand Prompt Architect — primary mode that assembles a single natural-language image prompt from a piece of written content (LinkedIn post, blog article, slide topic, Webflow page). Separates a FIXED brand frame (visual style, colour, lighting, negative instruction) from VARIABLE per-image content (subject metaphor, composition directive, aspect, open-space region).
- **nano-banana-2** Three composition modes selected automatically from the source subject:
  - **A — Node Network:** connectivity, ML, multi-agent, federated, data flow → luminous nodes joined by fine threads
  - **B — Structured Progression:** maturity assessments, frameworks, governance, roadmaps → layered geometric tiers
  - **C — Order from Chaos:** data quality, analytics, diagnostics, raw-to-insight → particles resolving into a crystalline lattice
- **nano-banana-2** Aspect ratio handled as plain language inside the prompt body (no CLI flags): default `a wide 16:9 landscape composition`, plus `a square 1:1` and `a tall 4:5 portrait`.
- **nano-banana-2** Three worked examples in SKILL.md covering all three modes (edge federated ML, Yarra Trams MR5 governance maturity, worthless-data-to-intelligent-assets).

### Changed
- **nano-banana-2** Frontmatter description updated so the skill triggers on requests to generate image prompts, social or blog or presentation imagery, or SAS-AM visuals from written content.
- **nano-banana-2** Hyper-realistic photographic enhancement is now opt-in only (`--photoreal` or explicit user request), not the default. SAS-AM imagery routes through the Brand Prompt Architect.
- **nano-banana-2** Plugin version bumped to 1.2.0 to reflect the new primary mode.

## [1.9.1] - 2026-04-15

### Changed
- **sas-presentation** Share mode now uses the same Reveal canvas (1760 by 990) and `.reveal` font size as light/dark — text size matches across all three modes. The earlier 1440 by 810 share canvas made share mode text noticeably larger than the other modes.

## [1.9.0] - 2026-04-15

### Added
- **sas-presentation** New `share` theme mode, designed to survive Microsoft Teams and Zoom screen share compression:
  - Codec friendly colour palette: off white background (`#fafbfc`), darkened accent green (`#4F9A1E`), solid (non alpha) text colours, doubled shadow opacity, 2px borders
  - Decorative low alpha elements disabled: binary rain background hidden, full bleed gradient overlays replaced with solid scrims, QR radial glow replaced with solid outline
  - Subpixel antialiasing disabled in share mode (4:2:0 chroma subsampling destroys it anyway)
  - Reveal canvas shrinks to 1440 by 810 in share mode so text scales larger on the receiver's screen
  - Theme toggle now cycles light → dark → share → light with dedicated broadcast icon
  - URL param `?mode=share` auto activates share mode and persists to localStorage
  - New SKILL.md section "Sharing over Microsoft Teams or Zoom" documents root causes of washout (chroma subsampling, bitrate adaptation, gamut conversion) and call side settings (Teams "Optimize for video clips" off, Zoom "Optimize for video" off)

### Changed
- **sas-presentation** Default Reveal slide canvas shrunk from 1920 by 1080 to 1760 by 990 — globally increases apparent text size by ~9 percent for better readability in all modes
- **sas-presentation** Base `.reveal` font size bumped from 24px to 28px, cascading to elements without explicit sizes

## [1.8.0] - 2026-04-13

### Changed
- **sas-presentation** Major refactor of presentation philosophy and slide guidance (v2.0.0 standards)
  - Added **Presentation Philosophy** preamble with 10 non-negotiable rules (one idea, rule of three, 10 word limit, no bullet lists, tease don't tell, unexpected opening, S→C→R arc, closing echoes opening, contributions final slide, dead laptop test)
  - Restructured default Presentation type from 7-section narrative to **Situation → Complication → Resolution** three-act arc
  - New footer nav labels: TITLE | SITUATION | COMPLICATION | EVIDENCE | DECISIONS | RECOMMENDATION
  - **Louder headings**: title slide h1 increased from 64px/300 to 96px/700 (bold, commanding)
  - **Louder nav bar**: footer nav items increased from 11px/600 to 13px/700 with stronger default colour and thicker active underline
  - Title slide h2 updated from 36px/400 to 40px/500
  - Google Fonts now loads weight 500 for subtitle typography

### Added
- **sas-presentation** 5 new slide types with full CSS and HTML templates:
  - **Question slide** (`.slide-question`) — provocative centred text, tease with slide, tell with voice
  - **Full bleed image slide** (`.slide-fullbleed`) — edge to edge image with optional gradient overlay
  - **Breather slide** (`.slide-breather`) — dark blank slide to pull focus back to speaker
  - **Stat / single number slide** (`.slide-stat`) — bold 160px number with context label
  - **Contributions slide** (`.slide-contributions`) — numbered list of what was accomplished, replaces "Thank You" close
- **sas-presentation** Reveal.js **Speaker Notes** fully integrated:
  - RevealNotes plugin loaded from CDN in scaffold template
  - Every scaffold slide includes `<aside class="notes">` with transition cues, timing, and recovery phrases
  - Speaker view opens with S key — shows current slide, next preview, notes, and timer
  - SKILL.md documents speaker notes structure (transition phrase, key stat, timing, recovery)
- **sas-presentation** Tighter discovery process with 5 new Phase 2 questions:
  - One sentence test (enforces single idea)
  - Rule of three (caps supporting points)
  - Hook question (feeds opening slide)
  - Sensory detail request (feeds storytelling)
  - The ask (feeds close/recommendation)
- **sas-presentation** Content writing guidelines expanded:
  - 10 word rule enforcement with counting methodology
  - Slide selection guide (maps intent to slide type)
  - "What NOT to put on a slide" table with banned items and alternatives
  - Word count audit step added to workflow
- **sas-presentation** Pre-delivery checklist expanded with presentation philosophy and speaker notes sections

## [1.7.0] - 2026-04-08

### Added
- **sas-presentation** Winston Prompts reference — 5 AI prompts faithfully sourced from Patrick Winston's MIT "How to Speak" framework
  - Prompt 1: Start Any Presentation Right (empowerment promise, cycling, fence building, verbal punctuation, 7 second rule)
  - Prompt 2: Eliminate Your Slide Crimes (laser pointer hell, tennis match effect, contributions final slide, blackboard advantage)
  - Prompt 3: Make Your Ideas Unforgettable (Star framework: Symbol, Slogan, Surprise, Salient idea, Story)
  - Prompt 4: Structure Any Talk That Persuades (VSN-C framework: Vision, Steps, News, Contributions with salute ending)
  - Prompt 5: Use Props and Stories to Teach Anything (empathetic mirroring, blackboard advantage, prop retention)
  - All principles verified against MIT OpenCourseWare source material and Winston's *Make It Clear*

## [1.6.0] - 2026-03-31

### Added
- **project-manager** New plugin — marcov.GATE project delivery framework (v1.0.0)
  - Stage-gated hybrid methodology: 5 phases (Inception, Discovery, Development, Delivery, Close) with evidence-gated advancement
  - GATE = Governed Advancement Through Evidence — extends marcov.BEAM from sales into delivery
  - `/project-manager` slash command with 9 subcommands (new, status, gate-review, dashboard, portfolio, report, update, close, list)
  - `portfolio-sweep` agent — discovers `.project-status.json` across all repos, generates master board
  - `sweepProjects.py` — Python script for repo scanning, validation, and aggregation
  - 4 interactive HTML dashboard templates (220KB total):
    - Portfolio kanban board with filters, stats, stale project alerts
    - Per-project 3-tab dashboard (progress, full dashboard, client report)
    - Client status report (print-ready, SAS-AM branded)
    - Gate review report with verdict banner, donut chart, evidence table
  - 7 reference templates: gate criteria (scaled by tier), inception, discovery, gate-review, closeout, risk register, PRINCE2 mapping
  - `.project-status.json` schema (marcov-gate-v1) for decentralised project state
  - BEAM auto-ingest: reads `.beam/` engagement data when creating new projects
  - Three scaling tiers: micro ($20K–$50K), standard ($50K–$200K), major ($200K–$2M)
  - PRINCE2 terminology overlay for Victorian Government compatibility
  - All visuals: light/dark mode, SAS-AM colour palette, WCAG 2.1 AA, print styles

## [1.5.0] - 2026-03-23

### Added
- **sas-amp** New plugin — Asset Management Plan development tool (v0.1.0)
  - Core skill with ISO 55001:2024 alignment, AMP template structure, adaptive interview methodology
  - `/sas-amp` slash command for starting AMP development sessions
  - `amp-researcher` agent — regulatory, benchmark, and organisational web research
  - `amp-data-analyst` agent — data cleaning, LCC/NPV analysis, chart generation (7 chart types)
  - `amp-asset-context-reviewer` agent (Opus) — per-section review through asset owner perspective
  - `amp-document-generator` agent — branded DOCX output via python-docx
  - `generateDocx.py` — SAS-AM branded document generation with cover page, ToC, tables
  - `generateCharts.py` — matplotlib charts + D3.js specs for dual HTML/DOCX output
  - `dataUtils.py` — data cleaning, profiling, renewal forecasting, quality assessment CLI
  - 4 reference files: ISO mapping, AMP template structure, data analysis patterns, interview methodology
  - Registered in marketplace.json

## [1.4.1] - 2026-03-23

### Fixed
- **b2b-research-agent** Score number text invisible on score cards — green text on green background from conflicting CSS rules
- **b2b-research-agent** Logos broken in dossier reports — replaced local asset paths with Webflow CDN URLs
- **b2b-research-agent** Added logo theme toggling CSS — correct logo shown per light/dark mode

## [1.4.0] - 2026-03-12

### Marketplace
- **Added** sas-content-hub to marketplace registry
- **Added** webflow-content-creator to marketplace registry
- **Added** analytics to marketplace registry
- **Added** fmeca to marketplace registry

## [1.3.0] - 2026-03-12

### Wiki & Documentation
- **Added** wiki pages for sas-content-hub, webflow-content-creator, website-analytics, fmeca
- **Updated** master wiki hub from 9 to 13 skills

### Server Deployment Automation
- **Added** `deployGate.py` — automates SCP, resources.json registration, container restart on cortext4
- **Added** `server-deployment.md` reference with full architecture and troubleshooting
- **Updated** email-gate SKILL.md with automated deployment step
- **Updated** content-campaign SKILL.md with Stage 2b for Cortex4 asset deployment

### New Plugins
- **Added** analytics plugin (website-analytics skill, analytics-advisor agent, 6 commands)
- **Added** webflow-content-creator plugin (standalone)
- **Added** fmeca skill (5 workflows, 4 sector taxonomies)

## [1.2.0] - 2026-03-09

### Wiki Documentation
- **Added** master wiki hub (`wiki.html`) with skill catalogue and navigation
- **Added** wiki page for sas-presentation skill
- **Added** wiki page for data-quality-analysis skill
- **Added** wiki page for b2b-research-agent skill
- **Added** wiki page for beam-selling skill
- **Added** wiki page for linkedin-post-generator skill
- **Added** wiki page for tender-assessment skill
- **Added** wiki page for push-notifications skill
- **Added** wiki page for nano-banana-2 skill
- **Added** wiki page for sasam-update (sasam-core) skill

## [1.1.0] - 2026-02-27

### nano-banana-2
- **Added** mandatory post-processing with SAS logo watermark
- **Added** `post-process.js` script for automated watermarking
- **Changed** config storage to global `~/.claude/skills/nano-banana-2/`
- **Changed** prominent warning section requiring post-processing
- **Fixed** watermark not being applied during generation

### Infrastructure
- **Added** VERSION file for marketplace versioning
- **Added** CHANGELOG.md for release tracking
- **Added** `/sasam-update` skill for update management
- **Added** File manifest for integrity tracking

## [1.0.0] - 2026-02-22

### Initial Release
- **Added** sas-presentation - Reveal.js presentations with SAS branding
- **Added** data-quality-analysis - ABS Data Quality Framework assessments
- **Added** b2b-research-agent - B2B prospect research and intelligence
- **Added** beam-selling - BEAM evidence-gated sales lifecycle
- **Added** linkedin-post-generator - LinkedIn content in SAS-AM voice
- **Added** tender-assessment - Victorian government tender scoring
- **Added** push-notifications - Teams webhook and desktop notifications
- **Added** nano-banana-2 - Google Gemini image generation
