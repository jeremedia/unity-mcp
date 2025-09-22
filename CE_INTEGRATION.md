# Curation Engine Unity MCP Integration

This fork extends the Unity MCP bridge with specialized support for Curation Engine (CE) Builders, enabling natural language control of exhibition creation.

## What's New

### 1. Odin Inspector Control Surface Extraction
- Automatically detects CE Builders (`OK_*_Builder` pattern)
- Extracts Odin-attributed properties (`[ShowInInspector]`)
- Discovers actionable methods (`[Button]`, `[ResponsiveButtonGroup]`)
- Generates MCP tool definitions from control surfaces

### 2. CE-Specific MCP Tools
New tools for curator-driven exhibition creation:

- **`get_builder_control_surface`** - Extract control interface from any CE Builder
- **`place_room`** - Create exhibition rooms with OK_Room_Builder
- **`place_floor_pedestal`** - Position pedestals using OK_Floor_Pedestal_Builder
- **`mount_artwork`** - Mount art on walls with frame system
- **`configure_lighting`** - Setup room lighting with OK_Room_Light_Builder
- **`create_exhibition_space`** - Natural language exhibition creation
- **`invoke_builder_method`** - Call Builder methods (Draw, Erase, etc.)

### 3. Natural Language Interface
Transform curator descriptions into exhibition spaces:

```python
await mcp.call_tool(
    "create_exhibition_space",
    {
        "description": "Create a 30x40 foot gallery with white walls, track lighting, and three pedestals"
    }
)
```

## Installation

### 1. Install Unity Package
Copy the `UnityMcpBridge` folder into your CE Unity project's `Assets` directory.

### 2. Add CE Assembly References
The package needs access to CE assemblies. In Unity:
1. Select `UnityMcpBridge/Editor/UnityMcpBridge.Editor.asmdef`
2. Add references to:
   - `CurationEngineScripts`
   - `Sirenix.OdinInspector.Attributes`

### 3. Install Python Server
```bash
cd UnityMcpBridge/UnityMcpServer~
uv sync
uv run start-server
```

### 4. Configure MCP Client
Add to your Claude Code settings:

```json
{
  "mcpServers": {
    "unity-mcp-ce": {
      "command": "uv",
      "args": ["run", "start-server"],
      "cwd": "/path/to/unity-mcp/UnityMcpBridge/UnityMcpServer~"
    }
  }
}
```

## Usage Examples

### Extract Control Surface
```python
# Get the control surface for a CE Builder
result = await mcp.call_tool(
    "get_builder_control_surface",
    {
        "target": "Room_Gallery",
        "search_method": "by_name"
    }
)

# Result contains:
# - properties: All Odin-attributed properties
# - methods: Available actions (Draw, Erase, etc.)
# - mcpToolDefinition: Generated tool spec
```

### Create Exhibition Room
```python
# Place a gallery room with specific dimensions
room = await mcp.call_tool(
    "place_room",
    {
        "width": 40,
        "length": 50,
        "height": 14,
        "wall_material": "white",
        "preset_name": "ModernGallery"
    }
)
```

### Natural Language Creation
```python
# Create complete exhibition from description
exhibition = await mcp.call_tool(
    "create_exhibition_space",
    {
        "description": """
        Create a 30x40 foot modern gallery with:
        - White walls and polished concrete floors
        - Track lighting focused on display areas
        - Three marble pedestals in the center
        - Optimal viewing circulation path
        """
    }
)
```

## Architecture

### Control Surface Discovery Flow
1. **Unity Side**: `CEBuilderSerializer.cs` detects CE Builders
2. **Extraction**: Reflects on Odin attributes to find control points
3. **Generation**: Creates MCP tool definitions from control surface
4. **Python Side**: `ce_builder_tools.py` provides natural language interface

### Key Components

#### CEBuilderSerializer.cs
- Detects CE Builder pattern (`OK_*_Builder`)
- Extracts Odin attributes
- Maps properties to Config paths
- Generates tool definitions

#### ce_builder_tools.py
- Implements CE-specific MCP tools
- Natural language parsing
- Builder method invocation
- Exhibition orchestration

## V1 Essential Builders Supported

All 10 V1 essential builders have been extracted and are controllable:

1. **OK_Room_Builder** - Exhibition spaces
2. **OK_Wall_Builder** - Wall construction
3. **OK_Floor_Pedestal_Builder** - Display pedestals (90 properties!)
4. **OK_Frame_Layout_Builder** - Artwork arrangement
5. **OK_Framed_Print_Builder** - Artwork display
6. **OK_Gallery_Show_Manager_Builder** - Exhibition management
7. **OK_Structure_Level_Builder** - Building levels
8. **OK_Room_Light_Builder** - Lighting systems
9. **OK_Material_Builder** - Surface materials
10. **OK_Portal_Builder** - Space connections

## Testing

Run the demo script to see all features:

```bash
cd examples
python ce_exhibition_demo.py
```

This demonstrates:
- Natural language gallery creation
- Control surface extraction
- Curated exhibition setup
- Builder method invocation

## Next Steps

### Immediate (Day 1-2)
- [ ] Test with live CE Unity project
- [ ] Validate control surface extraction accuracy
- [ ] Create first MCP-driven exhibition

### Short Term (Week 1)
- [ ] Generate tools for remaining 134 builders
- [ ] Implement preset database integration
- [ ] Add tour and viewpoint creation

### Long Term
- [ ] LLM-powered description parsing
- [ ] Exhibition export via MCP
- [ ] Analytics integration
- [ ] Multi-room exhibition orchestration

## Contributing

This is a fork optimized for Curation Engine. CE-specific changes should remain in this fork. Generic Unity MCP improvements can be contributed upstream to CoplayDev/unity-mcp.

## License

Inherits from upstream Unity MCP (MIT). CE-specific additions also under MIT.

## Support

For CE-specific issues, contact the Curation Engine team.
For Unity MCP core issues, see upstream: https://github.com/CoplayDev/unity-mcp