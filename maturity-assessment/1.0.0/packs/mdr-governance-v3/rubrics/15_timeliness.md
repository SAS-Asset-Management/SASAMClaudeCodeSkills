# 15 — Timeliness

## Definition

The lag between the occurrence or observation of a defect and its availability in the MDR submission. Distinct from submission schedule adherence — timeliness measures how current the data is within the submitted files, not whether the file arrived on time.

## Evidence Types

- Record level capture date or observed date
- Submission date or extract date
- A computed or published lag between capture and submission
- Documented target lag for each data type
- Reporting on lag outliers or stale records

## Maturity Ratings

| Level | Rubric |
| --- | --- |
| 0 | No capture date is recorded and lag is unknown. |
| 1 | A capture date exists but is not used to monitor lag. |
| 2 | Lag is measured on some datasets and targets are not defined. |
| 3 | Capture to submission lag is measured on every MDR dataset against a defined target and stale records are flagged. |
| 4 | Lag trends are analysed, bottlenecks in the capture to submission pipeline are identified, and targets are tightened. |
| 5 | Near real time feeds serve critical defect types and lag becomes negligible for high criticality assets. |

## Scoring Notes

- Cross references 01_scheduleAdherence, which is submission timing, and 23_assessmentFrequency, which is physical inspection cadence.
- Key artefact types: capture frequency forecasts, submitted datasets, process maps of the capture to submission pipeline.
- On time submission of stale data still fails timeliness; test the capture dates inside the files, not just the file date.
