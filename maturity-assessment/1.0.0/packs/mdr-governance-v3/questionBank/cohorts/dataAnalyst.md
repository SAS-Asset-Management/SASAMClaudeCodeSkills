# Cohort probes — data analyst

Hands on with the datasets that become MDR submissions. Probes test the data
quality dimensions against the pipeline as actually run.

## Probes

1. "Walk me through the last pre submission validation run — the script or
   checklist, the exceptions it raised, and what happened to them." — Subjects:
   13_validity, 02_dataFormatCompliance. Artefact type: validation routine or
   exception log. Typologies: procedural, evidence.
2. "What is the primary key for defect records, and how do you separate a
   duplicate from a legitimate recurrence?" — Subject: 11_uniqueness. Artefact
   type: deduplication rule documentation. Typologies: procedural,
   contradiction.
3. "For the most recent submission, how did the record count compare to the
   expected population, and who saw that comparison?" — Subject:
   10_completeness. Artefact type: completeness report. Typologies: evidence,
   coverage.
4. "Where do codes disagree between the asset management system and the field
   capture tool, and who owns the reconciliation?" — Subject: 12_consistency.
   Artefact type: reference data dictionary. Typologies: contradiction,
   procedural.
5. "What is the typical lag between a defect being observed and it appearing in
   a submission, and is that number reported anywhere?" — Subject:
   15_timeliness. Artefact type: lag analysis. Typologies: evidence, recency.
6. "Which quality caveats travel with the data to the receiving authority, and
   which stay inside the team?" — Subject: 14_uncertainty. Artefact type:
   dataset limitation statement. Typologies: evidence, contradiction.
