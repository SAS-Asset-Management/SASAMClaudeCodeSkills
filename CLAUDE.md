# SASAMClaudeCodeSkills — Project Rules

## Version Bumping (MANDATORY)

**Every commit that changes plugin functionality MUST bump VERSION and CHANGELOG.md before pushing.**

1. Increment version in `VERSION` (semver: major.minor.patch)
   - **Patch** (1.3.0 → 1.3.1): bug fixes, typo corrections, minor reference updates
   - **Minor** (1.3.0 → 1.4.0): new skills, wiki pages, scripts, feature additions
   - **Major** (1.3.0 → 2.0.0): breaking changes to skill interfaces or plugin structure
2. Add a dated section to `CHANGELOG.md` at the top (below the header), following Keep a Changelog format
3. Commit VERSION + CHANGELOG.md in the same commit as the changes, or as a dedicated bump commit

**Why:** The `/sasam-update` skill compares local VERSION against GitHub VERSION. If you forget to bump, users will never see the update.

## Manifest

After adding or removing files, regenerate the file manifest:
```bash
./generate-manifest.sh
```
