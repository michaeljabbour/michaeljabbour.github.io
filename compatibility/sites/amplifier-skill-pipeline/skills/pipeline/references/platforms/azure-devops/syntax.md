# Azure DevOps: Pipeline Syntax
## File Location
`azure-pipelines.yml` in repository root
## Structure
```yaml
trigger:
  branches: { include: [main] }
  paths: { include: [src/*] }
pr:
  branches: { include: [main] }

pool: { vmImage: ubuntu-latest }

variables:
  pythonVersion: "3.12"

stages:
  - stage: CI
    jobs:
      - job: Test
        timeoutInMinutes: 15
        steps:
          - task: UsePythonVersion@0
            inputs: { versionSpec: $(pythonVersion) }
          - script: pytest tests/ -v
            displayName: Run tests
          - task: PublishTestResults@2
            inputs: { testResultsFiles: "**/junit.xml" }
```
## Key Differences
- `trigger:` and `pr:` are separate (not combined `on:`)
- Uses `task:` for built-in actions (not `uses:`)
- `pool:` instead of `runs-on:`
- `displayName:` for human-readable step names
- Variables use `$(varName)` syntax
