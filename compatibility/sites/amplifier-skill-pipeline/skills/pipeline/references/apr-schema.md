# Abstract Pipeline Representation (APR) Schema

The APR is the core data model of this bundle. It captures *what* a CI/CD pipeline does in a platform-agnostic format. Platform Generators render the APR into native CI/CD configs (GitHub Actions, GitLab CI, Azure DevOps).

The APR is produced by the Pipeline Architect agent based on a Project Profile and user input. It can also be reverse-engineered from existing CI/CD configs by the Pipeline Auditor agent.

## Design Principles

- **Platform-agnostic** — No platform-specific syntax or references
- **Human-readable** — Structured YAML that a developer can review and understand
- **Diffable** — Changes to pipeline design are visible in version control
- **Complete** — Contains everything needed to render a working pipeline on any supported platform
- **Storable** — Saved alongside generated configs for drift detection

## Schema

```yaml
apr:
  # Metadata
  version: "1.0"                    # APR schema version
  generated_at: string              # ISO 8601 timestamp
  generated_from: string            # "project-profile" | "existing-config" | "user-input"
  target_platforms: string[]        # e.g., ["github-actions", "gitlab-ci"]

  # Triggers — what starts the pipeline
  triggers:
    - type: string                  # "push" | "pull_request" | "schedule" | "manual" | "tag"
      branches: string[] | null     # e.g., ["main", "release/*"]
      paths: string[] | null        # e.g., ["src/**", "package.json"]
      paths_ignore: string[] | null # e.g., ["docs/**", "*.md"]
      schedule: string | null       # Cron expression, e.g., "0 2 * * 1"
      tags: string[] | null         # e.g., ["v*"]

  # Stages — ordered groups of work
  stages:
    - name: string                  # e.g., "ci", "build", "deploy-staging", "deploy-prod"
      description: string
      depends_on: string[] | null   # Stage names this stage depends on
      condition: string | null      # When to run, e.g., "branch == main"
      environment: string | null    # Target environment name

      # Jobs within this stage
      jobs:
        - name: string              # e.g., "lint", "test-unit", "build-docker"
          description: string
          runner: string            # e.g., "ubuntu-latest", "macos-latest"
          timeout_minutes: integer
          depends_on: string[] | null
          condition: string | null
          services: service[] | null

          # Matrix strategy
          matrix:
            enabled: boolean
            dimensions:
              - name: string        # e.g., "python-version"
                values: string[]    # e.g., ["3.11", "3.12", "3.13"]
            fail_fast: boolean

          # Steps within this job
          steps:
            - name: string
              type: string          # "checkout" | "setup" | "cache" | "run" | "upload" | "download"
              command: string | null
              tool: string | null
              version: string | null
              cache_key: string | null
              cache_paths: string[] | null
              artifact_name: string | null
              artifact_paths: string[] | null
              env: map | null
              secrets: string[] | null

          outputs:
            - name: string
              value: string

  # Secrets
  secrets:
    - name: string                  # e.g., "DOCKER_REGISTRY_TOKEN"
      description: string
      sensitivity: string           # "low" | "medium" | "high"
      required_for: string[]        # Job names that reference this
      platform_feature: string | null  # e.g., "oidc"

  # Artifacts
  artifacts:
    - name: string
      produced_by: string           # Job name
      consumed_by: string[] | null  # Job names
      paths: string[]
      retention_days: integer | null

  # Caching strategy
  caching:
    - name: string
      type: string                  # "dependency" | "build" | "layer"
      key_pattern: string
      paths: string[]
      restore_keys: string[] | null

  # Environments
  environments:
    - name: string
      requires_approval: boolean
      approvers: string[] | null
      deployment_branch: string | null
      variables: map | null

  # Service definitions (referenced by jobs)
  services:
    - name: string
      image: string
      ports: string[]
      env: map | null
      health_check: string | null
```

## Complete Example: Python + Docker Project

A CI/CD pipeline for a Python FastAPI service with Docker, deploying to staging:

