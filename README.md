> **Status audit (2026-07-04):** General Unity MCP bridge documentation,
> source-refreshed against `MCPForUnity/package.json`,
> `Server/pyproject.toml`, the Python tool registry, Unity-side tool handlers,
> current client-config/server-launch builders, Dockerfile, telemetry source,
> and dev docs. This is not CE-specific Builder control-surface authority.
> Python server tests passed with `uv run --extra dev python -m pytest tests/ -q`
> (94 passed, 2 skipped, 7 xpassed). A local FastMCP HTTP smoke with Unity
> startup skipped proved `/health`, tools/list, resources/list,
> resource-template list, `debug_request_context`, and
> `manage_editor telemetry_status` with telemetry disabled. Unity/client/Docker
> runtime smoke tests, stdio MCP client smoke, Unity-attached tool execution,
> clean-worktree proof, remote proof, and release proof were not run.

<img width="676" height="380" alt="MCP for Unity" src="docs/images/logo.png" />

| [English](README.md) | [简体中文](README-zh.md) |
|----------------------|---------------------------------|

#### Proudly sponsored and maintained by [Coplay](https://www.coplay.dev/?ref=unity-mcp) -- the best AI assistant for Unity.

[![Discord](https://img.shields.io/badge/discord-join-red.svg?logo=discord&logoColor=white)](https://discord.gg/y4p8KfzrN4)
[![](https://img.shields.io/badge/Website-Visit-purple)](https://www.coplay.dev/?ref=unity-mcp)
[![](https://img.shields.io/badge/Unity-000000?style=flat&logo=unity&logoColor=blue 'Unity')](https://unity.com/releases/editor/archive)
[![python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![](https://badge.mcpx.dev?status=on 'MCP Enabled')](https://modelcontextprotocol.io/introduction)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/CoplayDev/unity-mcp)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/CoplayDev/unity-mcp)
[![](https://img.shields.io/badge/License-MIT-red.svg 'MIT License')](https://opensource.org/licenses/MIT)

**Create your Unity apps with LLMs!**

MCP for Unity acts as a bridge, allowing AI assistants (Claude, Cursor, Antigravity, VS Code, etc) to interact directly with your Unity Editor via a local **MCP (Model Context Protocol) Client**. Give your LLM tools to manage assets, control scenes, edit scripts, and automate tasks within Unity.

<img width="406" height="704" alt="MCP for Unity screenshot" src="docs/images/unity-mcp-ui-v8.6.png">

---

### 💬 Join Our [Discord](https://discord.gg/y4p8KfzrN4)

**Get help, share ideas, and collaborate with other MCP for Unity developers!**  

---

## Key Features 🚀

* **🗣️ Natural Language Control:** Instruct your LLM to perform Unity tasks.
* **🛠️ Powerful Tools:** Manage assets, scenes, materials, scripts, and editor functions.
* **🤖 Automation:** Automate repetitive Unity workflows.
* **🧩 Extensible:** Designed to work with various MCP Clients.
* **🌐 HTTP-First Transport:** Ships with HTTP connections enabled by default (stdio is still available as a fallback).

<details open>
  <summary><strong>Tools</strong></summary>

  Your LLM can use functions like:

* `manage_asset`: Performs asset operations (import, create, modify, delete, etc.).
* `manage_editor`: Controls and queries the editor's state and settings.
* `manage_gameobject`: Manages GameObjects: create, modify, delete, find, and component operations.
* `manage_material`: Manages materials: create, set properties, colors, assign to renderers, and query material info.
* `manage_prefabs`: Performs prefab operations (create, modify, delete, etc.).
* `manage_scene`: Manages scenes (load, save, create, get hierarchy, etc.).
* `manage_script`: Compatibility router for legacy script operations (create, read, delete). Prefer `apply_text_edits` or `script_apply_edits` for edits.
* `manage_script_capabilities`: Reports supported script edit operations, text edit operations, payload limits, and guard behavior.
* `manage_scriptable_object`: Creates and modifies ScriptableObject assets using Unity SerializedObject property paths.
* `manage_shader`: Performs shader CRUD operations (create, read, modify, delete).
* `read_console`: Gets messages from or clears the console.
* `refresh_unity`: Requests an AssetDatabase refresh and optional script compilation, with an optional readiness wait.
* `run_tests_async`: Starts tests asynchronously and returns a job_id for polling (preferred).
* `get_test_job`: Polls an async test job for progress and results.
* `run_tests`: Runs tests synchronously (blocks until complete; prefer `run_tests_async` for long suites).
* `execute_custom_tool`: Execute a project-scoped custom tool registered by Unity.
* `execute_menu_item`: Executes Unity Editor menu items (e.g., "File/Save Project").
* `set_active_instance`: Routes subsequent tool calls to a specific Unity instance (when multiple are running). Requires the exact `Name@hash` from `unity_instances`.
* `batch_execute`: Runs a bounded list of MCP tool calls as one batch through Unity.
* `get_performance_stats`: Gets Unity Editor performance marker summaries, details, or spike-only reports.
* `apply_text_edits`: Precise text edits with precondition hashes and atomic multi-edit batches.
* `script_apply_edits`: Structured C# method/class edits (insert/replace/delete) with safer boundaries.
* `validate_script`: Fast validation (basic/standard) to catch syntax/structure issues before/after writes.
* `create_script`: Create a new C# script at the given project path.
* `delete_script`: Delete a C# script by URI or Assets-relative path.
* `find_in_file`: Searches a Unity-readable file with a regex pattern and returns line numbers and excerpts.
* `get_sha`: Get SHA256 and basic metadata for a Unity C# script without returning file contents.
* `debug_request_context`: Returns FastMCP request/session context diagnostics for routing/debugging.
</details>


<details open>
  <summary><strong>Resources</strong></summary>

  Your LLM can retrieve the following resources:

* `custom_tools`: Lists custom tools available for the active Unity project.
* `unity_instances`: Lists running Unity Editor instances. HTTP entries include `id`, `name`, `hash`, `unity_version`, `connected_at`, and `session_id`; stdio entries also include `path`, `port`, `status`, and `last_heartbeat`.
* `menu_items`: Retrieves all available menu items in the Unity Editor.
* `get_tests`: Retrieves all available tests in the Unity Editor.
* `get_tests_for_mode`: Retrieves tests for a specific mode (e.g., "EditMode", "PlayMode").
* `editor_active_tool`: Currently active editor tool (Move, Rotate, Scale, etc.) and transform handle settings.
* `editor_prefab_stage`: Current prefab editing context if a prefab is open in isolation mode.
* `editor_selection`: Detailed information about currently selected objects in the editor.
* `editor_state`: Current editor runtime state including play mode, compilation status, active scene, and selection summary.
* `editor_state_v2`: Canonical editor readiness snapshot with advice and server-computed staleness.
* `editor_windows`: All currently open editor windows with their titles, types, positions, and focus state.
* `project_info`: Static project information including root path, Unity version, and platform.
* `project_layers`: All layers defined in the project's TagManager with their indices (0-31).
* `project_tags`: All tags defined in the project's TagManager.
</details>
---

## How It Works 

MCP for Unity connects your tools using two components:

1. **MCP for Unity Bridge:** A Unity package running inside the Editor. (Installed via Package Manager).
2. **MCP for Unity Server:** A Python server that runs locally (from a terminal window) and speaks HTTP/JSON-RPC to your MCP client. The Unity window launches it for you in HTTP mode by default; stdio is still available if you switch transports.

<img width="562" height="121" alt="image" src="https://github.com/user-attachments/assets/9abf9c66-70d1-4b82-9587-658e0d45dc3e" />

---

## Installation ⚙️

### Prerequisites

  * **Python:** Version 3.10 or newer. [Download Python](https://www.python.org/downloads/)
  * **Unity Hub & Editor:** Version 2021.3 LTS or newer. [Download Unity](https://unity.com/download)
  * **uv (Python toolchain manager):**
      ```bash
      # macOS / Linux
      curl -LsSf https://astral.sh/uv/install.sh | sh

      # Windows (PowerShell)
      winget install --id=astral-sh.uv  -e

      # Docs: https://docs.astral.sh/uv/getting-started/installation/
      ```
      
  * **An MCP Client:** : [Claude Desktop](https://claude.ai/download) | [Claude Code](https://github.com/anthropics/claude-code) | [Cursor](https://www.cursor.com/en/downloads) | [Visual Studio Code Copilot](https://code.visualstudio.com/docs/copilot/overview) | [Windsurf](https://windsurf.com) | Others work with manual config

 *  <details> <summary><strong>[Optional] Roslyn for Advanced Script Validation</strong></summary>

        For **Strict** validation level that catches undefined namespaces, types, and methods: 

        **Method 1: NuGet for Unity (Recommended)**
        1. Install [NuGetForUnity](https://github.com/GlitchEnzo/NuGetForUnity)
        2. Go to `Window > NuGet Package Manager`
        3. Search for `Microsoft.CodeAnalysis`, select version 4.14.0, and install the package
        4. Also install package `SQLitePCLRaw.core` and `SQLitePCLRaw.bundle_e_sqlite3`.
        5. Go to `Player Settings > Scripting Define Symbols`
        6. Add `USE_ROSLYN`
        7. Restart Unity

        **Method 2: Manual DLL Installation**
        1. Download Microsoft.CodeAnalysis.CSharp.dll and dependencies from [NuGet](https://www.nuget.org/packages/Microsoft.CodeAnalysis.CSharp/)
        2. Place DLLs in `Assets/Plugins/` folder
        3. Ensure .NET compatibility settings are correct
        4. Add `USE_ROSLYN` to Scripting Define Symbols
        5. Restart Unity

        **Note:** Without Roslyn, script validation falls back to basic structural checks. Roslyn enables full C# compiler diagnostics with precise error reporting.</details>

---
### 🌟 Step 1: Install the Unity Package

#### To install via Git URL

1. Open your Unity project.
2. Go to `Window > Package Manager`.
3. Click `+` -> `Add package from git URL...`.
4. Enter:
    ```
    https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity
    ```
5. Click `Add`.

**Need a stable/fixed version?** Use a tagged URL instead (updates require uninstalling and re-installing):
```
https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#v8.7.0
```

#### To install via OpenUPM

1. Install the [OpenUPM CLI](https://openupm.com/docs/getting-started-cli.html)
2. Open a terminal (PowerShell, Terminal, etc.) and navigate to your Unity project directory
3. Run `openupm add com.coplaydev.unity-mcp`

**Note:** If you installed the MCP Server before Coplay's maintenance, you will need to uninstall the old package before re-installing the new one.

### ⚡️ Step 2: Start the Local HTTP Server (Default)

HTTP transport is enabled out of the box. The Unity window can launch the FastMCP server for you:

1. Open `Window > MCP For Unity > Toggle MCP Window`.
2. Make sure the **Transport** dropdown is set to `HTTP Local` (default) and the **HTTP URL** is what you want (defaults to `http://localhost:8080`).
3. Click **Start Server**. Unity shows the core `uvx --from ... mcp-for-unity --transport http --http-url <url>` command and, when it owns the local launch, appends lifecycle args such as `--pidfile <path>` and `--unity-instance-token <token>` before opening the operating-system terminal.
4. Keep that terminal window open while you work; closing it stops the server. Use the **Stop Server** button in the Unity window if you need to tear it down cleanly.

> Prefer stdio? Change the transport dropdown to `Stdio` and Unity will fall back to the embedded TCP bridge instead of launching the HTTP server.

**Manual launch (optional)**

You can also start the server yourself from a terminal—useful for CI or when you want to see raw logs:

```bash
uvx --from "git+https://github.com/CoplayDev/unity-mcp@v8.7.0#subdirectory=Server" mcp-for-unity --transport http --http-url http://localhost:8080
```

Keep the process running while clients are connected.

### 🛠️ Step 3: Configure Your MCP Client
Connect your MCP Client to the HTTP server from Step 2 (auto) or via Manual Configuration (below). Claude Desktop and Cherry Studio are current non-HTTP exceptions in source: Claude Desktop supports stdio only, and Cherry Studio uses manual UI configuration with stdio values, so switch the transport dropdown to `Stdio` before configuring either one.

For **Claude Desktop** users, try using our manually curated Unity_Skills by downloading and uploading the claude_skill_unity.zip following this [link](https://www.claude.com/blog/skills).

**Option A: Configure Buttons (recommended for source-registered clients)**

1. In Unity, go to `Window > MCP For Unity > Toggle MCP Window`.
2. Select your Client/IDE from the dropdown.
3. Click the `Configure` Button.  (Or the `Configure All Detected Clients` button will try to configure every client it finds, but takes longer.)
4. Look for the green status dot and `Configured` / `Connected` status text. For HTTP-capable clients this writes the HTTP `url` pointing at the server you launched in Step 2. For Claude Desktop and Cherry Studio, switch to `Stdio` first; their configurators refuse HTTP.

The Client Configuration dropdown is source-populated from registered
configurators. Current source includes Antigravity, Cherry Studio, Claude Code,
Claude Desktop, CodeBuddy CLI, Codex, Cursor, Kilo Code, Kiro, Rider GitHub
Copilot, Trae, VSCode GitHub Copilot, VSCode Insiders GitHub Copilot, and
Windsurf.

<details><summary><strong>Client-specific troubleshooting</strong></summary>

  - **VSCode**: uses `Code/User/mcp.json` with top-level `servers.unityMCP`, `"type": "http"`, and the URL from Step 2. On Windows, MCP for Unity resolves and stores an absolute `uvx.exe` path when you switch back to stdio.
  - **Cursor / Windsurf** [(**help link**)](https://github.com/CoplayDev/unity-mcp/wiki/1.-Fix-Unity-MCP-and-Cursor,-VSCode-&-Windsurf): if the resolved uv/uvx path is missing or wrong, open Settings -> Advanced Settings and use the `UV Path:` row's `Browse` button. The file dialog title is `Select uv Executable`.
  - **Claude Code** [(**help link**)](https://github.com/CoplayDev/unity-mcp/wiki/2.-Fix-Unity-MCP-and-Claude-Code): the Client Configuration section shows `Claude CLI Path:`. If it is missing, the field says `Not found - click Browse to select`; use `Browse` to open the `Select Claude CLI` file dialog. Unregister now updates the UI immediately.
  - **Claude Desktop**: does not support HTTP transport in this plugin. Switch the Unity transport dropdown to `Stdio`, then use `Configure` or the stdio JSON snippet below.
  - **Cherry Studio**: does not support HTTP transport in this plugin and does not auto-write config files. Switch to `Stdio`, then use the manual snippet values in Cherry Studio's Settings -> MCP Server UI.</details>


**Option B: Manual Configuration**

If Configure fails or you use a different client:

1. **Find your MCP Client's configuration file.** (Check client documentation).
    * *Claude Example (macOS):* `~/Library/Application Support/Claude/claude_desktop_config.json`
    * *Claude Example (Windows):* `%APPDATA%\Claude\claude_desktop_config.json`
2. **Edit the file** to add/update the `mcpServers` section. Use HTTP snippets for HTTP-capable clients; use stdio for Claude Desktop and Cherry Studio.

<details>
<summary><strong>Click for Client-Specific JSON Configuration Snippets...</strong></summary>

  ---
**Claude Code**

If you're using Claude Code, you can register the MCP server using the below commands:

**HTTP default:**

```bash
claude mcp add --transport http UnityMCP http://localhost:8080/mcp
```

The Unity window stores a base HTTP URL such as `http://localhost:8080`; MCP
client configs use that base plus `/mcp`.

**VSCode (all OS – HTTP default)**

```json
{
  "servers": {
    "unityMCP": {
      "type": "http",
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

**macOS / Windows / Linux (Cursor and other JSON clients that use `url`)**

```json
{
  "mcpServers": {
    "unityMCP": {
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

**Windsurf / Antigravity (HTTP)**

```json
{
  "mcpServers": {
    "unityMCP": {
      "serverUrl": "http://localhost:8080/mcp",
      "disabled": false
    }
  }
}
```

Set the client URL to the Unity window's base URL plus `/mcp`.

#### Stdio configuration examples (legacy / optional)

Switch the Unity transport dropdown to `Stdio`, then use one of the following `command`/`args` blocks. Current generated JSON/TOML stdio configs use `uvx --from <server-source> mcp-for-unity --transport stdio`; the generated Claude Code CLI omits the trailing server-side flag and relies on the server's default stdio transport. They no longer point at a local `server.py` file. Claude Desktop and Cherry Studio must use this mode; Cherry Studio expects the command and args copied into its Settings -> MCP Server UI rather than written to a JSON file by the configurator.

**Claude Code (stdio)**

```bash
claude mcp add --transport stdio UnityMCP -- uvx --from "git+https://github.com/CoplayDev/unity-mcp@v8.7.0#subdirectory=Server" mcp-for-unity
```

**VSCode (stdio JSON shape)**

```json
{
  "servers": {
    "unityMCP": {
      "type": "stdio",
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

**Claude Desktop / macOS / Linux (stdio)**

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

**Windows (stdio)**

```json
{
  "mcpServers": {
    "unityMCP": {
      "command": "C:/Users/YOUR_USERNAME/AppData/Local/Microsoft/WinGet/Links/uvx.exe",
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

Replace absolute `uvx` paths as needed for your platform, or use the snippet copied from the Unity window.

</details>

---

## Usage ▶️

1. **Open your Unity Project**, open `Window > MCP For Unity > Toggle MCP Window`, and verify the HTTP server is running after you click **Start Server**. The indicator should show "Session Active" once the server is up.
    
2. **Start your HTTP-capable MCP client** (Cursor, VS Code, Windsurf, Claude Code, etc.). It connects to the HTTP endpoint configured in Step 3; Claude Desktop and Cherry Studio use the stdio configuration above.
    
3. **Interact!** Unity tools should now be available in your MCP Client.

    Example Prompt: `Create a 3D player controller`, `Create a tic-tac-toe game in 3D`, `Create a cool shader and apply to a cube`.

### Working with Multiple Unity Instances

MCP for Unity supports multiple Unity Editor instances simultaneously. Each instance is isolated per MCP client session.

**To direct tool calls to a specific instance:**

1. List available instances: Ask your LLM to check the `unity_instances` resource
2. Set the active instance: Use `set_active_instance` with the exact `Name@hash` shown (e.g., `MyProject@abc123`)
3. All subsequent tools route to that instance until changed. If multiple instances are running and no active instance is set, the server will error and instruct you to select one.

**Example:**
```
User: "List all Unity instances"
LLM: [Shows ProjectA@abc123 and ProjectB@def456]

User: "Set active instance to ProjectA@abc123"
LLM: [Calls set_active_instance("ProjectA@abc123")]

User: "Create a red cube"
LLM: [Creates cube in ProjectA]
```

---

## Development & Contributing 🛠️

### Development Setup and Guidelines

See [README-DEV.md](docs/README-DEV.md) for complete development setup and workflow documentation.

### Adding Custom Tools

MCP for Unity uses a Python MCP Server tied with Unity's C# scripts for tools. If you'd like to extend the functionality with your own tools, learn how to do so in **[CUSTOM_TOOLS.md](docs/CUSTOM_TOOLS.md)**.

### How to Contribute

1. **Fork** the main repository.
2. **Create an issue** to discuss your idea or bug.
3. **Create a branch** (`feature/your-idea` or `bugfix/your-fix`).
4. **Make changes.**
5. **Commit** (feat: Add cool new feature).
6. **Push** your branch.
7. **Open a Pull Request** against the main branch, referencing the issue you created earlier.

---

## 📊 Telemetry & Privacy

MCP for Unity includes **privacy-focused, anonymous telemetry** to help us improve the product. We collect usage analytics and performance data, but **never** your code, project names, or personal information.

- **🔒 Anonymous**: Random UUIDs only, no personal data
- **🚫 Easy opt-out**: Set `DISABLE_TELEMETRY=true` before launching the server,
  or use the Unity EditorPrefs opt-out path
- **📖 Transparent**: See [TELEMETRY.md](docs/TELEMETRY.md) for full details

Your privacy matters to us. All telemetry is optional and designed to respect your workflow.

---

## Troubleshooting ❓

<details>  
<summary><strong>Click to view common issues and fixes...</strong></summary>  

- **Unity Bridge Not Running/Connecting:**
    - Ensure Unity Editor is open.
    - Check the status window: `Window > MCP For Unity > Toggle MCP Window`.
    - Restart Unity.
- **MCP Client Not Connecting / Server Not Starting:**
    - Make sure the local HTTP server is running from the MCP window after `Window > MCP For Unity > Toggle MCP Window` and **Start Server**. Keep the spawned terminal window open.
    - **Verify HTTP URL:** Ensure the client config points at the Unity window's HTTP URL plus `/mcp` (default `http://localhost:8080/mcp`).
    - **Verify uv/uvx:** Make sure `uv` and `uvx` are installed and working (`uv --version` and `uvx --version`).
    - **Run Manually:** Try running the server directly from the terminal to see errors: 
      ```bash
      uvx --from "git+https://github.com/CoplayDev/unity-mcp@v8.7.0#subdirectory=Server" mcp-for-unity --transport http --http-url http://localhost:8080
      ```
- **Configuration Failed:**
    - Use the Manual Configuration steps. The plugin may lack permissions to write to the MCP client's config file.

</details>  

Still stuck? [Open an Issue](https://github.com/CoplayDev/unity-mcp/issues) or [Join the Discord](https://discord.gg/y4p8KfzrN4)!

---

## License 📜

MIT License. See [LICENSE](LICENSE) file.

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=CoplayDev/unity-mcp&type=Date)](https://www.star-history.com/#CoplayDev/unity-mcp&Date)

## Unity AI Tools by Coplay

Coplay offers 2 AI tools for Unity
- **MCP for Unity** is available freely under the MIT license.
- **Coplay** is a premium Unity AI assistant that sits within Unity and is more than the MCP for Unity.

(These tools have different tech stacks. See this blog post [comparing Coplay to MCP for Unity](https://www.coplay.dev/blog/comparing-coplay-and-unity-mcp).)

<img alt="Coplay" src="docs/images/coplay-logo.png" />

## Disclaimer

This project is a free and open-source tool for the Unity Editor, and is not affiliated with Unity Technologies.
