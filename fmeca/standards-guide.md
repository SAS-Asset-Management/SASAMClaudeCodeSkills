# Standards Guide — FMEA/FMECA

## Table of Contents

1. [IEC 60812](#iec60812)
2. [SAE J1739](#saej1739)
3. [MIL-STD-1629A](#milstd)
4. [ISO 14224](#iso14224)
5. [Standard Selection Guide](#selection)
6. [Cross-Reference Matrix](#crossref)

---

## 1. IEC 60812 — Analysis Techniques for System Reliability <a name="iec60812"></a>

### Overview
The primary international standard for FMEA/FMECA. Published by IEC, applicable across all
industries. Most recent edition: IEC 60812:2018.

### Key Characteristics
- Supports both FMEA (qualitative) and FMECA (with criticality)
- Flexible — does not mandate a specific scoring scale
- Defines the process, not a rigid template
- Applicable to hardware, software, processes, and services
- Emphasises the analysis process rather than prescriptive forms

### Process Steps per IEC 60812
1. Define the system and its boundaries
2. Define the ground rules and assumptions
3. Construct system block diagrams / functional models
4. Identify failure modes for each item
5. Determine failure effects (local, next higher level, end)
6. Identify failure detection methods
7. Identify compensating provisions
8. Determine severity classification
9. Estimate failure mode probability (if FMECA)
10. Calculate risk (RPN or criticality)
11. Document recommended actions
12. Report results

### Severity Classification (IEC 60812 reference categories)
The standard provides guidance categories rather than mandating a fixed scale:

| Category | Description |
|----------|-------------|
| Catastrophic | Death, system loss, severe environmental damage |
| Critical | Severe injury, major system damage, significant environmental impact |
| Marginal | Minor injury, minor system damage, minor environmental impact |
| Negligible | No injury, no significant system/environmental impact |

Note: Organisations typically expand these into 5-point or 10-point scales — see scoring-scales.md.

### When to Use IEC 60812
- Default choice for most industrial applications
- When no sector-specific standard is mandated
- When flexibility in approach is valued
- Multi-sector organisations wanting a common methodology

---

## 2. SAE J1739 — Potential Failure Mode and Effects Analysis <a name="saej1739"></a>

### Overview
Developed by SAE International for the automotive and transport sectors. Heavily used in AIAG
(Automotive Industry Action Group) environments. Current edition references align with the
AIAG-VDA FMEA Handbook (2019).

### Key Characteristics
- Distinguishes between DFMEA (Design) and PFMEA (Process)
- Uses the classic Severity × Occurrence × Detection = RPN model
- Mandates 1-10 scales for each factor
- Separates Prevention Controls from Detection Controls (a significant improvement over older FMEA
  formats that lumped them together)
- Introduces Action Priority (AP) as an alternative to RPN in newer AIAG-VDA alignment

### DFMEA vs PFMEA

**DFMEA (Design FMEA)**
- Analyses the product/component design
- Failure modes relate to design deficiencies
- Controls are design verification activities (testing, simulation, analysis)
- Done during design phase, before manufacturing

**PFMEA (Process FMEA)**
- Analyses the manufacturing/maintenance process
- Failure modes relate to process deficiencies
- Controls are process controls (inspections, error-proofing, SPC)
- Done before process implementation

### SAE J1739 / AIAG Scoring (1-10 scales)

**Severity**: Based on the effect on the customer/end user
- 10: Hazardous without warning (safety/regulatory non-compliance)
- 9: Hazardous with warning
- 8: Loss of primary function
- 7: Degraded primary function
- 6: Loss of comfort/convenience function
- 5: Degraded comfort/convenience function
- 4: Moderate annoyance to customer
- 3: Slight annoyance
- 2: Negligible effect, noticed by discriminating customer
- 1: No discernible effect

**Occurrence**: Based on predicted frequency
- 10: Very high — failure almost inevitable (≥1 in 2)
- 7-9: High — repeated failures
- 4-6: Moderate — occasional failures
- 2-3: Low — relatively few failures
- 1: Remote — failure unlikely (≤1 in 1,500,000)

**Detection**: Based on ability of current controls to detect before reaching customer
- 10: Almost impossible — no known control can detect
- 9: Very remote
- 7-8: Remote to low
- 4-6: Moderate — control may detect
- 2-3: High — control likely to detect
- 1: Almost certain — control will detect

### Action Priority (AP) — AIAG-VDA 2019 Alternative

Instead of multiplying S×O×D (which treats all combinations equally), the AP table categorises
combinations into three priority levels:

- **High (H)**: Action required — must implement action to reduce risk
- **Medium (M)**: Action recommended — should implement action
- **Low (L)**: Action optional — may implement action

AP tables are sector-specific and published in the AIAG-VDA FMEA Handbook.

### When to Use SAE J1739
- Rolling stock design reviews
- Automotive supply chain requirements
- When client or regulator mandates AIAG-VDA alignment
- When distinguishing prevention vs detection controls matters

---

## 3. MIL-STD-1629A — Procedures for Performing FMECA <a name="milstd"></a>

### Overview
US military standard, widely adopted in defence and aerospace. Although technically superseded
(cancelled 1998), it remains the reference standard for quantitative FMECA and is still widely
used and cited in defence contracts globally, including Australian Defence.

### Key Characteristics
- Two methods: Task 101 (Functional FMECA) and Task 102 (Damage/Piece-Part FMECA)
- Quantitative criticality assessment using failure rate data
- Severity classifications (Category I-IV)
- Worksheet-based format with specific required fields
- Formal criticality matrix (severity class vs criticality number)

### Task 101 — Functional FMECA
- Top-down approach starting from system functions
- Identifies functional failures and traces to hardware items
- Used in early design phases when detailed designs aren't available

### Task 102 — Hardware FMECA
- Bottom-up approach starting from piece parts or components
- Identifies how individual items can fail
- Used when design detail is available

### Severity Categories

| Category | Name | Description |
|----------|------|-------------|
| I | Catastrophic | Death, system loss |
| II | Critical | Severe injury, major damage, mission failure |
| III | Marginal | Minor injury, minor damage, mission degradation |
| IV | Minor | Less than minor injury/damage, mission completion with workaround |

### Quantitative Criticality Calculation

**Failure Mode Criticality Number (Cm):**
```
Cm = β × α × λp × t
```

Where:
- β = conditional probability of occurrence of next higher failure effect (0-1)
- α = failure mode ratio — fraction of total item failure rate attributable to this mode (0-1)
- λp = item failure rate (failures per million hours or per operating cycle)
- t = operating time or cycles in the mission/period

**Item Criticality Number (Cr):**
```
Cr = Σ (Cm) for all failure modes of the item within a severity category
```

### Criticality Matrix
Plot items on a matrix: Severity Category (I-IV) on one axis, Criticality Number (log scale) on
the other. Items in the upper-right quadrant (high severity, high criticality number) demand
priority action.

### When to Use MIL-STD-1629A
- Australian Defence procurement (CASG/DMO requirements)
- When quantitative criticality data is available or required
- Aerospace or defence contracts
- When the client specifically mandates MIL-STD-1629A

---

## 4. ISO 14224 — Collection and Exchange of Reliability and Maintenance Data <a name="iso14224"></a>

### Overview
Petroleum and natural gas industry standard for reliability data. Not an FMEA standard per se,
but provides the definitive taxonomy for equipment classification, failure modes, and failure
mechanisms that underpins many industrial FMEAs.

### Key Characteristics
- Defines a 9-level equipment taxonomy
- Standardised failure mode and failure mechanism lists per equipment class
- Standardised equipment boundary definitions (what's in/out of a "pump", "compressor", etc.)
- Failure data recording guidelines
- Widely adopted beyond petroleum — used in water, power, mining, ports

### Taxonomy Levels

```
1. Industry
2. Business category
3. Installation
4. Plant/unit
5. Section/system
6. Equipment unit (the "tag" level — pumps, compressors, valves, etc.)
7. Sub-unit (e.g. for a pump: driver, pump unit, power transmission, control/monitoring)
8. Maintainable item (e.g. bearings, seals, impeller, casing)
9. Part (not typically used in FMEA — too granular)
```

The critical levels for FMEA work are 6 (equipment unit), 7 (sub-unit), and 8 (maintainable item).

### Equipment Classes Covered
ISO 14224 provides detailed failure mode and mechanism tables for:
- Rotating equipment: pumps, compressors, turbines, generators, fans
- Static equipment: heat exchangers, pressure vessels, boilers, piping
- Electrical equipment: motors, transformers, switchgear, UPS, batteries
- Safety equipment: fire & gas detectors, ESD valves, pressure relief
- Mechanical handling: cranes, conveyors, winches
- Control and monitoring: transmitters, PLCs, control valves
- Subsea equipment (specific to offshore)

### How ISO 14224 Supports FMEA

Use ISO 14224 to:
1. Define equipment boundaries consistently
2. Source standardised failure mode lists as a starting point
3. Ensure failure mechanism categorisation is consistent
4. Align failure data recording with the FMEA (enables feedback loop)
5. Benchmark failure rates against published ISO 14224 data (e.g. OREDA)

### When to Use ISO 14224
- Oil & gas sector (often mandatory)
- When aligning FMEA with CMMS failure coding schemes
- When benchmarking against OREDA or similar databases
- When a consistent taxonomy is needed across diverse equipment types
- As a supplement to IEC 60812 for equipment-specific failure mode libraries

---

## 5. Standard Selection Guide <a name="selection"></a>

| Scenario | Recommended Standard | Rationale |
|----------|---------------------|-----------|
| General industrial FMEA | IEC 60812 | Broadest applicability, flexible |
| Rolling stock design review | SAE J1739 (DFMEA) | Transport sector alignment, prevention/detection split |
| Rolling stock maintenance strategy | IEC 60812 + ISO 14224 taxonomy | Operational focus with standardised failure modes |
| Defence procurement | MIL-STD-1629A | Typically contractually mandated |
| Oil & gas operations | IEC 60812 + ISO 14224 | ISO 14224 provides the taxonomy, IEC 60812 the process |
| Mining operations | IEC 60812 + ISO 14224 taxonomy | ISO 14224 equipment classes cover most mining equipment |
| Port infrastructure | IEC 60812 + ISO 14224 taxonomy | Blend of structural, mechanical, and electrical equipment |
| Process manufacturing | SAE J1739 (PFMEA) | Process-focused with manufacturing controls |
| Multiple standards required | IEC 60812 as base | Easiest to adapt columns to meet multiple requirements |

---

## 6. Cross-Reference Matrix <a name="crossref"></a>

| Concept | IEC 60812 | SAE J1739 | MIL-STD-1629A | ISO 14224 |
|---------|-----------|-----------|---------------|-----------|
| Failure mode | Failure mode | Potential failure mode | Failure mode | Failure mode |
| Failure cause | Failure cause | Potential cause | Failure cause | Failure mechanism |
| Local effect | Local effect | — | Local effect | — |
| System effect | Next higher effect | — | Next higher effect | — |
| End effect | End effect | Potential effect | End effect | — |
| Severity | Severity class | Severity (1-10) | Severity category (I-IV) | — |
| Occurrence | Probability | Occurrence (1-10) | Failure rate × mode ratio | Failure rate |
| Detection | Detection method | Detection (1-10) | Compensating provisions | Detection method |
| Risk metric | RPN or criticality | RPN or Action Priority | Criticality number (Cm) | — |
| Controls | Compensating provisions | Prevention + Detection controls | Compensating provisions | — |

This cross-reference is invaluable when translating between standards or when a client's existing
FMEA uses a mix of terminology.
