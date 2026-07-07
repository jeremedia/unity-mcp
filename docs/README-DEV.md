# MCP for Unity Development Tools

> **Status audit (2026-07-04):** General Unity MCP development guide,
> source-refreshed against `Server/pyproject.toml`, current Advanced Settings
> UI, and checked-in dev scripts. This is not CE-specific control-surface
> authority. `uv run --extra dev python -m pytest tests/ -q` passed with
> 94 passed, 2 skipped, and 7 xpassed; a local FastMCP HTTP smoke proved the
> Python server endpoint with Unity startup skipped. Unity tests, CI, stdio MCP
> client smoke, Docker smoke, and Unity-attached tool execution were not run.

| [English](README-DEV.md) | [简体中文](README-DEV-zh.md) |
|---------------------------|------------------------------|

Welcome to the MCP for Unity development environment! This directory contains tools and utilities to streamline MCP for Unity core development.

## 🛠️ Development Setup

### Installing Development Dependencies

To contribute or run tests, you need to install the development dependencies using `uv`:

```bash
# Navigate to the server source directory
cd Server

# Install the package in editable mode with dev dependencies
uv pip install -e ".[dev]"
```

This installs:

- **Runtime dependencies**: `httpx`, `fastmcp`, `mcp`, `pydantic`, `tomli`, `fastapi`, `uvicorn`
- **Development dependencies**: `pytest`, `pytest-asyncio`

### Running Tests

```bash
# From the server source directory
cd Server
uv run --extra dev python -m pytest tests/ -q
```

Or from the repo root:

```bash
# Using uv from the server directory
cd Server && uv run --extra dev python -m pytest tests/ -q
```

To run the current integration test tree:
```bash
uv run --extra dev python -m pytest tests/integration/ -q
```

`Server/tests/pytest.ini` defines both `integration` and `unit` markers, but
the current documented integration tree is selected by path. Use file, test, or
marker selection only after confirming the target tests are annotated as needed.

## 🚀 Available Development Features

### ✅ Source-backed development features

- **Development Deployment Scripts**: Quick deployment and restore scripts for MCP for Unity core changes.
- **Development Mode Toggle**: Now exposed through Advanced Settings as `Force fresh server install`.
- **Script editing, validation, and runtime compilation**:
  `apply_text_edits`, `script_apply_edits`, and `validate_script` are
  source-backed. The project-scoped `runtime_compilation` custom tool source
  exists under `CustomTools/RoslynRuntimeCompilation/` and is gated by
  `USE_ROSLYN`; Unity import/runtime proof was not run in this slice.
- **Plugin Development Kit**: Covered by project-scoped Custom Tools.
- **Automated Tests**: Python tests live under `Server/tests/`; Unity/CI guidance is documented later in this file.

### 🔄 Still planned or separately verified

- **Debug Dashboard**: Advanced debugging and monitoring tools remain outside this source-checked slice.

---

## Advanced Settings (Editor Window)

Use the MCP for Unity Editor window (`Window > MCP For Unity > Toggle MCP Window`) and open **Advanced Settings** inside the Settings tab to override tooling and deploy local code during development.

![Advanced Settings](./images/advanced-setting.png)


- **UV/UVX Path Override**: Point the UI to a specific `uv`/`uvx` executable (e.g., from a custom install) when PATH resolution is wrong. Clear to fall back to auto-discovery.
- **Server Source Override**: Set a local folder or git URL for the Python server (`uvx --from <url> mcp-for-unity`). Clear to use the packaged default.
- **Dev Mode (Force fresh server install)**: When enabled, generated `uvx` commands add `--no-cache --refresh` before launching. This is slower, but avoids accidentally running a stale cached build while iterating on `Server/`.
- **Local Package Deployment**: Pick a local `MCPForUnity` folder (must contain `Editor/` and `Runtime/`) and click **Deploy to Project** to copy it over the currently installed package path (from `Packages/manifest.json` / Package Manager). A timestamped backup is stored under `Library/MCPForUnityDeployBackups`, and **Restore Last Backup** reverts the last deploy.

