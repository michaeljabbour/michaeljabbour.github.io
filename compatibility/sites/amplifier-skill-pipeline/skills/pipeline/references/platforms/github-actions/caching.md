# GitHub Actions: Caching
## actions/cache
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}
    restore-keys: uv-${{ runner.os }}-
```
## Setup Action Built-in Caching
Many setup actions have built-in caching:
```yaml
- uses: actions/setup-python@v5
  with: { python-version: "3.12", cache: "pip" }
- uses: actions/setup-node@v4
  with: { node-version: "22", cache: "pnpm" }
- uses: actions/setup-go@v5
  with: { go-version-file: "go.mod", cache: true }
```
## Docker Layer Caching
```yaml
- uses: docker/build-push-action@v6
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```
## Cache Limits
- 10 GB per repo, evicts least recently used
- Individual cache entries up to ~400 MB compressed
- Cache keys are exact match first, then restore-keys prefix
