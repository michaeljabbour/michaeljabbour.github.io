# GitLab CI: Caching
## Basic Cache
```yaml
cache:
  key:
    files: [uv.lock]
    prefix: uv
  paths: [.cache/uv]
  policy: pull-push  # pull, push, or pull-push
```
## Cache vs Artifacts
| Feature | Cache | Artifacts |
|---|---|---|
| Purpose | Speed up jobs | Pass data between jobs |
| Scope | Per branch/key | Per pipeline |
| Reliability | Best-effort | Guaranteed |
| Use for | Dependencies | Build output, reports |
## Distributed Cache
Use S3/GCS backend for shared caching across runners.
