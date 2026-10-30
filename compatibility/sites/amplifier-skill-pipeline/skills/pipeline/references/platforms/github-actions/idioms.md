# GitHub Actions: Best Practices & Idioms
## Reusable Workflows
Define shared workflows called by other repos:
```yaml
# .github/workflows/reusable-ci.yml
on:
  workflow_call:
    inputs:
      python-version: { type: string, default: "3.12" }
    secrets:
      DEPLOY_KEY: { required: true }
```
## Composite Actions
Reusable step sequences:
```yaml
# .github/actions/setup-python-env/action.yml
runs:
  using: composite
  steps:
    - uses: actions/setup-python@v5
      with: { python-version: ${{ inputs.python-version }} }
    - run: uv sync --frozen
      shell: bash
```
## OIDC for Cloud Auth
Replace static credentials with OIDC tokens:
```yaml
permissions: { id-token: write, contents: read }
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with: { role-to-assume: arn:aws:iam::ACCOUNT:role/ROLE, aws-region: us-east-1 }
```
## Concurrency Control
Prevent parallel deploys or duplicate PR runs:
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Cancel older runs on same branch
```
## Minimal Permissions
Always set `permissions` explicitly — default `write-all` is too broad:
```yaml
permissions:
  contents: read
  pull-requests: write
  packages: write
```
