"""Smoke test: build the fictional Acme Rail fixture engagement and
inspect the generated surfaces."""

import importlib.util
import os
import re
import shutil

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE_ENGAGEMENT = os.path.join(HERE, "fixtures", "acmeEngagement")
FIXTURE_PLUGIN_ROOT = os.path.join(HERE, "fixtures", "pluginRoot")

RENDER_FUNCTIONS = [
    "renderDomainRadar",
    "renderSubjectConfidence",
    "renderRunTrend",
    "renderPeerPercentile",
]


def _loadModule(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def builtEngagement(tmp_path, monkeypatch):
    repoRoot = str(tmp_path / "acmeEngagement")
    shutil.copytree(FIXTURE_ENGAGEMENT, repoRoot)
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", FIXTURE_PLUGIN_ROOT)
    buildDashboard = _loadModule(
        "buildDashboardUnderTest",
        os.path.join(HERE, os.pardir, "buildDashboard.py"),
    )
    result = buildDashboard.build(repoRoot)
    return repoRoot, result


def _stripVendorRegion(text):
    return re.sub(
        r"/\* vendorPlotlyBegin.*?vendorPlotlyEnd \*/", "", text, flags=re.S
    )


def test_buildWritesBothSurfaces(builtEngagement):
    repoRoot, result = builtEngagement
    assert os.path.isfile(os.path.join(repoRoot, "deliverable", "dashboard.html"))
    assert os.path.isfile(os.path.join(repoRoot, "deliverable", "summary.html"))
    assert result["gate"]["open"] is False


def test_dashboardContainsFourRenderCalls(builtEngagement):
    repoRoot, _ = builtEngagement
    with open(
        os.path.join(repoRoot, "deliverable", "dashboard.html"), encoding="utf-8"
    ) as handle:
        html = handle.read()
    for functionName in RENDER_FUNCTIONS:
        assert "{}(".format(functionName) in html, functionName


def test_dashboardEmbedsLedgerJson(builtEngagement):
    repoRoot, _ = builtEngagement
    with open(
        os.path.join(repoRoot, "deliverable", "dashboard.html"), encoding="utf-8"
    ) as handle:
        html = handle.read()
    assert '"engagement": "ACME-CYBER-2026"' in html
    assert '"01_strategyAlignment"' in html
    assert 'id="ledger-data"' in html


def test_dashboardHasNoRuntimeNetworkReferences(builtEngagement):
    repoRoot, _ = builtEngagement
    for surface in ("dashboard.html", "summary.html"):
        with open(
            os.path.join(repoRoot, "deliverable", surface), encoding="utf-8"
        ) as handle:
            html = handle.read()
        stripped = _stripVendorRegion(html)
        assert "http://" not in stripped, surface
        assert "https://" not in stripped, surface
        assert "fetch(" not in stripped, surface
        assert "cdn.plot.ly" not in stripped, surface


def test_draftBadgeStampedWhenGateClosed(builtEngagement):
    repoRoot, result = builtEngagement
    assert result["gate"]["reasons"]
    for surface in ("dashboard.html", "summary.html"):
        with open(
            os.path.join(repoRoot, "deliverable", surface), encoding="utf-8"
        ) as handle:
            html = handle.read()
        assert 'class="draft-badge"' in html, surface
        assert "04_assuranceReview" in html, surface


def test_summaryCarriesSectionsDatesAndTagline(builtEngagement):
    repoRoot, _ = builtEngagement
    with open(
        os.path.join(repoRoot, "deliverable", "summary.html"), encoding="utf-8"
    ) as handle:
        html = handle.read()
    assert "Executive context" in html
    assert "04/05/2026" in html
    assert "advanced analytics, expert asset management services" in html
    assert "Acme Rail" in html


def test_summaryIsLightAndPlotlyFree(builtEngagement):
    repoRoot, _ = builtEngagement
    path = os.path.join(repoRoot, "deliverable", "summary.html")
    assert os.path.getsize(path) < 100 * 1024
    with open(path, encoding="utf-8") as handle:
        html = handle.read()
    assert "vendorPlotlyBegin" not in html
    assert "Plotly.newPlot" not in html


def test_summaryRendersInlineSvgRadar(builtEngagement):
    repoRoot, _ = builtEngagement
    with open(
        os.path.join(repoRoot, "deliverable", "summary.html"), encoding="utf-8"
    ) as handle:
        html = handle.read()
    assert "<svg" in html
    assert "<polygon" in html
    assert "Mean maturity score by domain" in html
    assert "Strategy and Planning" in html
    assert "Lowest domain" in html
    assert 'stroke-dasharray="4 4"' in html


def test_dashboardStillEmbedsPlotly(builtEngagement):
    repoRoot, _ = builtEngagement
    with open(
        os.path.join(repoRoot, "deliverable", "dashboard.html"), encoding="utf-8"
    ) as handle:
        html = handle.read()
    assert "vendorPlotlyBegin" in html


def test_singleSourceCiRendersAsLabel(builtEngagement):
    repoRoot, _ = builtEngagement
    with open(
        os.path.join(repoRoot, "deliverable", "dashboard.html"), encoding="utf-8"
    ) as handle:
        html = handle.read()
    # 02_planningDiscipline has one evidence record and a degenerate
    # CI of [1, 1] — no false precision.
    assert "single source" in html
    assert "[1.0, 1.0]" not in html
    # 01_strategyAlignment has two records — the real CI still renders.
    assert "[2.7, 3.3]" in html


def test_gateRequiresReconciledFindings(builtEngagement):
    _, result = builtEngagement
    # The fixture engagement carries no findings/ tree, so the gate
    # names every unwaived taxonomy subject.
    assert any(
        "no findings run directory" in reason
        for reason in result["gate"]["reasons"]
    )


def test_peerPercentileOmittedWithoutBenchmark(builtEngagement):
    repoRoot, _ = builtEngagement
    with open(
        os.path.join(repoRoot, "deliverable", "dashboard.html"), encoding="utf-8"
    ) as handle:
        html = handle.read()
    assert 'id="plot-peerPercentile"' not in html


def test_benchmarkPresenceAddsPeerPercentileContainer(tmp_path, monkeypatch):
    repoRoot = str(tmp_path / "acmeEngagementBench")
    shutil.copytree(FIXTURE_ENGAGEMENT, repoRoot)
    benchmark = (
        '{"01_strategyAlignment": '
        '{"p25": 1.5, "p50": 2.5, "p75": 3.5, "cohortSize": 14}}'
    )
    with open(
        os.path.join(repoRoot, "deliverable", "benchmark.json"),
        "w",
        encoding="utf-8",
    ) as handle:
        handle.write(benchmark)
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", FIXTURE_PLUGIN_ROOT)
    buildDashboard = _loadModule(
        "buildDashboardUnderTestBench",
        os.path.join(HERE, os.pardir, "buildDashboard.py"),
    )
    buildDashboard.build(repoRoot)
    with open(
        os.path.join(repoRoot, "deliverable", "dashboard.html"), encoding="utf-8"
    ) as handle:
        html = handle.read()
    assert 'id="plot-peerPercentile"' in html
    assert '"cohortSize": 14' in html
