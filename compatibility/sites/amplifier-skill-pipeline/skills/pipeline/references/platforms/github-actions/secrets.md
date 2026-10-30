# GitHub Actions: Secrets
## Secret Types
| Scope | Set Via | Access |
|---|---|---|
| Repository | Settings → Secrets → Actions | `${{ secrets.NAME }}` |
| Environment | Settings → Environments → NAME → Secrets | Same syntax, scoped to environment |
| Organization | Org Settings → Secrets | Shared across repos with access policy |
## CLI Management
```bash
gh secret set SECRET_NAME --body "value"
gh secret set SECRET_NAME < secret-file.txt
gh secret list
gh secret delete SECRET_NAME
```
## Environment Secrets
```bash
gh secret set DEPLOY_KEY --env production --body "value"
```
## OIDC (Preferred for Cloud)
Instead of static cloud credentials, use OIDC:
- AWS: `aws-actions/configure-aws-credentials` with `role-to-assume`
- GCP: `google-github-actions/auth` with `workload_identity_provider`
- Azure: `azure/login` with `client-id` and `tenant-id`
## Security Rules
- Never echo secrets — GitHub auto-masks but don't risk it
- Minimize secret scope — use environment secrets over repo secrets
- Rotate regularly — set reminders
- Prefer OIDC over static tokens — no rotation needed
