# MCP for Unity — Editor Plugin Guide

> **Status audit (2026-06-20):** General Unity MCP bridge editor guide,
> source-refreshed against the current UI UXML/controllers, package metadata,
> and server-launch/config builders. This is not CE-specific control-surface
> authority. Python server tests passed; Unity/client runtime smoke tests were
> not run.

Use this guide to configure and run MCP for Unity inside the Unity Editor. Installation is covered elsewhere; this document focuses on the Editor window, client configuration, and troubleshooting.

## Open the window
- Unity menu: `Window > MCP For Unity > Toggle MCP Window`

The window has `Settings` and `Tools` tabs. `Settings` contains the
Connection, Client Configuration, and Settings sections; `Tools` controls
per-tool enablement and rescans.

---

## Quick start
1. Open `Window > MCP For Unity > Toggle MCP Window`.
2. In Connection, keep `HTTP Local` selected unless you need `HTTP Remote` or `Stdio`, and confirm the HTTP URL.
3. Click `Start Server`. In HTTP Local mode this launches the local `uvx --from ... mcp-for-unity` server and starts the Unity session; Unity-managed launches may append lifecycle args such as `--pidfile <path>` and `--unity-instance-token <token>`.
4. In Client Configuration, select your client and click `Configure`, or click `Configure All Detected Clients`.
5. Use your MCP client to connect. Current source-registered clients include Antigravity, Cherry Studio, Claude Code, Claude Desktop, CodeBuddy CLI, Codex, Cursor, Kilo Code, Kiro, Rider GitHub Copilot, Trae, VSCode GitHub Copilot, VSCode Insiders GitHub Copilot, and Windsurf.

---

## Connection
- Transport:
  - `HTTP Local` is the default.
  - `HTTP Remote` points clients at an already-running remote HTTP server.
  - `Stdio` uses the local Unity socket bridge instead of the HTTP/WebSocket path.
- HTTP URL:
  - Shown for HTTP transports; defaults to `http://localhost:8080`.
  - MCP clients use the same base URL with `/mcp` appended.
- Local HTTP server command:
  - Shows the core `uvx --from ... mcp-for-unity --transport http --http-url ...` command. The copy/manual command omits Unity-managed lifecycle args; `Start Server` may append `--pidfile <path>` and `--unity-instance-token <token>` when it opens the terminal.
  - Includes a copy button and the `Start Server` / `Stop Server` action.
- Unity Socket Port:
  - Shown for Stdio mode; the port varies and is shown in the UI.
- Status and Health:
  - Connection status reports the current session state.
  - Health is a separate verify/ping check and can differ from session state.

---

## Unity Bridge
- Shows Running or Stopped with a status dot.
- In HTTP Local mode, use `Start Server` / `Stop Server` to launch the local HTTP server and manage the Unity session.
- In Stdio mode, use the connection toggle (`Start`, then `Start Session` / `End Session`) for the Unity bridge session used by stdio clients.
- Tip: after configuring a client, status text is transport-specific. The current UI exposes path repair through the Settings tab's `UV Path:` row and the Client Configuration section's `Claude CLI Path:` row.

---

## MCP Client Configuration
- Select Client: Choose your target MCP client from the source-registered configurator list.
- Per-client actions:
  - Cursor / VS Code / Windsurf:
    - Configure: Writes/updates your config for the selected transport.
      - HTTP mode writes a URL such as `http://localhost:8080/mcp`.
      - Stdio mode writes `uvx --from <git-url> mcp-for-unity --transport stdio`.
    - Manual configuration: Review/copy the generated JSON snippet from the window.
    - UV path repair: Open Settings -> Advanced Settings, use the `UV Path:` row's `Browse` button, and pick the executable in the `Select uv Executable` file dialog.
    - A compact “Config:” line shows the resolved config file name once uv/server are detected.
  - Claude Code:
    - Register / Unregister MCP for Unity with Claude Code.
    - If the CLI isn’t found, the `Claude CLI Path:` field says `Not found - click Browse to select`; use `Browse` to open the `Select Claude CLI` file dialog.
    - The window displays the resolved Claude CLI path when detected.

Notes:
- The UI shows a status dot and short status text such as `Configured`, `Connected`, and transport/configuration-specific errors.
- Claude Desktop and Cherry Studio are non-HTTP exceptions in current source.
  Claude Desktop is stdio-only; Cherry Studio uses manual UI configuration
  with stdio values. Their configurators refuse HTTP mode and ask you to switch
  transport first.
- Use `Configure` for one-click setup; use the generated snippet when you prefer to review/copy config.

---

## Script Validation
- Validation Level options:
  - Basic — Only syntax checks
  - Standard — Syntax + Unity practices
  - Comprehensive — All checks + semantic analysis
  - Strict — Full semantic validation (requires Roslyn)
- Pick a level based on your project’s needs. A description is shown under the dropdown.

---

## Troubleshooting
- Python or `uv` not found:
  - Help: [Fix MCP for Unity with Cursor, VS Code & Windsurf](https://github.com/CoplayDev/unity-mcp/wiki/1.-Fix-Unity-MCP-and-Cursor,-VSCode-&-Windsurf)
- Claude CLI not found:
  - Help: [Fix MCP for Unity with Claude Code](https://github.com/CoplayDev/unity-mcp/wiki/2.-Fix-Unity-MCP-and-Claude-Code)

---

## Tips
- Use Cmd+Shift+M (macOS) / Ctrl+Shift+M (Windows, Linux) to toggle the MCP for Unity window.
- Enable “Debug Mode” in Settings for more Console detail when diagnosing issues.
- Use Advanced Settings to override the `uv` path or the server source used for `uvx --from`.

---