Tips:
- After deploy/restore, Unity will refresh scripts automatically; if in doubt, re-open the MCP window and confirm the target path label in Advanced Settings.
- Keep the source and target distinct (don’t point the source at the already-installed `PackageCache` folder).
- Use git ignored working folders for rapid iteration; the deploy flow copies only `Editor` and `Runtime`.

## Switching MCP package sources quickly

Run this from the unity-mcp repo, not your game's root directory. Use `mcp_source.py` to quickly switch between different MCP for Unity package sources:

**Usage:**

```bash
python mcp_source.py [--manifest /path/to/manifest.json] [--repo /path/to/unity-mcp] [--choice 1|2|3]
```

**Options:**

- **1** Upstream main (CoplayDev/unity-mcp)
- **2** Remote current branch (origin + branch)
- **3** Local workspace (file: MCPForUnity)

After switching, open Package Manager and Refresh to re-resolve packages.

## Development Deployment Scripts

These deployment scripts help you quickly test changes to MCP for Unity core code.

## Scripts

### `deploy-dev.bat`

Deploys your development code to the actual installation locations for testing.

**What it does:**

1. Backs up existing package-cache `Editor/` and `Runtime/` files to a timestamped folder
2. Copies `MCPForUnity/Editor/` to Unity's package cache
3. Copies `MCPForUnity/Runtime/` to Unity's package cache
4. Does not deploy the Python server; the server deploy and server-path prompt are disabled in the current batch file

**Usage:**

1. Run `deploy-dev.bat`
2. Enter Unity package cache path (example provided)
3. Enter backup location (or use default: `%USERPROFILE%\Desktop\unity-mcp-backup`)

**Note:** Dev deploy skips Python server deployment in this checkout. The
server copy block is commented out in `deploy-dev.bat`, so there is no active
server exclude/copy behavior to rely on unless that block is reimplemented.

### `restore-dev.bat`

Restores original files from backup.

**What it does:**

1. Lists available backups with timestamps
2. Allows you to select which backup to restore
3. Restores Unity Bridge `Editor/` and `Runtime/` files when present
4. Prompts for an existing legacy server path before restore; Python Server files are restored only if the selected legacy backup contains a `PythonServer/` folder

### `prune_tool_results.py`

Compacts large `tool_result` blobs in conversation JSON into concise one-line summaries.

**Usage:**

```bash
python3 prune_tool_results.py < reports/claude-execution-output.json > reports/claude-execution-output.pruned.json
```

The script reads a conversation from `stdin` and writes the pruned version to `stdout`, making logs much easier to inspect or archive.

These defaults dramatically cut token usage without affecting essential information.

## Finding Unity Package Cache Path

Unity stores Git packages under a version-or-hash folder. Expect something like:
```
X:\UnityProject\Library\PackageCache\com.coplaydev.unity-mcp@<version-or-hash>
```
Example (hash):
```
X:\UnityProject\Library\PackageCache\com.coplaydev.unity-mcp@272123cfd97e

```

To find it reliably:

1. Open Unity Package Manager
2. Select "MCP for Unity" package
3. Right click the package and choose "Show in Explorer"
4. That opens the exact cache folder Unity is using for your project

Note: In this checkout, `MCPForUnity/` does not contain bundled Python server
sources. The current config builder resolves the server from
`git+https://github.com/CoplayDev/unity-mcp@v<package-version>#subdirectory=Server`
unless you override the source in Advanced Settings.

## Payload sizing & paging defaults (recommended)

Some Unity tool calls can return *very large* JSON payloads (deep hierarchies, components with full serialized properties). To keep MCP responses bounded and avoid Unity freezes/crashes, prefer **paged + summary-first** reads and fetch full properties only when needed.

### `manage_scene(action="get_hierarchy")`

- **Default behavior**: returns a **paged summary** of either root GameObjects (no `parent`) or direct children (`parent` specified). It does **not** inline full recursive subtrees.
- **Paging params**:
  - **`page_size`**: defaults to **50**, clamped to **1..500**
  - **`cursor`**: defaults to **0**
  - **`next_cursor`**: returned as a **string** when more results remain; `null` when complete
- **Other safety knobs**:
  - **`max_nodes`**: defaults to **1000**, clamped to **1..5000**
  - **`include_transform`**: defaults to **false**

### `manage_gameobject(action="get_components")`

