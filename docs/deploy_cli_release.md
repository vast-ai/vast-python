# Deploying a CLI release

A release is a tag push. CI (`python-publish.yml`) builds and publishes
`vastai` and `vastai-sdk` to PyPI and attaches the installer assets to the
GitHub Release. **There is no undo**: the tag goes live immediately
(`releases/latest` is what vast.ai's installer redirects serve), and a bad
release is fixed by releasing a newer version.

## 1. See what's shipping

```bash
git checkout master && git pull --ff-only
git log $(git describe --tags --abbrev=0)..master --oneline
```

## 2. Pick the version

- Any `feat` in the list → bump minor (`1.8.3` → `1.9.0`).
- Only fixes/docs/chores → bump patch (`1.8.3` → `1.8.4`).
- Format is `vX.Y.Z` with no leading zeros; CI only fires on that pattern.

## 3. Confirm master is green

Master commits have no checks of their own, so check the PRs that are shipping:

```bash
gh pr checks <PR#>   # for each PR in the log above
```

Then run the CI test set locally on master head, since each PR was tested
without the others merged in:

```bash
cd tests && poetry install && poetry run pytest -q cli api sdk scripts
```

## 4. Tag and push

```bash
git tag vX.Y.Z && git push origin vX.Y.Z
```

## 5. Verify

```bash
gh run watch --repo vast-ai/vast-cli   # publish workflow, all jobs green
curl -fsSL https://github.com/vast-ai/vast-cli/releases/latest/download/manifest.env | grep LATEST
curl -fsSL "https://pypi.org/pypi/vastai/json?nocache=$RANDOM" | python3 -c "import json,sys; print(json.load(sys.stdin)['info']['version'])"
```

PyPI's JSON endpoint is CDN-cached and can report the old version for a few
minutes; the cache-busting query string above avoids that.

## If something goes wrong

- Users can roll back with `vastai update --version X.Y.Z`.
- Fix forward with a new patch release.
- Break-glass manual release: `docs/install-design.md` §13.
