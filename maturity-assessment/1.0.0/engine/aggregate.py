"""Aggregation and confidence engine for the maturity assessment suite.

This module owns ALL score arithmetic. Skills and agents append evidence
records, sayScore, doScore, and disputes to scoreLedger.json; only this
engine writes final (score, confidence, ci), history, flag, and the runs
list. Nothing downstream recomputes scores from prose.

CLI:
    python3 aggregate.py --repo <engagementRoot> [--run-trigger "text"]

Method (fixed and documented so an auditor probing "how did you aggregate"
gets one reproducible answer):

* Per subject weighted mean over evidence records, weight = tagWeight x
  confWeight. tagWeight: Direct = directOverIndirect, Indirect = 1.0,
  tag None is excluded entirely. confWeight: High = highOverLow,
  Medium = 1.0, Low = 1 / highOverLow. Weights come from engagement
  framework.aggregationWeights, falling back to the pack defaultWeights.
* 95 percent confidence interval = mean plus or minus 1.96 x weighted
  standard error, clamped to [0, 5]. A single evidence record gives
  ci = [mean, mean].
* Rounding rule "from-0.7": final = floor(mean) unless the fractional part
  is STRICTLY GREATER than 0.7, in which case ceil. So a mean of 1.70
  rounds to 1 and a mean of 1.71 rounds to 2. The fractional part is
  rounded to nine decimal places before the comparison so binary float
  representation cannot flip the boundary.
* Final confidence is the weighted mean of evidence confidence mapped
  Low = 0, Medium = 1, High = 2: at least 1.5 gives High, at least 0.5
  gives Medium, otherwise Low.
* flag = "lowOutlier" when final < 2, "highOutlier" when final > 4,
  otherwise null.
* Run over run delta: when a subject's recomputed score or confidence
  differs from its last history entry, a history record is appended whose
  driver states the direction (lifts, holds, lowers) plus the trigger text.
* A runs entry is appended only when anything changed or --run-trigger was
  given.
* Every evidence record is validated before aggregation: tag must be one of
  None, Indirect, Direct; confidence one of Low, Medium, High; rubricLevel an
  integer within the pack scale bounds. Any violation aborts the run loudly,
  naming the subject and the record index — never silently skipped, never
  ingested.
* When a previously scored subject recomputes to no score (its weight
  bearing evidence withdrawn), a history entry "reverts to unscored after
  {trigger}" is appended so the history never contradicts the final block.

Subjects with no evidence keep final, confidence, and ci all null — the
engine never invents a score. The ledger is rewritten deterministically
(fixed key order, two space indent, trailing newline) and atomically (temp
file then os.replace), so identical inputs produce byte identical output.
"""

from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import math
import os
import sys
import tempfile

_ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))