- **Default behavior**: returns **paged component metadata** only (`typeName`, `instanceID`).
- **Paging params**:
  - **`page_size`**: defaults to **25**, clamped to **1..200**
  - **`cursor`**: defaults to **0**
  - **`max_components`**: defaults to **50**, clamped to **1..500**
  - **`next_cursor`**: returned as a **string** when more results remain; `null` when complete
- **Properties-on-demand**:
  - **`include_properties`** defaults to **false**
  - When `include_properties=true`, the implementation enforces a conservative response-size budget (roughly **~250KB** of JSON text) and may return fewer than `page_size` items; use `next_cursor` to continue.

### Practical defaults (what we recommend in prompts/tests)

- **Hierarchy roots**: start with `page_size=50` and follow `next_cursor` (usually 1–2 calls for big scenes).
- **Children**: page by `parent` with `page_size=10..50` (depending on expected breadth).
- **Components**:
  - Start with `include_properties=false` and `page_size=10..25`
  - When you need full properties, keep `include_properties=true` with a **small** `page_size` (e.g. **3..10**) to bound peak payload sizes.

## MCP Bridge Stress Test

An on-demand stress utility exercises the MCP bridge with multiple concurrent clients while triggering real script reloads via immediate script edits (no menu calls required).

### Script

- `tools/stress_mcp.py`

### What it does

- Starts N TCP clients against the MCP for Unity bridge (default port auto-discovered from `~/.unity-mcp/unity-mcp-status-*.json`).
- Sends lightweight framed `ping` keepalives to maintain concurrency.
- In parallel, appends a unique marker comment to a target C# file using `manage_script.apply_text_edits` with:
  - `options.refresh = "immediate"` to force an import/compile immediately (triggers domain reload), and
  - `precondition_sha256` computed from the current file contents to avoid drift.
- Uses EOF insertion to avoid header/`using`-guard edits.

### Usage (local)

```bash
# Recommended: use the included large script in the test project
python3 tools/stress_mcp.py \
  --duration 60 \
  --clients 8 \
  --unity-file "TestProjects/UnityMCPTests/Assets/Scripts/LongUnityScriptClaudeTest.cs"
```

### Flags

- `--project` Unity project path (auto-detected to the included test project by default)
- `--unity-file` C# file to edit (defaults to the long test script)
- `--clients` number of concurrent clients (default 10)
- `--duration` seconds to run (default 60)

### Expected outcome

- No Unity Editor crashes during reload churn
- Immediate reloads after each applied edit (no `Assets/Refresh` menu calls)
- Some transient disconnects or a few failed calls may occur during domain reload; the tool retries and continues
- JSON summary printed at the end, e.g.:
  - `{"port": 6400, "stats": {"pings": 28566, "applies": 69, "disconnects": 0, "errors": 0}}`

### Notes and troubleshooting

- Immediate vs debounced:
  - The tool sets `options.refresh = "immediate"` so changes compile instantly. If you only need churn (not per-edit confirmation), switch to debounced to reduce mid-reload failures.
- Precondition required:
  - `apply_text_edits` requires `precondition_sha256` on larger files. The tool reads the file first to compute the SHA.
- Edit location:
  - To avoid header guards or complex ranges, the tool appends a one-line marker at EOF each cycle.
- Read API:
  - The bridge currently supports `manage_script.read` for file reads. You may see a deprecation warning; it's harmless for this internal tool.
- Transient failures:
  - Occasional `apply_errors` often indicate the connection reloaded mid-reply. Edits still typically apply; the loop continues on the next iteration.

### CI guidance

- Keep this out of default PR CI due to Unity/editor requirements and runtime variability.
- Optionally run it as a manual workflow or nightly job on a Unity-capable runner.

## CI Test Workflow (GitHub Actions)

We provide a CI job to run a Natural Language Editing suite against the Unity test project. It spins up a headless Unity container and connects via the MCP bridge. To run from your fork, you need the following GitHub "secrets": an `ANTHROPIC_API_KEY` and Unity credentials (usually `UNITY_EMAIL` + `UNITY_PASSWORD` or `UNITY_LICENSE` / `UNITY_SERIAL`.) These are redacted in logs so never visible.

***To run it***

