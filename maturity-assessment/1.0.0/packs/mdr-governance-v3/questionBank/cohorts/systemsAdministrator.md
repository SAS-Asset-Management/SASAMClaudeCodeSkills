# Cohort probes — systems administrator

Administers the asset management system, master data, and the interfaces that
feed submissions. Probes test the technical plumbing that the documented
process assumes.

## Probes

1. "Show me the interface mapping between the source systems and the MDR
   specification — who maintains it, and what happened at the last schema
   change?" — Subject: 02_dataFormatCompliance. Artefact type: interface
   mapping register. Typologies: procedural, recency.
2. "Where does reference data live, and how does a code change propagate to the
   field capture tools?" — Subject: 12_consistency. Artefact type: reference
   data dictionary. Typologies: procedural, contradiction.
3. "What automated checks run when assessment data lands in the system, and
   where do the failures go?" — Subject: 13_validity. Artefact type: validation
   rule configuration. Typologies: evidence, procedural.
4. "Can you produce the last assessed date per asset across the network, and
   who asks for that view?" — Subject: 24_dataCurrency. Artefact type: currency
   report or system extract. Typologies: evidence, coverage.
5. "Which datasets are extracted manually before submission, and what does the
   manual step change?" — Subjects: 02_dataFormatCompliance, 15_timeliness.
   Artefact type: extract procedure. Typologies: contradiction, evidence.
