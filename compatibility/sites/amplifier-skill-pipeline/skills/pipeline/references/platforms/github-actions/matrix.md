# GitHub Actions: Matrix Strategies
## Basic Matrix
```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
    os: [ubuntu-latest, macos-latest]
  fail-fast: true
  max-parallel: 4
```
## Dynamic Matrix
Generate matrix at runtime:
```yaml
jobs:
  generate:
    outputs:
      matrix: ${{ steps.set.outputs.matrix }}
    steps:
      - id: set
        run: echo "matrix=$(cat matrix.json)" >> $GITHUB_OUTPUT
  test:
    needs: generate
    strategy:
      matrix: ${{ fromJson(needs.generate.outputs.matrix) }}
```
## Include/Exclude
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    include:
      - os: ubuntu-latest
        extra-flag: --fast
    exclude:
      - os: windows-latest
```
## Test Sharding
```yaml
strategy:
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - run: npx playwright test --shard=${{ matrix.shard }}/4
```