- Trigger: In GitHub "Actions" for the repo, trigger `workflow dispatch` (`Claude NL/T Full Suite (Unity live)`).
- Image: `UNITY_IMAGE` (UnityCI) pulled by tag; the job resolves a digest at runtime. Logs are sanitized.
- Execution: single pass with immediate per‑test fragment emissions (strict single `<testcase>` per file). A placeholder guard fails fast if any fragment is a bare ID. Staging (`reports/_staging`) is promoted to `reports/` to reduce partial writes.
- Reports: JUnit at `reports/junit-nl-suite.xml`, Markdown at `reports/junit-nl-suite.md`.
- Publishing: JUnit is normalized to `reports/junit-for-actions.xml` and published; artifacts upload all files under `reports/`.

### Test target script

- The repo includes a long, standalone C# script used to exercise larger edits and windows:
  - `TestProjects/UnityMCPTests/Assets/Scripts/LongUnityScriptClaudeTest.cs`
  Use this file locally and in CI to validate multi-edit batches, anchor inserts, and windowed reads on a sizable script.

### Adjust tests / prompts

- Edit `.claude/prompts/nl-unity-suite-t.md` to modify the NL/T steps. Follow the conventions: emit one XML fragment per test under `reports/<TESTID>_results.xml`, each containing exactly one `<testcase>` with a `name` that begins with the test ID. No prologue/epilogue or code fences.
- Keep edits minimal and reversible; include concise evidence.

### Run the suite

1) Push your branch, then manually run the workflow from the Actions tab.
2) The job writes reports into `reports/` and uploads artifacts.
3) The “JUnit Test Report” check summarizes results; open the Job Summary for full markdown.

### View results

- Job Summary: inline markdown summary of the run on the Actions tab in GitHub
- Check: “JUnit Test Report” on the PR/commit.
- Artifacts: `claude-nl-suite-artifacts` includes XML and MD.

### MCP Connection Debugging

- *Enable debug logs* in the MCP for Unity window (inside the Editor) to view connection status, auto-setup results, and MCP client paths. It shows:
  - bridge startup/port, client connections, strict framing negotiation, and parsed frames
  - auto-config path detection (Windows/macOS/Linux), uv/claude resolution, and surfaced errors
- In CI, the job tails Unity logs (redacted for serial/license/password/token) and prints socket/status JSON diagnostics if startup fails.
## Workflow

1. **Make changes** to your source code in this directory
2. **Deploy** using `deploy-dev.bat`
3. **Test** in Unity (restart Unity Editor first)
4. **Iterate** - repeat steps 1-3 as needed
5. **Restore** original files when done using `restore-dev.bat`

## Troubleshooting

### "Path not found" errors running the .bat file

- Verify Unity package cache path is correct
- Check that MCP for Unity package is actually installed
- For `restore-dev.bat` only, the script still validates a legacy server path
  before checking whether the selected backup contains `PythonServer/`. Current
  `deploy-dev.bat` skips Python server deployment and only copies package
  `Editor/` and `Runtime/` files.

### "Permission denied" errors

- Run cmd as Administrator
- Close Unity Editor before deploying
- Close any MCP clients before deploying

### "Backup not found" errors

- Run `deploy-dev.bat` first to create initial backup
- Check backup directory permissions
- Verify backup directory path is correct

### Windows uvx path issues

- On Windows, when testing GUI clients, prefer the WinGet Links `uvx.exe`; if
  multiple `uvx.exe` paths exist, open Settings -> Advanced Settings and use
  the `UV Path:` row's `Browse` button to pin the Links shim stored in
  `MCPForUnity.UvxPath`. The current file dialog title is `Select uv
  Executable`.

### Domain Reload Tests Stall When Unity is Backgrounded

Tests that trigger script compilation mid-run (e.g., `DomainReloadResilienceTests`) may stall when Unity is not the active window. This is an OS-level limitation—macOS throttles background application main threads, preventing compilation from completing.

**Workarounds:**
- Run domain reload tests with Unity foregrounded
- Run them first in the test suite (before backgrounding Unity)
- Use the `[Explicit]` attribute to exclude them from default runs

**Note:** The MCP workflow itself is unaffected—socket messages provide external stimulus that keeps Unity responsive even when backgrounded. This limitation only affects Unity's internal test coroutine waits.
