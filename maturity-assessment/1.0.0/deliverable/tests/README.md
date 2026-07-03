# Deliverable tests

Run standalone from the plugin root:

```bash
python3 -m pytest deliverable/tests -q --import-mode=importlib
```

The plugin `pytest.ini` sets `testpaths = engine packs`, so these tests are not collected by the default suite — run them with the explicit path above. The merge step adds no configuration; nothing here depends on conftest plumbing or the merged engine package.

Every test loads its module under test via `importlib.util.spec_from_file_location`, matching the plugin wide `--import-mode=importlib` convention.

## Fixtures

- `fixtures/acmeEngagement/` — a fictional Acme Rail engagement (code ACME-CYBER-2026) with a deliberately incomplete ledger: one subject unscored, one with only a say score, one open dispute, and one taxonomy subject missing entirely. The report gate is therefore closed and the build must stamp the DRAFT badge.
- `fixtures/pluginRoot/engine/configLoader.py` — a stub of the engine configLoader public API (`loadYaml`, `loadEngagement`, `resolvePack` with the local overlay resolution order). Tests point `CLAUDE_PLUGIN_ROOT` at `fixtures/pluginRoot` so the deliverable scripts resolve this stub; in production the real engine loader is resolved instead. The fixture engagement carries its pack as a local overlay at `packs/acme-governance/`.

The build tests copy the fixture engagement into a pytest `tmp_path` before building, so no generated output lands inside the plugin tree.
