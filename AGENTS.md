# AGENTS.md - Unity MCP in the CE Workspace

## Current Status

This repository is a clean checkout of Jeremy's fork of `CoplayDev/unity-mcp`.
It is currently the general MCP for Unity bridge, not a CE-specific Builder
control-surface package.

Verified on 2026-05-03:

- Unity package: `MCPForUnity/package.json`, `com.coplaydev.unity-mcp`, version `8.7.0`
- Python server: `Server/pyproject.toml`, `mcpforunityserver`, version `8.7.0`
- Unity tools: `MCPForUnity/Editor/Tools/`
- Python tools: `Server/src/services/tools/`
- Python tests: `Server/tests/integration/`

## CE Boundary

Use CE architecture rules when applying this bridge to Curation Engine:

```
MCP -> Builder control surface -> Config -> re-manifestation
```

Do not claim CE-specific tools exist here unless code proves it. The current
checkout does not contain `CEBuilderSerializer.cs`, `get_builder_control_surface`,
`place_room`, `mount_artwork`, or the older `UnityMcpBridge/` package path.

## Development Commands

From `Server/`:

```bash
uv run src/main.py --transport http --http-url http://localhost:8080
uv run pytest
```

In Unity, open:

```text
Window > MCP for Unity
```

## Documentation Rules

- Preserve upstream MCP for Unity docs when they describe the current package and server accurately.
- Add CE notes only when verified against this checkout or the owning CE project.
- Before changing tool docs, inspect both `Server/src/services/tools/` and
  `MCPForUnity/Editor/Tools/`.
- Before changing version references, verify both `MCPForUnity/package.json` and
  `Server/pyproject.toml`.

