# Enterprise-brain hook (optional standards citation upgrade)

The suite bundles concise, clause-mapped standards in `standards-library/` so it cites
authoritatively **without** depending on the enterprise brain. This is the default.

When the enterprise brain's asset-management graph is wired (roadmap **Q1-0**: ISO 55001 /
IAM / GFMAM nodes added to the graph — today only ISO 27001 is graphified), the suite can
retrieve **live clause citations** instead of the bundled files:

- Service: `brain/retrieval.py` → `HybridGraphRAGRetriever` (in the `theEnsembles` repo).
- Contract: `schemas/brain.py` → `RetrievalQuery` / `RetrievalResult` / `Citation`
  (citations already carry an evidence tier, mirroring sorenAaberg's tiering).
- Architecture: `.planning/ENTERPRISE-BRAIN-STACK.md`.

**This is a hook, not a hard dependency.** Pattern: if the brain AM graph is available,
resolve a clause citation via `HybridGraphRAGRetriever`; otherwise fall back to the
`standards-library/*-mapping.md` file for the same clause. Build it so the document is fully
producible offline today, and gains live-graph citations when Q1-0 lands.
