# Azure DevOps: Best Practices
## Templates
```yaml
# templates/python-ci.yml
parameters:
  - name: pythonVersion
    default: "3.12"
steps:
  - task: UsePythonVersion@0
    inputs: { versionSpec: ${{ parameters.pythonVersion }} }
  - script: pip install -r requirements.txt

# azure-pipelines.yml
stages:
  - stage: CI
    jobs:
      - job: Test
        steps:
          - template: templates/python-ci.yml
            parameters: { pythonVersion: "3.12" }
```
## Variable Groups
Share variables across pipelines:
```yaml
variables:
  - group: production-vars
  - name: localVar
    value: hello
```
## Service Connections
For deployment auth, use service connections (configured in Project Settings):
```yaml
- task: AzureWebApp@1
  inputs:
    azureSubscription: my-service-connection
    appName: my-app
```
## Environments with Approvals
```yaml
- stage: Deploy
  jobs:
    - deployment: DeployWeb
      environment: production  # Approval configured in Environments UI
      strategy:
        runOnce:
          deploy:
            steps:
              - script: deploy.sh
```