def _loadConfigLoader():
    spec = importlib.util.spec_from_file_location(
        "maturityConfigLoader", os.path.join(_ENGINE_DIR, "configLoader.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_CONF_NUMERIC = {"Low": 0.0, "Medium": 1.0, "High": 2.0}
VALID_TAGS = ("None", "Indirect", "Direct")
VALID_CONFIDENCE = ("Low", "Medium", "High")
DEFAULT_TRIGGER = "aggregation run"


def validateEvidence(subjectId, evidence, scaleLow, scaleHigh):
    """Fail loudly on any malformed evidence record. The engine never silently
    skips or ingests an invalid tag, confidence, or out of bounds rubricLevel;
    the error names the subject and the record index."""
    for index, record in enumerate(evidence or []):
        tag = record.get("tag")
        if tag not in VALID_TAGS:
            raise ValueError(
                f"subject {subjectId} evidence record {index}: tag {tag!r} is not "
                f"one of {', '.join(VALID_TAGS)}"
            )
        confidence = record.get("confidence")
        if confidence not in VALID_CONFIDENCE:
            raise ValueError(
                f"subject {subjectId} evidence record {index}: confidence "
                f"{confidence!r} is not one of {', '.join(VALID_CONFIDENCE)}"
            )
        level = record.get("rubricLevel")
        if not isinstance(level, int) or isinstance(level, bool) or not (scaleLow <= level <= scaleHigh):
            raise ValueError(
                f"subject {subjectId} evidence record {index}: rubricLevel "
                f"{level!r} is not an integer between {scaleLow} and {scaleHigh}"
            )


def roundFrom07(mean):
    """Apply the from-0.7 rounding rule: floor unless the fractional part is
    strictly greater than 0.7 (1.70 rounds to 1, 1.71 rounds to 2)."""
    floor = math.floor(mean)
    frac = round(mean - floor, 9)
    if frac > 0.7:
        return int(math.ceil(mean))
    return int(floor)


def flagFor(score):
    """flag = lowOutlier below 2, highOutlier above 4, otherwise null."""
    if score is None:
        return None
    if score < 2:
        return "lowOutlier"
    if score > 4:
        return "highOutlier"
    return None


def resolveWeights(engagement, pack):
    framework = engagement.get("framework") or {}
    weights = framework.get("aggregationWeights") or pack.get("defaultWeights") or {}
    direct = weights.get("directOverIndirect")
    high = weights.get("highOverLow")
    if direct is None or high is None:
        raise ValueError(
            "Aggregation weights missing: set framework.aggregationWeights in "
            "engagement.yaml or defaultWeights in pack.yaml (directOverIndirect, highOverLow)."
        )
    return float(direct), float(high)


def _recordWeight(record, directOverIndirect, highOverLow):
    tag = record.get("tag")
    if tag == "Direct":
        tagWeight = directOverIndirect
    elif tag == "Indirect":
        tagWeight = 1.0
    else:
        return None  # tag None (or unknown) carries no scoring weight
    confidence = record.get("confidence")
    if confidence == "High":
        confWeight = highOverLow
    elif confidence == "Medium":
        confWeight = 1.0
    elif confidence == "Low":
        confWeight = 1.0 / highOverLow
    else:
        return None
    return tagWeight * confWeight


def computeSubject(evidence, directOverIndirect, highOverLow):
    """Compute (score, confidence, ci) from a subject's evidence records.

    Returns None when no record carries scoring weight, so the caller leaves
    the final block null rather than inventing a score.
    """
    weighted = []
    for record in evidence or []:
        weight = _recordWeight(record, directOverIndirect, highOverLow)
        if weight is None:
            continue
        level = record.get("rubricLevel")
        if level is None:
            continue
        weighted.append((float(weight), float(level), record.get("confidence")))
    if not weighted:
        return None

    totalWeight = sum(w for w, _, _ in weighted)
    mean = sum(w * x for w, x, _ in weighted) / totalWeight

    if len(weighted) == 1:
        ci = [round(mean, 4), round(mean, 4)]
    else:
        variance = sum(w * (x - mean) ** 2 for w, x, _ in weighted) / totalWeight
        effectiveN = totalWeight ** 2 / sum(w ** 2 for w, _, _ in weighted)
        standardError = math.sqrt(variance / effectiveN)
        halfWidth = 1.96 * standardError
        ci = [
            round(max(0.0, mean - halfWidth), 4),
            round(min(5.0, mean + halfWidth), 4),
        ]

    confMean = sum(w * _CONF_NUMERIC[c] for w, _, c in weighted) / totalWeight
    if confMean >= 1.5:
        confidence = "High"
    elif confMean >= 0.5:
        confidence = "Medium"
    else:
        confidence = "Low"

    return roundFrom07(mean), confidence, ci


def _taxonomySubjects(pack):
    subjects = []
    for domain in (pack.get("taxonomy") or {}).get("domains") or []:
        subjects.extend(domain.get("subjects") or [])
    return subjects


def _emptySubject():
    return {
        "final": {"score": None, "confidence": None, "ci": None},
        "sayScore": None,
        "doScore": None,
        "evidence": [],
        "history": [],
        "flag": None,
        "disputes": [],
    }


def _orderedSubject(subject):
    ordered = {}
    final = subject.get("final") or {"score": None, "confidence": None, "ci": None}
    ordered["final"] = {
        "score": final.get("score"),
        "confidence": final.get("confidence"),
        "ci": final.get("ci"),
    }
    for key in ("sayScore", "doScore", "evidence", "history", "flag", "disputes"):
        ordered[key] = subject.get(key, _emptySubject()[key])
    for key, value in subject.items():
        if key not in ordered and key != "final":
            ordered[key] = value
    return ordered


def _orderedLedger(ledger):
    ordered = {}
    for key in ("engagement", "pack", "scale", "runs"):
        ordered[key] = ledger.get(key)
    ordered["subjects"] = {
        subjectId: _orderedSubject(ledger.get("subjects", {})[subjectId])
        for subjectId in sorted(ledger.get("subjects", {}))
    }
    for key, value in ledger.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def writeLedger(path, ledger):
    """Write the ledger atomically: serialise to a temp file in the same
    directory, then os.replace so a crash mid write never truncates the
    ledger."""
    payload = json.dumps(_orderedLedger(ledger), indent=2, ensure_ascii=False) + "\n"
    directory = os.path.dirname(os.path.abspath(path))
    fd, tempPath = tempfile.mkstemp(dir=directory, prefix=".scoreLedger.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
        os.replace(tempPath, path)
    except BaseException:
        try:
            os.unlink(tempPath)
        except OSError:
            pass
        raise


def loadLedger(path):
    """Load scoreLedger.json, turning a JSON decode failure into an
    actionable message."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"{path} is not valid JSON ({error}). The ledger may be corrupted "
            "or the victim of an interrupted write; recover the last good "
            "version from git (git checkout -- scoreLedger.json) and rerun."
        ) from error


def _driverText(lastEntry, score, confidence, trigger):
    if lastEntry is None or lastEntry.get("score") is None:
        return f"sets initial score {score} ({confidence}) after {trigger}"
    previous = lastEntry.get("score")
    if score > previous:
        return f"lifts from {previous} to {score} after {trigger}"
    if score < previous:
        return f"lowers from {previous} to {score} after {trigger}"
    return f"holds at {score}, confidence now {confidence}, after {trigger}"


def runAggregation(repoRoot, trigger=None, today=None, pluginRoot=None):
    """Recompute finals, CIs, flags, history, and runs for an engagement repo.

    ``today`` (ISO 8601 string) and ``pluginRoot`` exist for deterministic
    testing; the CLI leaves them at their defaults. Returns True when the
    ledger changed.
    """
    loader = _loadConfigLoader()
    if pluginRoot is None:
        pluginRoot = os.path.dirname(_ENGINE_DIR)
    engagement = loader.loadEngagement(repoRoot)
    _, pack = loader.resolvePack(repoRoot, pluginRoot)
    directOverIndirect, highOverLow = resolveWeights(engagement, pack)

    ledgerPath = os.path.join(repoRoot, "scoreLedger.json")
    if os.path.isfile(ledgerPath):
        ledger = loadLedger(ledgerPath)
    else:
        ledger = {"runs": [], "subjects": {}}

    engagementBlock = engagement.get("engagement") or {}
    ledger["engagement"] = engagementBlock.get("code")
    ledger["pack"] = f"{pack.get('id')}@{pack.get('version')}"
    ledger["scale"] = (pack.get("scale") or {}).get("id")
    ledger.setdefault("runs", [])
    ledger.setdefault("subjects", {})

    runs = ledger["runs"]
    nextRun = max((entry.get("run", 0) for entry in runs), default=0) + 1
    triggerText = trigger if trigger is not None else DEFAULT_TRIGGER
    changed = False

    scaleLow, scaleHigh = loader.scaleBounds(pack)

    for subjectId in _taxonomySubjects(pack):
        subject = ledger["subjects"].setdefault(subjectId, _emptySubject())
        subject.setdefault("history", [])
        validateEvidence(subjectId, subject.get("evidence"), scaleLow, scaleHigh)
        result = computeSubject(subject.get("evidence"), directOverIndirect, highOverLow)
        if result is None:
            newFinal = {"score": None, "confidence": None, "ci": None}
            newFlag = None
            history = subject["history"]
            last = history[-1] if history else None
            if last is not None and last.get("score") is not None:
                history.append(
                    {
                        "run": nextRun,
                        "score": None,
                        "confidence": None,
                        "driver": f"reverts to unscored after {triggerText}",
                    }
                )
                changed = True
        else:
            score, confidence, ci = result
            newFinal = {"score": score, "confidence": confidence, "ci": ci}
            newFlag = flagFor(score)
            history = subject["history"]
            last = history[-1] if history else None
            if last is None or last.get("score") != score or last.get("confidence") != confidence:
                history.append(
                    {
                        "run": nextRun,
                        "score": score,
                        "confidence": confidence,
                        "driver": _driverText(last, score, confidence, triggerText),
                    }
                )
                changed = True
        if subject.get("final") != newFinal or subject.get("flag") != newFlag:
            changed = True
        subject["final"] = newFinal
        subject["flag"] = newFlag

    if changed or trigger is not None:
        runDate = today if today is not None else datetime.date.today().isoformat()
        runs.append({"run": nextRun, "date": runDate, "trigger": triggerText})

    writeLedger(ledgerPath, ledger)
    return changed


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Recompute finals, confidence intervals, flags, history, and runs in scoreLedger.json."
    )
    parser.add_argument("--repo", required=True, help="engagement repo root")
    parser.add_argument("--run-trigger", dest="trigger", default=None, help="trigger text recorded against this run")
    args = parser.parse_args(argv)
    runAggregation(args.repo, trigger=args.trigger)
    return 0


if __name__ == "__main__":
    sys.exit(main())
