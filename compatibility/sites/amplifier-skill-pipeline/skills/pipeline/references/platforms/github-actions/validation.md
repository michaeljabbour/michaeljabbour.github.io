# GitHub Actions: Validation
## actionlint
Fast, offline linter for workflow files:
```bash
# Install
brew install actionlint  # macOS
go install github.com/rhysd/actionlint/cmd/actionlint@latest  # Go

# Run
actionlint .github/workflows/*.yml
```
## Common Errors actionlint Catches
- Invalid `on` trigger syntax
- Undefined step outputs referenced
- Expression syntax errors
- Deprecated action versions
- Invalid `runs-on` values
## YAML Validation
```bash
# Basic YAML syntax
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"

# Schema validation
pip install check-jsonschema
check-jsonschema --builtin-schema vendor.github-workflows .github/workflows/*.yml
```
## act (Local Testing)
Run workflows locally:
```bash
brew install act
act push  # Simulate push event
act pull_request --job test  # Run specific job
```
Note: act doesn't support all features (services, environments, OIDC).
