# GitLab CI: Best Practices
## DRY with extends
```yaml
.python-base:
  image: python:3.12
  before_script: [pip install -r requirements.txt]
  cache: { key: pip, paths: [.cache/pip] }

lint:
  extends: .python-base
  script: [ruff check src/]

test:
  extends: .python-base
  script: [pytest tests/]
```
## Include Templates
```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - project: my-group/ci-templates
    file: /python.yml
  - remote: https://example.com/ci.yml
```
## DAG Pipelines
Use `needs:` to skip stage ordering:
```yaml
build:
  stage: build
  script: [make build]
test:
  stage: test
  needs: [build]  # Starts as soon as build finishes
deploy:
  stage: deploy
  needs: [test]
  when: manual  # Manual approval
```
