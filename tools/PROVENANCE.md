# Provenance

This shared implementation develops the preview, complete-method installation and compatibility principles used by the Market Fit capability. The original Market Fit MIT notice is retained in LICENSE. No family-theme files are distributed here; the theme notice at the end of that retained license concerns the original theme.

The canonical maintained source is the tools directory of the public repository https://github.com/michaeljabbour/michaeljabbour.github.io. `capability.py`, `contract.schema.json` and `test_capability.py` are the exact reviewed shared-source bytes, without a separate copy in each capability repository. The schema identity remains `urn:amplifier:capability-contract:v1` and the contract version remains `amplifier-capability/v1`.

The publication build records its exact Git revision and file SHA256 values in the download manifest. The installer uses Python's standard library and Git; it adds no model SDK, package bootstrap, external capability or persistent account integration. Its transactions preserve prior copies for explicit rollback.
