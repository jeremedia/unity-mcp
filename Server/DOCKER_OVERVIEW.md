# MCP for Unity Server (Docker Image)

> **Status audit (2026-07-04):** General Unity MCP bridge Docker
> documentation, not CE-specific control-surface authority. Source-refreshed
> against `Server/Dockerfile`, which starts the server in HTTP mode on
> `0.0.0.0:8080` when built from the repository root with
> `-f Server/Dockerfile`. `docker-compose.yml` uses the same repository-root
> context, `Server/Dockerfile`, `8080:8080` port mapping, and HTTP
> `0.0.0.0:8080` command. `Server/pyproject.toml` and `Server/uv.lock` both
> record `8.7.0`; Python server tests passed with 94 passed, 2 skipped, and
> 7 xpassed. A separate non-Docker local FastMCP HTTP smoke proved server
> `/health`, tools/list, resources/list, one resource template,
> `debug_request_context`, and `manage_editor telemetry_status` with Unity
> startup skipped and telemetry disabled. This slice did not pull the published
> image, build the image, run Docker Compose, or run a Docker smoke test.

[![MCP](https://badge.mcpx.dev?status=on 'MCP Enabled')](https://modelcontextprotocol.io/introduction)
[![License](https://img.shields.io/badge/License-MIT-red.svg 'MIT License')](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/badge/discord-join-red.svg?logo=discord&logoColor=white)](https://discord.gg/y4p8KfzrN4)

Model Context Protocol server for Unity Editor integration. Control Unity through natural language using AI assistants like Claude, Cursor, and more.

**Maintained by [Coplay](https://www.coplay.dev/?ref=unity-mcp)** - This project is not affiliated with Unity Technologies.

💬 **Join our community:** [Discord Server](https://discord.gg/y4p8KfzrN4)

**Required:** Install the [Unity MCP Plugin](https://github.com/CoplayDev/unity-mcp?tab=readme-ov-file#-step-1-install-the-unity-package) to connect Unity Editor with this MCP server.

---

## Quick Start

### 1. Pull the image

```bash
docker pull msanatan/mcp-for-unity-server:latest
```

### 2. Run the server

```bash
docker run -p 8080:8080 msanatan/mcp-for-unity-server:latest
```

This starts the MCP server on port 8080. The checked-in Dockerfile uses
`uv run python src/main.py --transport http --http-host 0.0.0.0 --http-port
8080` as its default command.

Source caveat: Docker builds from this checkout use the frozen `uv.lock`, and
the editable `mcpforunityserver` entry now matches `pyproject.toml` at
`8.7.0`. Run a fresh build and container smoke test before treating the Docker
image as verified-current.

The checked-in `docker-compose.yml` builds from repository root with
`dockerfile: Server/Dockerfile`, maps `8080:8080`, sets
`PYTHONPATH=/app/Server/src`, and runs the same HTTP command. This compose path
was source-checked only; no compose smoke was run in this slice.

### 3. Configure your MCP Client

Add the following configuration to an HTTP-capable MCP client (for example,
Cursor settings). Claude Desktop and Cherry Studio are non-HTTP exceptions in
the current Unity plugin configurators and cannot use this HTTP Docker endpoint
directly.

```json
{
  "mcpServers": {
    "unityMCP": {
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

---

## Configuration

The server container alone is not enough for Unity tool execution. In HTTP
mode, the Unity package must connect a session to the same base URL; MCP
clients use `<base>/mcp`, while the Unity plugin opens the WebSocket session at
`<base>/hub/plugin`. For a Docker server, configure the Unity window to use the
container's base URL and start the Unity session.

**Environment Variables:**

- `UNITY_MCP_DEFAULT_INSTANCE` - Default Unity instance to target.
- `UNITY_MCP_SKIP_STARTUP_CONNECT` - Skip initial Unity connection attempt
  (`1`, `true`, `yes`, or `on`).
- `UNITY_MCP_TRANSPORT` - Transport protocol (`stdio` or `http`). The Docker
  image command already starts HTTP mode.
- `UNITY_MCP_HTTP_URL` - HTTP server URL; currently this can override
  `--http-url`.
- `UNITY_MCP_HTTP_HOST` / `UNITY_MCP_HTTP_PORT` - HTTP host/port; explicit
  CLI host/port args override these.
- `UNITY_MCP_TELEMETRY_ENDPOINT` / `UNITY_MCP_TELEMETRY_TIMEOUT` - Telemetry
  endpoint and timeout controls.
- `UNITY_MCP_TELEMETRY_ENABLED` - Listed in server help as an enable flag;
  current runtime opt-out checks are the disable aliases below.
- `DISABLE_TELEMETRY=true`, `UNITY_MCP_DISABLE_TELEMETRY=true`, or
  `MCP_DISABLE_TELEMETRY=true` - Opt out of anonymous usage analytics.

Example running with environment variables:

```bash
docker run -p 8080:8080 -e DISABLE_TELEMETRY=true msanatan/mcp-for-unity-server:latest
```

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

For complete documentation, troubleshooting, and advanced usage, please visit the GitHub repository:

📖 **[Full Documentation](https://github.com/CoplayDev/unity-mcp#readme)**

---

## License

MIT License - See [LICENSE](https://github.com/CoplayDev/unity-mcp/blob/main/LICENSE)
