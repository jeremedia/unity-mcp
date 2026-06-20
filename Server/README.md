# MCP for Unity Server

> **Status audit (2026-06-20):** General Unity MCP server documentation,
> source-refreshed against `Server/pyproject.toml`, the Python tool/resource
> registries, and current `uvx`/HTTP/stdio launch paths. This is not CE-specific
> Builder control-surface authority. Source metadata and `Server/uv.lock` now
> agree on `8.7.0`; `uv run --extra dev python -m pytest tests/ -q` passed.
> Docker and Unity runtime smoke tests were not run.

[![MCP](https://badge.mcpx.dev?status=on 'MCP Enabled')](https://modelcontextprotocol.io/introduction)
[![python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-red.svg 'MIT License')](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/badge/discord-join-red.svg?logo=discord&logoColor=white)](https://discord.gg/y4p8KfzrN4)

Model Context Protocol server for Unity Editor integration. Control Unity through natural language using AI assistants like Claude, Cursor, and more.

**Maintained by [Coplay](https://www.coplay.dev/?ref=unity-mcp)** - This project is not affiliated with Unity Technologies.

💬 **Join our community:** [Discord Server](https://discord.gg/y4p8KfzrN4)

**Required:** Install the [Unity MCP Plugin](https://github.com/CoplayDev/unity-mcp?tab=readme-ov-file#-step-1-install-the-unity-package) to connect Unity Editor with this MCP server. You also need `uvx` (requires [uv](https://docs.astral.sh/uv/)) to run the server.

**Repository-source caveat:** `pyproject.toml` and `uv.lock` both record
`mcpforunityserver` version `8.7.0` in this checkout. Docker builds still need
an explicit build or container smoke test before the image should be treated as
verified-current.

---

## Installation

### Option 1: PyPI

Install and run directly from PyPI using `uvx`.

**Run Server (HTTP):**

```bash
uvx --from mcpforunityserver mcp-for-unity --transport http --http-url http://localhost:8080
```

**MCP Client Configuration (HTTP):**

```json
{
  "mcpServers": {
    "unityMCP": {
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

**MCP Client Configuration (stdio):**

```json
{
  "mcpServers": {
    "unityMCP": {
      "command": "uvx",
      "args": [
        "--from",
        "mcpforunityserver",
        "mcp-for-unity",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

### Option 2: From GitHub Source

Use this to run the latest released version from the repository. Change the version to `main` to run the latest unreleased changes from the repository.

```json
{
  "mcpServers": {
    "unityMCP": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/CoplayDev/unity-mcp@v8.7.0#subdirectory=Server",
        "mcp-for-unity",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

### Option 3: Docker

**Use Pre-built Image:**

```bash
docker run -p 8080:8080 msanatan/mcp-for-unity-server:latest
```

**Build Locally:**

```bash
docker build -f Server/Dockerfile -t unity-mcp-server .
docker run -p 8080:8080 unity-mcp-server
```

Run the build command from the repository root. The checked-in
`Server/Dockerfile` copies the repository into `/app`, switches to
`/app/Server`, and starts `src/main.py` in HTTP mode on `0.0.0.0:8080` by
default. Configure your MCP client with `"url": "http://localhost:8080/mcp"`.

### Option 4: Local Development

For contributing or modifying the server code:

```bash
# Clone the repository
git clone https://github.com/CoplayDev/unity-mcp.git
cd unity-mcp/Server

# Run with uv
uv run python src/main.py --transport stdio
```

---

## Configuration

The server process alone is not enough for Unity tool execution. In HTTP mode,
the Unity package must connect a session to the same base URL; the MCP client
uses `<base>/mcp`, while the Unity plugin opens the WebSocket session at
`<base>/hub/plugin`. In the normal local flow, the Unity window's **Start
Server** action starts the server and then auto-starts that Unity session.

**Environment Variables:**

- `UNITY_MCP_DEFAULT_INSTANCE` - Default Unity instance to target.
- `UNITY_MCP_SKIP_STARTUP_CONNECT` - Skip initial Unity connection attempt
  (`1`, `true`, `yes`, or `on`).
- `UNITY_MCP_TRANSPORT` - Transport protocol (`stdio` or `http`). Current
  parser defaults mean `--transport http` is the reliable way to start HTTP.
- `UNITY_MCP_HTTP_URL` - HTTP server URL; currently this can override
  `--http-url`.
- `UNITY_MCP_HTTP_HOST` / `UNITY_MCP_HTTP_PORT` - HTTP host/port; explicit
  `--http-host` and `--http-port` override these.
- `UNITY_MCP_TELEMETRY_ENDPOINT` / `UNITY_MCP_TELEMETRY_TIMEOUT` - Telemetry
  endpoint and timeout controls.
- `UNITY_MCP_TELEMETRY_ENABLED` - Listed in server help as an enable flag;
  current runtime opt-out checks are the disable aliases below.
- `DISABLE_TELEMETRY=true`, `UNITY_MCP_DISABLE_TELEMETRY=true`, or
  `MCP_DISABLE_TELEMETRY=true` - Opt out of anonymous usage analytics.

---

## Example Prompts

Once connected, try these commands in your AI assistant:

- "Create a 3D player controller with WASD movement"
- "Add a rotating cube to the scene with a red material"
- "Create a simple platformer level with obstacles"
- "Generate a shader that creates a holographic effect"
- "List all GameObjects in the current scene"

---

## Documentation

For complete documentation, troubleshooting, and advanced usage:

📖 **[Full Documentation](https://github.com/CoplayDev/unity-mcp#readme)**

---

## Requirements

- **Python:** 3.10 or newer
- **Unity Editor:** 2021.3 LTS or newer
- **uv:** Python package manager ([Installation Guide](https://docs.astral.sh/uv/getting-started/installation/))

---

## License

MIT License - See [LICENSE](https://github.com/CoplayDev/unity-mcp/blob/main/LICENSE)
