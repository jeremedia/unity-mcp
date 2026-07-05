# AGENTS.md - Unity MCP in the CE Workspace

> **Status audit (2026-07-04):** Active Codex-facing guidance for Jeremy's fork of
> `CoplayDev/unity-mcp` — the generic Unity MCP bridge in the CE workspace, NOT
> the CE Builder control-surface package. Package/server/lockfile version `8.7.0`.
> Known-red: none.
> Not proven: no Unity import / Editor-window / client-config / Docker runtime
> smoke, stdio MCP client smoke, Unity-attached tool execution, CE consumer
> response, clean-worktree, remote, or release proof.
> Probe evidence lives in git history (`git log -p AGENTS.md`).

## Current Status

This repository is Jeremy's fork of `CoplayDev/unity-mcp`. It is currently the
general MCP for Unity bridge, not a CE-specific Builder control-surface package.

Version authority (both must agree): `MCPForUnity/package.json`
(`com.coplaydev.unity-mcp`) and `Server/pyproject.toml` (`mcpforunityserver`),
`8.7.0` at this audit. Unity tools: `MCPForUnity/Editor/Tools/`. Python tools:
`Server/src/services/tools/`. Registries: `Server/src/services/registry/`,
`Server/src/services/tools/__init__.py`, `Server/src/services/resources/__init__.py`.

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