```yaml
apr:
  version: "1.0"
  generated_at: "2026-03-26T10:30:00Z"
  generated_from: "project-profile"
  target_platforms: ["github-actions"]

  triggers:
    - type: "push"
      branches: ["main"]
    - type: "pull_request"
      branches: ["main"]

  stages:
    - name: "ci"
      description: "Continuous integration — lint, type check, test, build"
      depends_on: null
      condition: null
      environment: null
      jobs:
        - name: "quality"
          description: "Linting, formatting, and type checking"
          runner: "ubuntu-latest"
          timeout_minutes: 10
          depends_on: null
          condition: null
          services: null
          matrix:
            enabled: false
            dimensions: []
            fail_fast: false
          steps:
            - name: "Checkout code"
              type: "checkout"
              command: null
              tool: null
              version: null
              cache_key: null
              cache_paths: null
              artifact_name: null
              artifact_paths: null
              env: null
              secrets: null
            - name: "Set up Python"
              type: "setup"
              command: null
              tool: "python"
              version: "3.12"
              cache_key: null
              cache_paths: null
              artifact_name: null
              artifact_paths: null
              env: null
              secrets: null
            - name: "Install dependencies"
              type: "run"
              command: "uv sync --frozen"
              tool: null
              version: null
              cache_key: "uv-{{ hashFiles('uv.lock') }}"
              cache_paths: ["~/.cache/uv"]
              artifact_name: null
              artifact_paths: null
              env: null
              secrets: null
            - name: "Lint"
              type: "run"
              command: "uv run ruff check src/"
              tool: null
              version: null
              cache_key: null
              cache_paths: null
              artifact_name: null
              artifact_paths: null
              env: null
              secrets: null
            - name: "Type check"
              type: "run"
              command: "uv run pyright src/"
              tool: null
              version: null
              cache_key: null
              cache_paths: null
              artifact_name: null
              artifact_paths: null
              env: null
              secrets: null
          outputs: []

        - name: "test"
          description: "Run unit and integration tests with Postgres"
          runner: "ubuntu-latest"
          timeout_minutes: 15
          depends_on: null
          condition: null
          services:
            - name: "postgres"
              image: "postgres:16"
              ports: ["5432:5432"]
              env: {"POSTGRES_DB": "test", "POSTGRES_PASSWORD": "test"}
              health_check: "pg_isready -U postgres"
          matrix:
            enabled: false
            dimensions: []
            fail_fast: false
          steps:
            - name: "Checkout code"
              type: "checkout"
              command: null
              tool: null
              version: null
              cache_key: null
              cache_paths: null
              artifact_name: null
              artifact_paths: null
              env: null
              secrets: null
            - name: "Set up Python"
              type: "setup"
              command: null
              tool: "python"
              version: "3.12"
              cache_key: null
              cache_paths: null
              artifact_name: null
              artifact_paths: null
              env: null
              secrets: null
            - name: "Install dependencies"
              type: "run"
              command: "uv sync --frozen"
              tool: null
              version: null
              cache_key: "uv-{{ hashFiles('uv.lock') }}"
              cache_paths: ["~/.cache/uv"]
              artifact_name: null
              artifact_paths: null
              env: null
              secrets: null
            - name: "Run tests"
              type: "run"
              command: "uv run pytest tests/ -v --cov=src --cov-report=xml"
              tool: null
              version: null
              cache_key: null
              cache_paths: null
              artifact_name: null
              artifact_paths: null
              env:
                DATABASE_URL: "postgresql://postgres:test@localhost:5432/test"
              secrets: null
            - name: "Upload coverage"
              type: "upload"
              command: null
              tool: null
              version: null
              cache_key: null
              cache_paths: null
              artifact_name: "coverage-report"
              artifact_paths: ["coverage.xml"]
              env: null
              secrets: null
          outputs: []

        - name: "build-docker"
          description: "Build and push Docker image"
          runner: "ubuntu-latest"
          timeout_minutes: 15
          depends_on: ["quality", "test"]
          condition: "trigger == push AND branch == main"
          services: null
          matrix:
            enabled: false
            dimensions: []
            fail_fast: false
          steps:
            - name: "Checkout code"
              type: "checkout"
              command: null
              tool: null
              version: null
              cache_key: null
              cache_paths: null
              artifact_name: null
              artifact_paths: null
              env: null
              secrets: null
            - name: "Set up Docker Buildx"
              type: "setup"
              command: null
              tool: "docker-buildx"
              version: null
              cache_key: null
              cache_paths: null
              artifact_name: null
              artifact_paths: null
              env: null
              secrets: null
            - name: "Login to registry"
              type: "run"
              command: "echo $REGISTRY_TOKEN | docker login ghcr.io -u $GITHUB_ACTOR --password-stdin"
              tool: null
              version: null
              cache_key: null
              cache_paths: null
              artifact_name: null
              artifact_paths: null
              env: null
              secrets: ["REGISTRY_TOKEN"]
            - name: "Build and push"
              type: "run"
              command: "docker buildx build --push --tag ghcr.io/$REPO:$SHA --tag ghcr.io/$REPO:latest --cache-from type=gha --cache-to type=gha,mode=max ."
              tool: null
              version: null
              cache_key: null
              cache_paths: null
              artifact_name: null
              artifact_paths: null
              env: null
              secrets: null
          outputs:
            - name: "image_tag"
              value: "ghcr.io/$REPO:$SHA"

    - name: "deploy-staging"
      description: "Deploy to staging environment"
      depends_on: ["ci"]
      condition: "trigger == push AND branch == main"
      environment: "staging"
      jobs:
        - name: "deploy"
          description: "Deploy Docker image to staging"
          runner: "ubuntu-latest"
          timeout_minutes: 10
          depends_on: null
          condition: null
          services: null
          matrix:
            enabled: false
            dimensions: []
            fail_fast: false
          steps:
            - name: "Deploy to staging"
              type: "run"
              command: "deploy --environment staging --image $IMAGE_TAG"
              tool: null
              version: null
              cache_key: null
              cache_paths: null
              artifact_name: null
              artifact_paths: null
              env:
                IMAGE_TAG: "{{ stages.ci.jobs.build-docker.outputs.image_tag }}"
              secrets: ["DEPLOY_KEY"]
          outputs: []

  secrets:
    - name: "REGISTRY_TOKEN"
      description: "Token for pushing to GitHub Container Registry"
      sensitivity: "medium"
      required_for: ["build-docker"]
      platform_feature: "oidc"
    - name: "DEPLOY_KEY"
      description: "Key for deploying to staging environment"
      sensitivity: "high"
      required_for: ["deploy"]
      platform_feature: null

  artifacts:
    - name: "coverage-report"
      produced_by: "test"
      consumed_by: null
      paths: ["coverage.xml"]
      retention_days: 30

  caching:
    - name: "uv-cache"
      type: "dependency"
      key_pattern: "uv-{{ hashFiles('uv.lock') }}"
      paths: ["~/.cache/uv"]
      restore_keys: ["uv-"]
    - name: "docker-layer-cache"
      type: "layer"
      key_pattern: "docker-{{ hashFiles('Dockerfile') }}"
      paths: []
      restore_keys: ["docker-"]

  environments:
    - name: "staging"
      requires_approval: false
      approvers: null
      deployment_branch: "main"
      variables:
        APP_ENV: "staging"
        LOG_LEVEL: "debug"
```
