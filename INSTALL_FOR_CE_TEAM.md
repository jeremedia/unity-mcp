# CE Unity MCP Installation Guide for Team

## 🎯 What This Gives You

Once installed, you can control Unity with natural language commands like:
- "Create a 30x40 foot gallery with white walls"
- "Place three pedestals in the center"
- "Extract the control surface from OK_Floor_Pedestal_Builder"

## 📋 Prerequisites

1. **Unity 6000.1.5f1** (or your CE project version)
2. **Python 3.12+** with `uv` installed:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **MCP Client** (Claude Code recommended)
4. **GitHub access** to https://github.com/jeremedia/unity-mcp

## 🚀 Step-by-Step Installation

### Step 1: Install Unity Package

1. Open your CE Unity project
2. Open **Window > Package Manager**
3. Click the **+** button (top left)
4. Select **Add package from git URL...**
5. Paste this exact URL:
   ```
   https://github.com/jeremedia/unity-mcp.git?path=/UnityMcpBridge#v3.4.0-ce.1
   ```
6. Click **Add**
7. Wait for Unity to download and compile (30-60 seconds)

✅ **Success Check**: You should see "MCP for Unity - Curation Engine Edition" in your Package Manager

### Step 2: Start Unity MCP Bridge

1. In Unity, go to **Window > MCP for Unity**
2. The window should show:
   - Unity Bridge Status: 🟢 Running
   - A port number (e.g., 5000)
3. If you see red status, click **Start Bridge**

### Step 3: Install Python Server

The Unity package tries to auto-install. If that fails:

**macOS:**
```bash
cd ~/Library/Application\ Support/UnityMCP/UnityMcpServer
uv sync
uv run start-server  # Test it works
```

**Windows:**
```bash
cd %LOCALAPPDATA%\UnityMCP\UnityMcpServer
uv sync
uv run start-server  # Test it works
```

### Step 4: Configure Claude Code (Recommended)

From your CE project directory:

**macOS:**
```bash
claude mcp add unity-mcp-ce -- uv --directory ~/Library/Application\ Support/UnityMCP/UnityMcpServer/src run server.py
```

**Windows:**
```bash
claude mcp add unity-mcp-ce -- uv --directory "%LOCALAPPDATA%\UnityMCP\UnityMcpServer\src" run server.py
```

Then restart Claude Code.

### Step 5: Verify Installation

Ask Claude Code to:
1. "List available MCP tools" - Should show CE tools like `place_room`
2. "What CE builders are in the current scene?" - Should detect OK_*_Builder components
3. "Create a test room" - Should create a room in Unity

## 🎨 Using CE MCP Features

### Natural Language Commands

```python
# In Claude Code, you can say:
"Create a 30x40 foot gallery with white walls and track lighting"

# Claude will use:
await mcp.call_tool(
    "create_exhibition_space",
    {"description": "30x40 gallery with white walls and track lighting"}
)
```

### Extract Control Surfaces

```python
# Ask Claude:
"Extract the control surface from the Floor Pedestal Builder"

# Claude will use:
await mcp.call_tool(
    "get_builder_control_surface",
    {"target": "FloorPedestal", "search_method": "by_name"}
)
```

### Available CE Tools

- `place_room` - Create exhibition spaces
- `place_floor_pedestal` - Add display pedestals
- `mount_artwork` - Mount art on walls
- `configure_lighting` - Setup gallery lighting
- `create_exhibition_space` - Natural language curation
- `get_builder_control_surface` - Extract Odin interfaces
- `invoke_builder_method` - Call Builder methods

## 🔧 Troubleshooting

### "Unity MCP not connected"
1. Check Unity MCP window (Window > MCP for Unity)
2. Click **Start Bridge** if status is red
3. Try **Auto-Setup** button

### "Can't find CE tools"
1. Verify you installed the CE version (not standard unity-mcp)
2. Check package.json shows `com.curationengine.unity-mcp-ce`
3. Restart Claude Code after configuration

### "Python server not starting"
1. Ensure `uv` is installed: `uv --version`
2. Check Python version: `python --version` (needs 3.12+)
3. Try manual server start to see errors

### "Can't create GameObjects"
1. Unity must be in Play mode or have a scene open
2. Check Unity console for errors
3. Ensure CE project has all required assemblies

## 📦 Updating to Latest Version

### To Update Unity Package:
1. Open Package Manager
2. Find "MCP for Unity - Curation Engine Edition"
3. Click **Remove**
4. Re-add with latest URL:
   ```
   https://github.com/jeremedia/unity-mcp.git?path=/UnityMcpBridge#ce-builder-integration
   ```

### To Update Python Server:
```bash
cd ~/Library/Application\ Support/UnityMCP/UnityMcpServer  # or Windows equivalent
git pull
uv sync
```

## 🔄 Syncing with Upstream

We periodically merge improvements from CoplayDev/unity-mcp:

```bash
# For maintainers only
git fetch upstream
git merge upstream/main
# Resolve conflicts favoring CE additions
git push origin ce-builder-integration
```

## 📝 Version History

- **v3.4.0-ce.1** (2025-09-22) - Initial CE release with Odin extraction
- Future versions will follow semantic versioning: `vX.Y.Z-ce.N`

## 🆘 Getting Help

1. **CE Team Slack**: #unity-mcp channel
2. **GitHub Issues**: https://github.com/jeremedia/unity-mcp/issues
3. **Upstream Issues**: https://github.com/CoplayDev/unity-mcp (for non-CE bugs)

## ✅ Installation Checklist

- [ ] Unity Package installed (shows in Package Manager)
- [ ] Unity MCP Bridge running (green status)
- [ ] Python server installed (`uv sync` completed)
- [ ] Claude Code configured (MCP added)
- [ ] Claude Code restarted
- [ ] CE tools available (test with "List MCP tools")
- [ ] Can create GameObjects (test with "Create a room")
- [ ] Can extract control surfaces (test with any Builder)

## 🎉 Success!

If all checks pass, you're ready to create exhibitions with natural language!

Try: "Create a modern art gallery with three pedestals and dramatic lighting"