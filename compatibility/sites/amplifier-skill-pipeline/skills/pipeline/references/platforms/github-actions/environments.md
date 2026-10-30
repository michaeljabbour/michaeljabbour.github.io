# GitHub Actions: Environments
## Environment Setup
Configure in Settings → Environments:
- **Protection rules**: Required reviewers, wait timer, branch restrictions
- **Secrets**: Environment-scoped secrets
- **Variables**: Environment-scoped variables
## Usage in Workflow
```yaml
jobs:
  deploy-staging:
    environment:
      name: staging
      url: https://staging.example.com
    runs-on: ubuntu-latest
    steps:
      - run: deploy --env staging
```
## Promotion Pattern
```yaml
jobs:
  deploy-staging:
    environment: staging
    # ... deploys automatically
  deploy-production:
    needs: deploy-staging
    environment: production  # Requires manual approval
    # ... deploys after approval
```
## Branch Protection
Limit which branches can deploy to an environment:
- Settings → Environments → production → Deployment branches → Selected branches → `main`
