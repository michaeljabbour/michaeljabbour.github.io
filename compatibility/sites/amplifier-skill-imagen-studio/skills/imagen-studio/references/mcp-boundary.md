# MCP-only execution boundary

The retained native adapter is `modules/tool-imagen/`, independent from the separately installed provider server. It declares no imagen-mcp distribution dependency, imports no server implementation, and never auto-discovers sibling development directories. Configuration selects an explicit executable/checkout or a separately installed command on PATH. Do not add provider-library imports to make a local test convenient.

Reviewed tool names: `generate_image`, `generate_image_batch`, `conversational_image`, `edit_image`, `estimate_cost`, `list_providers`, `list_conversations`, `list_gemini_models`. Argument schemas come from MCP discovery, not this prose. Initialization validates the compatible server protocol/version, tool membership, request timeout, errors, bounded model-visible results, and owned cleanup.

Fast/Guided/Studio judgment is portable; an available host tool can supply execution. The optional native adapter's current compatibility range is a versioned contract, not permission to silently upgrade an independently released 0.x server. Check the live discovery and adapter tests before changing it. Local ASCII conversion is a separate Pillow-backed utility and uses no MCP server.
