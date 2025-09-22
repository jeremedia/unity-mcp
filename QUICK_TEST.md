# Quick Test Guide - CE Unity MCP

## Installation in CE Unity Project

### Option A: Add Our Fork (Alongside existing unity-mcp)
```
https://github.com/jeremedia/unity-mcp.git?path=/UnityMcpBridge#v3.4.0-ce.1
```

### Option B: Replace existing unity-mcp
1. Remove existing "MCP for Unity" package
2. Add our CE version with the URL above

## Test CE Features

### 1. Test Odin Control Surface Extraction
Ask Claude: "Find a GameObject with OK_Room_Builder and extract its control surface"

Expected: Should return properties with [ShowInInspector] and methods with [Button]

### 2. Test Natural Language Creation
Ask Claude: "Create a 20x30 foot gallery room"

Expected: Should create room GameObject with OK_Room_Builder configured

### 3. Test Builder Method Invocation
Ask Claude: "Find any OK builder and invoke its Draw method"

Expected: Should trigger the Draw() async method

## What Should Work Now

✅ All standard unity-mcp tools (manage_scene, manage_gameobject, etc.)
✅ CE-specific tools (place_room, place_floor_pedestal, etc.)
✅ Odin Inspector attribute detection
✅ Natural language exhibition creation

## What's Next

- [ ] Test with real CE scene with existing builders
- [ ] Create first exhibition via natural language
- [ ] Extract control surfaces for remaining 134 builders
- [ ] Build proper Curator agent

## Debug Commands

If things don't work, check:

```python
# List available tools
mcp.list_tools()

# Check if CE builders are detected
mcp.call_tool("list_resources", {"pattern": "OK_*_Builder.cs"})

# Try manual control surface extraction
mcp.call_tool("get_builder_control_surface", {"target": "SomeBuilder", "search_method": "by_name"})
```