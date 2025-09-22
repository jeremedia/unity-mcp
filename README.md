# MCP for Unity - Curation Engine Edition 🎨

**Unity MCP enhanced for Curation Engine with Odin Inspector control surface extraction and natural language exhibition creation.**

This is a fork of [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp) with specialized features for Curation Engine (CE) Builders.

## ✨ CE-Specific Features

### 🔍 Odin Inspector Control Surface Extraction
- Automatically detects CE Builders (`OK_*_Builder` pattern)
- Extracts `[ShowInInspector]` properties as controllable surfaces
- Discovers `[Button]` and `[ResponsiveButtonGroup]` methods
- Maps Builder properties to underlying Config paths

### 🎭 Natural Language Exhibition Creation
Transform curator descriptions into exhibition spaces:
```python
await mcp.call_tool(
    "create_exhibition_space",
    {
        "description": "Create a 30x40 foot gallery with white walls, track lighting, and three pedestals"
    }
)
```

### 🛠️ CE-Specific MCP Tools
- **`get_builder_control_surface`** - Extract Odin control interface from any CE Builder
- **`place_room`** - Create exhibition rooms with `OK_Room_Builder`
- **`place_floor_pedestal`** - Position pedestals using `OK_Floor_Pedestal_Builder`
- **`mount_artwork`** - Mount art on walls with frame system
- **`configure_lighting`** - Setup room lighting with `OK_Room_Light_Builder`
- **`create_exhibition_space`** - Natural language exhibition creation
- **`invoke_builder_method`** - Call Builder methods (Draw, Erase, etc.)

## 📦 Installation for Curation Engine

### Prerequisites
- Unity 6000.1.5f1 or compatible (CE requirement)
- Python 3.12+ with `uv` installed
- Curation Engine project
- MCP Client (Claude Code, Cursor, etc.)

### Step 1: Install CE-Enhanced Unity Package

#### Via Unity Package Manager (Recommended)
1. Open your CE Unity project
2. Go to `Window > Package Manager`
3. Click `+` -> `Add package from git URL...`
4. Enter ONE of these URLs:

   **For latest CE features:**
   ```
   https://github.com/jeremedia/unity-mcp.git?path=/UnityMcpBridge#ce-builder-integration
   ```

   **For stable CE release:**
   ```
   https://github.com/jeremedia/unity-mcp.git?path=/UnityMcpBridge#v3.4.0-ce.1
   ```

5. Click `Add`
6. Unity will install the package with CE enhancements

#### Alternative: OpenUPM Installation
```bash
# Coming soon - will be published as com.curationengine.unity-mcp-ce
```

### Step 2: Install Python MCP Server

The Unity package will attempt to auto-install the Python server. If that fails:

```bash
# Manual installation
cd ~/Library/AppSupport/UnityMCP/UnityMcpServer  # macOS
# or
cd %LOCALAPPDATA%\UnityMCP\UnityMcpServer       # Windows

# Install dependencies
uv sync

# Test the server
uv run start-server
```

### Step 3: Configure MCP Client

#### For Claude Code:
```bash
# Run from your CE project directory
claude mcp add unity-mcp-ce -- uv --directory ~/Library/AppSupport/UnityMCP/UnityMcpServer/src run server.py
```

#### For other clients, add to config:
```json
{
  "mcpServers": {
    "unity-mcp-ce": {
      "command": "uv",
      "args": ["--directory", "/path/to/UnityMCP/UnityMcpServer/src", "run", "server.py"]
    }
  }
}
```

### Step 4: Verify CE Features

1. In Unity, go to `Window > MCP for Unity`
2. Check for green connection status
3. Test CE Builder detection:
   - Create a GameObject with any `OK_*_Builder` component
   - Your MCP client should be able to extract its control surface

## 🚀 Usage Examples

### Extract Builder Control Surface
```python
# Get the control interface for a CE Builder
result = await mcp.call_tool(
    "get_builder_control_surface",
    {
        "target": "MyGalleryRoom",
        "search_method": "by_name"
    }
)

# Result contains Odin-attributed properties and methods
print(f"Properties: {result['controlSurface']['property_count']}")
print(f"Methods: {result['controlSurface']['method_count']}")
```

### Create Exhibition from Natural Language
```python
# Curator describes the space
exhibition = await mcp.call_tool(
    "create_exhibition_space",
    {
        "description": """
        Create a modern 40x50 foot gallery with:
        - White walls and polished concrete floors
        - Track lighting focused on display areas
        - Three marble pedestals arranged in a triangle
        - Warm color temperature for evening ambiance
        """
    }
)
```

## 🏗️ Architecture

### CE Integration Points
```
Unity Editor
├── CEBuilderSerializer.cs (NEW)
│   ├── Detects OK_*_Builder components
│   ├── Extracts Odin attributes
│   └── Generates MCP tool definitions
├── GameObjectSerializer.cs (MODIFIED)
│   └── Calls CEBuilderSerializer for CE components
└── Standard MCP Bridge components

Python MCP Server
├── ce_builder_tools.py (NEW)
│   ├── Natural language parsing
│   ├── CE-specific tool implementations
│   └── Builder method invocation
└── Standard MCP tools
```

## 🔧 Development

### Building from Source
```bash
# Clone the CE-enhanced fork
git clone -b ce-builder-integration https://github.com/jeremedia/unity-mcp.git
cd unity-mcp

# Install Python dependencies
cd UnityMcpBridge/UnityMcpServer~
uv sync

# Link to your Unity project (for development)
ln -s $(pwd)/UnityMcpBridge ~/YourCEProject/Assets/UnityMcpBridge
```

### Testing CE Features
Run the included test script:
```bash
cd examples
python ce_exhibition_demo.py
```

## 📚 Documentation

- [CE Integration Guide](CE_INTEGRATION.md) - Detailed CE-specific documentation
- [Upstream Documentation](https://github.com/CoplayDev/unity-mcp) - Original Unity MCP features
- [CE Control Surfaces API](https://dev.zice.app/api/v1/control_surfaces) - Rails registry of extracted surfaces

## 🤝 Contributing

### For CE-Specific Features
Submit PRs to the `ce-builder-integration` branch of this fork.

### For General Unity MCP Improvements
Consider contributing to the upstream repository at [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp).

## 📄 License

This fork maintains the MIT license from the original project. CE-specific additions are also MIT licensed.

## 🙏 Acknowledgments

- Original Unity MCP by [Coplay](https://coplay.dev)
- Curation Engine by Jeremy Roush
- Control surface extraction powered by Odin Inspector patterns

## 🔗 Links

- **This Fork**: https://github.com/jeremedia/unity-mcp
- **Upstream**: https://github.com/CoplayDev/unity-mcp
- **Curation Engine**: https://github.com/jeremedia/CurationEngineProductShipper
- **CE Rails API**: https://dev.zice.app

---

## Standard Unity MCP Features

All standard Unity MCP features remain available:

### Available Tools
- `manage_script` - C# script management
- `manage_scene` - Scene operations
- `manage_gameobject` - GameObject manipulation
- `manage_asset` - Asset operations
- `manage_editor` - Editor control
- `read_console` - Console access
- And more...

For complete standard documentation, see the [original README](README-ORIGINAL.md).