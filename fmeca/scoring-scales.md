# Scoring Scales — FMEA/FMECA

## Table of Contents

1. [Severity Scales](#severity)
2. [Occurrence Scales](#occurrence)
3. [Detection Scales](#detection)
4. [RPN Thresholds](#rpn)
5. [MIL-STD-1629A Criticality](#milcrit)
6. [Risk Matrix (Qualitative)](#riskmatrix)
7. [Sector-Specific Adaptations](#sector)
8. [Scoring Consistency Rules](#consistency)

---

## 1. Severity Scales <a name="severity"></a>

### 10-Point Severity Scale (SAE J1739 / AIAG aligned)

This is the most widely used industrial severity scale. Adapt descriptions to the sector/asset.

| Score | Category | General Description | Key Indicator |
|-------|----------|-------------------|---------------|
| 10 | Hazardous — no warning | Failure causes harm without prior warning. Regulatory non-compliance. | Fatality, major environmental disaster |
| 9 | Hazardous — with warning | Failure causes harm with some warning. Regulatory non-compliance. | Serious injury, significant environmental harm |
| 8 | Very high | Total loss of primary function. Asset/system inoperable. | Complete service outage, total production loss |
| 7 | High | Significant degradation of primary function. Asset partially operable. | Major service disruption, major production loss |
| 6 | Moderate | Loss of comfort/secondary function. Primary function maintained. | Service quality degraded, minor production impact |
| 5 | Low-moderate | Degraded comfort/secondary function. | Customer inconvenience, minor quality issue |
| 4 | Low | Minor effect noticed by most users. | Noticeable but tolerable degradation |
| 3 | Very low | Minor effect noticed by some users. | Cosmetic defect, slight performance reduction |
| 2 | Negligible | Effect barely perceptible. | Perceptible only to discriminating observer |
| 1 | None | No discernible effect. | No operational impact |

### 5-Point Severity Scale (simplified — for organisations preferring coarser granularity)

| Score | Category | Description |
|-------|----------|-------------|
| 5 | Catastrophic | Fatality, permanent disability, major environmental damage, total system loss |
| 4 | Major | Serious injury, significant environmental impact, major system damage, extended outage |
| 3 | Moderate | Medical treatment injury, minor environmental impact, moderate damage, significant service disruption |
| 2 | Minor | First aid injury, negligible environmental impact, minor damage, brief service disruption |
| 1 | Insignificant | No injury, no environmental impact, negligible damage, no service impact |

---

## 2. Occurrence Scales <a name="occurrence"></a>

### 10-Point Occurrence Scale (SAE J1739 / AIAG aligned)

| Score | Category | Indicative Frequency | Probability per item per year |
|-------|----------|---------------------|-------------------------------|
| 10 | Almost certain | ≥1 in 2 | Continuous or daily |
| 9 | Very high | 1 in 3 | Multiple per month |
| 8 | High | 1 in 8 | Monthly |
| 7 | Moderately high | 1 in 20 | Every few months |
| 6 | Moderate | 1 in 80 | Annually |
| 5 | Low-moderate | 1 in 400 | Every few years |
| 4 | Low | 1 in 2,000 | Every 5-10 years |
| 3 | Very low | 1 in 15,000 | Very rarely |
| 2 | Remote | 1 in 150,000 | Extremely rare |
| 1 | Nearly impossible | ≤1 in 1,500,000 | Unheard of in this application |

**Guidance**: When historical failure data is available (e.g. from CMMS work orders), use actual
failure frequencies to calibrate. When data is unavailable, use engineering judgement and document
the basis. The frequency ranges above are indicative — tailor to fleet size and operating context.

For fleet operations (e.g. 80 trams): A failure that occurs once per year across the fleet is
different from once per year per tram. Always specify the basis: per item, per fleet, per
operating hour, or per cycle.

### 5-Point Occurrence Scale

| Score | Category | Description |
|-------|----------|-------------|
| 5 | Frequent | Likely to occur multiple times per year per asset |
| 4 | Probable | Likely to occur annually per asset |
| 3 | Occasional | Likely to occur over the asset lifecycle but not annually |
| 2 | Remote | Unlikely but possible over asset lifecycle |
| 1 | Improbable | So unlikely it can be assumed it will not occur |

---

## 3. Detection Scales <a name="detection"></a>

### 10-Point Detection Scale (SAE J1739 / AIAG aligned)

Detection assesses the ability of CURRENT controls (not proposed or ideal controls) to detect
the failure mode or its cause before the effect reaches the end user/system.

| Score | Category | Description | Example Controls |
|-------|----------|-------------|-----------------|
| 10 | Absolute uncertainty | No current control exists. No means of detection. | No inspection, no monitoring, no alarm |
| 9 | Very remote | Current controls almost certainly will not detect. | Infrequent visual inspection of hidden component |
| 8 | Remote | Current controls have poor chance of detection. | Annual inspection of gradually degrading item |
| 7 | Very low | Current controls have low detection capability. | Periodic manual measurement, no trending |
| 6 | Low | Current controls may detect. | Scheduled inspection at moderate frequency |
| 5 | Moderate | Current controls have moderate chance. | Periodic sampling/testing with analysis |
| 4 | Moderately high | Current controls have good chance. | Vibration monitoring with quarterly analysis |
| 3 | High | Current controls likely to detect. | Continuous monitoring with alarms (e.g. SCADA trip) |
| 2 | Very high | Current controls almost certain to detect. | Automated online monitoring with validated diagnostics |
| 1 | Almost certain | Current controls will detect. Failure mode cannot reach end user. | Proven fail-safe design with redundant detection |

**Critical rule**: Detection scores rate what EXISTS today, not what could exist. If a condition
monitoring system is planned but not yet installed, score based on current controls. The gap
between current and improved detection is the basis for improvement actions.

### 5-Point Detection Scale

| Score | Category | Description |
|-------|----------|-------------|
| 5 | Undetectable | No existing means to detect before failure/effect |
| 4 | Low detectability | Detection only by chance or specialist investigation |
| 3 | Moderate detectability | Detection possible through routine maintenance activities |
| 2 | High detectability | Detection likely through existing monitoring or inspection |
| 1 | Almost certain detection | Failure or precursor reliably detected by existing controls |

---

## 4. RPN Thresholds <a name="rpn"></a>

### 10-Point Scale RPN (range 1-1000)

There is no universal RPN threshold — organisations set their own. These are common defaults:

| RPN Range | Risk Level | Typical Action |
|-----------|-----------|----------------|
| ≥200 | High (Red) | Action required — reduce risk through design change, additional controls, or maintenance strategy |
| 100-199 | Medium-high (Orange) | Action recommended — review controls and consider improvements |
| 50-99 | Medium (Amber) | Monitor — ensure current controls are effective |
| <50 | Low (Green) | Acceptable — document and maintain current controls |

**Important**: RPN has well-known limitations. The same RPN can represent very different risk
profiles (e.g. S=10 × O=1 × D=2 = 20 vs S=2 × O=5 × D=2 = 20). Always consider severity
independently — any failure mode with Severity ≥ 9 warrants attention regardless of RPN.

### 5-Point Scale RPN (range 1-125)

| RPN Range | Risk Level | Action |
|-----------|-----------|--------|
| ≥60 | High (Red) | Action required |
| 30-59 | Medium (Amber) | Action recommended |
| <30 | Low (Green) | Acceptable |

### RPN Limitations and Alternatives

RPN is criticised because:
1. It's ordinal, not interval — the difference between RPN 100 and 200 isn't meaningful
2. Same RPN can mean very different risk levels (as shown above)
3. It over-emphasises detection relative to severity
4. Multiplying ordinal scales is mathematically questionable

Alternatives:
- **Action Priority (AP)**: SAE J1739 / AIAG-VDA lookup table (H/M/L) based on S, O, D combination
- **Risk matrix**: Plot severity vs occurrence (or severity vs likelihood) — simpler, widely understood
- **MIL-STD-1629A criticality number**: Quantitative, based on actual failure rate data
- **Cost-risk**: Multiply consequence cost by probability — gives dollar-denominated risk

When an organisation is choosing, recommend AP or risk matrix for operational FMEAs, and retain
RPN only where the client already uses it and doesn't want to change.

---

## 5. MIL-STD-1629A Criticality <a name="milcrit"></a>

### Criticality Number Calculation

**Failure Mode Criticality Number (Cm):**
```
Cm = β × α × λp × t
```

| Symbol | Name | Description | Source |
|--------|------|-------------|--------|
| β | Conditional probability | Probability that the failure effect results in the identified severity (0 to 1) | Engineering judgement or test data |
| α | Failure mode ratio | Fraction of total item failure rate due to this failure mode (0 to 1, Σα = 1 for all modes of an item) | Historical data, handbooks (e.g. NPRD, OREDA) |
| λp | Item failure rate | Total failure rate of the item (failures per 10⁶ hours) | Reliability databases, field data |
| t | Operating time | Duration of operation in the period under analysis (hours) | Mission profile or operating period |

**Item Criticality Number (Cr):**
Sum all Cm values for the item within a given severity category.

### Criticality Matrix Plotting

- X-axis: Item Criticality Number (Cr) — logarithmic scale
- Y-axis: Severity Category (I through IV, I at top)
- Plot each item as a point
- Items in upper-right quadrant (Cat I/II, high Cr) are highest priority

### Interpreting the Matrix

| Zone | Severity | Criticality | Action |
|------|----------|-------------|--------|
| Upper-right | Cat I-II | High Cr | Mandatory corrective action |
| Upper-left | Cat I-II | Low Cr | Review — severe but rare |
| Lower-right | Cat III-IV | High Cr | Review — frequent but manageable |
| Lower-left | Cat III-IV | Low Cr | Accept and monitor |

---

## 6. Risk Matrix (Qualitative) <a name="riskmatrix"></a>

For organisations preferring a simpler approach over RPN:

### 5×5 Risk Matrix

```
              Likelihood →
              Rare  Unlikely  Possible  Likely  Almost Certain
Severity ↓   (1)     (2)       (3)      (4)        (5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Catastrophic (5) │  M    H       H        E         E
Major        (4) │  L    M       H        H         E
Moderate     (3) │  L    M       M        H         H
Minor        (2) │  L    L       M        M         H
Insignificant(1) │  L    L       L        L         M
```

Where: E = Extreme (immediate action), H = High (priority action), M = Medium (action plan
required), L = Low (manage by routine procedures)

This format is familiar to most Australian organisations as it aligns with AS/NZS ISO 31000
risk management conventions.

---

## 7. Sector-Specific Adaptations <a name="sector"></a>

### Rolling Stock / Rail

Severity considerations specific to rail:
- Passenger safety weight highest (derailment, collision, fire, entrapment)
- Service reliability second (delays, cancellations affect public transport KPIs)
- Regulatory compliance (ONRSR in Australia, EN standards in Europe)
- Consider dwell time impacts (door failures delay entire network)
- Fleet availability — loss of one tram has different impact depending on fleet size and headroom

Occurrence calibration:
- Per vehicle vs per fleet — always specify
- Per kilometre may be more meaningful than per year for wear-related modes
- Consider duty cycle — a tram doing 200km/day vs 80km/day

### Ports & Marine

Severity considerations:
- Vessel delay costs ($25k-$100k+ per day depending on vessel class)
- Cargo damage or contamination
- Environmental (spills into harbour)
- Worker safety in heavy-lift operations
- Channel/berth availability

Occurrence calibration:
- Per operating hour (variable utilisation)
- Weather-exposed vs sheltered equipment
- Corrosion rates in marine environment
- Tidal and wave loading cycles

### Mining & Resources

Severity considerations:
- Production loss (tonnes per hour cost, often $10k-$500k+ per hour)
- Safety in remote/underground environments
- Environmental (tailings, dust, water contamination)
- Regulatory (mining inspectorate stop-work orders)
- Supply chain impact (single-point processing)

Occurrence calibration:
- Extreme operating conditions (dust, vibration, heat, impact loading)
- Continuous vs campaign operation
- OEM recommendations vs actual achieved intervals
- Haul road conditions, material hardness, abrasiveness

### General Industrial

Severity considerations:
- Product quality impact
- Downstream production stoppage
- Warranty/recall costs
- Regulatory compliance (WHS, EPA)
- Reputational damage

Occurrence calibration:
- Align with maintenance intervals where possible
- Consider seasonal variations
- Start-up/shutdown stress vs steady-state

---

## 8. Scoring Consistency Rules <a name="consistency"></a>

Apply these rules to ensure internal consistency within any FMEA/FMECA:

1. **Same severity for same end effect**: If two different failure modes produce the same end
   effect, they must have the same severity score.

2. **Severity based on worst credible case**: Not worst imaginable, not average — worst case
   that could credibly occur given the operating context and existing safeguards.

3. **Occurrence reflects current state**: If a PM task exists and is effective, occurrence
   reflects the managed failure rate, not the unmanaged rate. (The unmanaged rate matters for
   risk-based decision-making about PM changes, but the FMEA should reflect current reality.)

4. **Detection reflects current controls only**: Score what you have, not what you want. Planned
   improvements are captured as recommended actions, not as detection scores.

5. **Don't double-count controls**: If a single inspection covers multiple failure modes, each
   mode gets credit for that inspection — but don't count the same information twice (e.g.
   the inspection AND the resulting work order as two separate detection methods).

6. **Document assumptions**: When scoring is based on engineering judgement rather than data,
   state this explicitly. Use phrasing like "Based on engineering judgement — no historical
   failure data available for this mode in this application."

7. **Calibration workshop**: For large FMEAs with multiple contributors, score a set of
   reference failure modes first and use these as anchors to maintain consistency.
