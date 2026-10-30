# GitHub Actions: Workflow Syntax
## File Location
`.github/workflows/<name>.yml`
## Top-Level Structure
```yaml
name: <workflow name>
on: <triggers>
permissions: <token permissions>
concurrency: <concurrency group>
env: <global env vars>
jobs: <job definitions>
```
## Triggers (on:)
```yaml
on:
  push: { branches: [main], paths: [src/**] }
  pull_request: { branches: [main] }
  schedule: [{ cron: "0 2 * * 1" }]
  workflow_dispatch: { inputs: { env: { type: choice, options: [staging, prod] } } }
  release: { types: [published] }
```
## Jobs
```yaml
jobs:
  job-name:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    needs: [other-job]
    if: github.ref == 'refs/heads/main'
    permissions: { contents: read, packages: write }
    environment: { name: staging, url: https://staging.example.com }
    services: { postgres: { image: postgres:16, ports: [5432:5432] } }
    steps: [...]
    outputs: { result: ${{ steps.step-id.outputs.value }} }
```
## Steps
```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with: { python-version: "3.12" }
  - run: echo "Hello"
    env: { MY_VAR: value }
  - id: my-step
    run: echo "value=hello" >> $GITHUB_OUTPUT
```
## Expressions
- `${{ github.ref }}` — branch ref
- `${{ github.sha }}` — commit SHA
- `${{ secrets.MY_SECRET }}` — secret access
- `${{ hashFiles('**/lockfile') }}` — file hash for cache keys
- `${{ needs.job.outputs.value }}` — inter-job data
