# Project Profile Schema

The Project Profile is the output of the Pipeline Scout agent. It captures everything detected about a project that's relevant to CI/CD pipeline design.

The Pipeline Scout produces this by inspecting file trees, package manifests, Dockerfiles, existing CI configs, and other project artifacts. Fields that can't be determined are set to `null` — the explore phase will ask the user about them.

## Schema

```yaml
project_profile:
  # Project identity
  name: string                    # Project name (from package.json, pyproject.toml, etc.)
  repository_url: string | null   # Git remote URL if available
  monorepo: boolean               # Whether the project contains multiple packages/services

  # Languages and frameworks
  languages:
    - name: string                # e.g., "python", "typescript", "go"
      version: string | null      # e.g., "3.12", "22", "1.22"
      detected_from: string       # e.g., "pyproject.toml", ".nvmrc", "go.mod"

  frameworks:
    - name: string                # e.g., "fastapi", "next.js", "gin"
      version: string | null
      detected_from: string

  # Build and package
  build_tools:
    - name: string                # e.g., "npm", "uv", "cargo", "docker"
      config_file: string         # e.g., "package.json", "pyproject.toml"

  package_managers:
    - name: string                # e.g., "npm", "yarn", "pnpm", "uv", "pip"
      lockfile: string | null     # e.g., "package-lock.json", "uv.lock"

  # Testing
  test_runners:
    - name: string                # e.g., "pytest", "jest", "vitest", "go test"
      config_file: string | null  # e.g., "pytest.ini", "jest.config.ts"
      detected_tests: string[]    # Glob patterns of test files found

  # Quality tools
  linters:
    - name: string                # e.g., "ruff", "eslint", "golangci-lint"
      config_file: string | null

  type_checkers:
    - name: string                # e.g., "pyright", "tsc", "mypy"
      config_file: string | null

  formatters:
    - name: string                # e.g., "ruff format", "prettier", "gofmt"
      config_file: string | null

  # Containerization
  docker:
    present: boolean
    dockerfile_path: string | null       # e.g., "Dockerfile", "docker/Dockerfile"
    compose_file: string | null          # e.g., "docker-compose.yml"
    multi_stage: boolean | null          # Whether Dockerfile uses multi-stage builds

  # Existing CI/CD
  existing_ci:
    - platform: string            # e.g., "github-actions", "gitlab-ci", "azure-devops", "jenkins"
      config_files: string[]      # e.g., [".github/workflows/ci.yml"]
      detected_stages: string[]   # e.g., ["build", "test", "deploy"]

  # Deployment indicators (often can't be fully detected — filled by user)
  deployment:
    targets: string[] | null      # e.g., ["aws-ecs", "vercel", "kubernetes"]
    environments: string[] | null # e.g., ["staging", "production"]
    branching_strategy: string | null  # e.g., "trunk-based", "gitflow", "github-flow"

  # Metadata
  detected_at: string             # ISO 8601 timestamp
  confidence: string              # "high", "medium", "low" — overall detection confidence
  gaps: string[]                  # Fields that couldn't be detected and need user input
```

## Example: Python + Docker Project

```yaml
project_profile:
  name: "payment-service"
  repository_url: "https://github.com/acme/payment-service"
  monorepo: false

  languages:
    - name: "python"
      version: "3.12"
      detected_from: "pyproject.toml"

  frameworks:
    - name: "fastapi"
      version: "0.115.0"
      detected_from: "pyproject.toml"

  build_tools:
    - name: "uv"
      config_file: "pyproject.toml"
    - name: "docker"
      config_file: "Dockerfile"

  package_managers:
    - name: "uv"
      lockfile: "uv.lock"

  test_runners:
    - name: "pytest"
      config_file: "pyproject.toml"
      detected_tests: ["tests/**/*.py"]

  linters:
    - name: "ruff"
      config_file: "pyproject.toml"

  type_checkers:
    - name: "pyright"
      config_file: "pyproject.toml"

  formatters:
    - name: "ruff format"
      config_file: "pyproject.toml"

  docker:
    present: true
    dockerfile_path: "Dockerfile"
    compose_file: "docker-compose.yml"
    multi_stage: true

  existing_ci: []

  deployment:
    targets: null
    environments: null
    branching_strategy: null

  detected_at: "2026-03-26T10:00:00Z"
  confidence: "high"
  gaps: ["deployment.targets", "deployment.environments", "deployment.branching_strategy"]
```

## Example: Node.js Monorepo

```yaml
project_profile:
  name: "acme-platform"
  repository_url: "https://github.com/acme/platform"
  monorepo: true

  languages:
    - name: "typescript"
      version: "5.7"
      detected_from: "tsconfig.json"

  frameworks:
    - name: "next.js"
      version: "15.2.0"
      detected_from: "packages/web/package.json"
    - name: "express"
      version: "4.21.0"
      detected_from: "packages/api/package.json"

  build_tools:
    - name: "turbo"
      config_file: "turbo.json"
    - name: "docker"
      config_file: "Dockerfile"

  package_managers:
    - name: "pnpm"
      lockfile: "pnpm-lock.yaml"

  test_runners:
    - name: "vitest"
      config_file: "vitest.config.ts"
      detected_tests: ["packages/*/tests/**/*.test.ts"]
    - name: "playwright"
      config_file: "playwright.config.ts"
      detected_tests: ["e2e/**/*.spec.ts"]

  linters:
    - name: "eslint"
      config_file: "eslint.config.js"

  type_checkers:
    - name: "tsc"
      config_file: "tsconfig.json"

  formatters:
    - name: "prettier"
      config_file: ".prettierrc"

  docker:
    present: true
    dockerfile_path: "Dockerfile"
    compose_file: "docker-compose.yml"
    multi_stage: true

  existing_ci:
    - platform: "github-actions"
      config_files: [".github/workflows/ci.yml"]
      detected_stages: ["lint", "test"]

  deployment:
    targets: ["vercel"]
    environments: ["preview", "production"]
    branching_strategy: null

  detected_at: "2026-03-26T10:00:00Z"
  confidence: "medium"
  gaps: ["deployment.branching_strategy"]
```

## Example: Go Microservice

```yaml
project_profile:
  name: "auth-service"
  repository_url: "https://github.com/acme/auth-service"
  monorepo: false

  languages:
    - name: "go"
      version: "1.23"
      detected_from: "go.mod"

  frameworks:
    - name: "gin"
      version: "1.10.0"
      detected_from: "go.mod"

  build_tools:
    - name: "go"
      config_file: "go.mod"
    - name: "docker"
      config_file: "Dockerfile"

  package_managers:
    - name: "go modules"
      lockfile: "go.sum"

  test_runners:
    - name: "go test"
      config_file: null
      detected_tests: ["**/*_test.go"]

  linters:
    - name: "golangci-lint"
      config_file: ".golangci.yml"

  type_checkers: []

  formatters:
    - name: "gofmt"
      config_file: null

  docker:
    present: true
    dockerfile_path: "Dockerfile"
    compose_file: null
    multi_stage: true

  existing_ci:
    - platform: "jenkins"
      config_files: ["Jenkinsfile"]
      detected_stages: ["build", "test", "deploy"]

  deployment:
    targets: ["kubernetes"]
    environments: ["dev", "staging", "production"]
    branching_strategy: "trunk-based"

  detected_at: "2026-03-26T10:00:00Z"
  confidence: "high"
  gaps: []
```
