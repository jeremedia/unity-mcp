# AGENTS.md - Unity MCP in the CE Workspace

> **Status audit (2026-06-20):** Active workspace guidance for Jeremy's fork
> of `CoplayDev/unity-mcp`. Source-reviewed
> `MCPForUnity/package.json`, `Server/pyproject.toml`, `Server/uv.lock`,
> Unity-side tools, and Python server tool/resource registration. Current
> package/server/lockfile version is `8.7.0`. Python server tests pass with the
> dev-extra command below. This is the generic Unity MCP bridge, not the CE
> Builder control-surface package. No Unity/client/Docker runtime smoke was run
> in this pass.

## Current Status

This repository is Jeremy's fork of `CoplayDev/unity-mcp`. It is currently the
general MCP for Unity bridge, not a CE-specific Builder control-surface
package.

Verified on 2026-06-20:

- Unity package: `MCPForUnity/package.json`, `com.coplaydev.unity-mcp`, version `8.7.0`
- Python server: `Server/pyproject.toml`, `mcpforunityserver`, version `8.7.0`
- Lockfile: `Server/uv.lock` records the editable `mcpforunityserver` package
  as version `8.7.0`.
- Unity tools: `MCPForUnity/Editor/Tools/`
- Python tools: `Server/src/services/tools/`
- Python tool/resource registries: `Server/src/services/registry/`, `Server/src/services/tools/__init__.py`, and `Server/src/services/resources/__init__.py`
- Python tests: `uv run --extra dev python -m pytest tests/ -q` passed
  94 tests, skipped 2, and xpassed 7.

## CE Boundary

Use CE architecture rules when applying this bridge to Curation Engine:

```
MCP -> Builder control surface -> Config -> re-manifestation
```

Do not claim CE-specific tools exist here unless code proves it. The active
package path is `MCPForUnity/`, not the vestigial `UnityMcpBridge/` folder, and
the current checkout does not contain `CEBuilderSerializer.cs`,
`get_builder_control_surface`, `place_room`, or `mount_artwork`.

## Development Commands

From `Server/`:

```bash
uv run python src/main.py --transport http --http-url http://localhost:8080
uv run --extra dev python -m pytest tests/ -q
```

In Unity, open:

```text
Window > MCP For Unity > Toggle MCP Window
```

## Documentation Rules

- Preserve upstream MCP for Unity docs when they describe the current package and server accurately.
- Add CE notes only when verified against this checkout or the owning CE project.
- Before changing tool docs, inspect both `Server/src/services/tools/` and
  `MCPForUnity/Editor/Tools/`.
- Before changing version references, verify both `MCPForUnity/package.json` and
  `Server/pyproject.toml`.
