# GitLab CI: Pipeline Syntax
## File Location
`.gitlab-ci.yml` in repository root
## Structure
```yaml
stages: [build, test, deploy]
variables: { CI_DEBUG: "true" }

job-name:
  stage: test
  image: python:3.12
  script: [pytest tests/ -v]
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  artifacts:
    reports: { junit: report.xml }
    paths: [coverage/]
  cache:
    key: $CI_COMMIT_REF_SLUG
    paths: [.cache/pip]
  services:
    - name: postgres:16
      alias: db
  needs: [build-job]  # DAG dependency
  timeout: 15 minutes
```
## Triggers
```yaml
rules:
  - if: $CI_COMMIT_BRANCH == "main"
  - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  - if: $CI_COMMIT_TAG
```
## Key Differences from GitHub Actions
- Stages are declared globally, not per-job
- `needs:` for DAG pipelines (skip stage ordering)
- `extends:` and YAML anchors for DRY
- `include:` for reusable templates
- Services use `alias` for hostname
