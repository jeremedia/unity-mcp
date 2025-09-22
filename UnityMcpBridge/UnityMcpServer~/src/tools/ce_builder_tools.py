"""
Curation Engine Builder Tools for Unity MCP

Provides MCP tools for manipulating CE Builders and their control surfaces.
These tools enable natural language curator commands to create exhibitions.
"""

from typing import Dict, Any, List, Optional
from ..bridge import Bridge
from ..models.result import UnityResult
import json


# Tool 1: Get Control Surface for a Builder
async def get_builder_control_surface(
    target: str,
    search_method: str = "by_name"
) -> UnityResult:
    """
    Extracts the control surface (Odin-attributed properties and methods) from a CE Builder.

    Args:
        target: GameObject name, path, or instance ID containing the Builder
        search_method: How to find the GameObject ("by_name", "by_path", "by_id")

    Returns:
        Control surface data including properties, methods, and MCP tool definition
    """
    return await Bridge.call_unity_method(
        "ManageGameObjectHandler",
        "GetBuilderControlSurface",
        {
            "target": target,
            "search_method": search_method
        }
    )


# Tool 2: Place a Room using preset
async def place_room(
    preset_name: Optional[str] = None,
    width: float = 30.0,
    length: float = 40.0,
    height: float = 12.0,
    wall_material: str = "white",
    position: Optional[List[float]] = None,
    **kwargs
) -> UnityResult:
    """
    Places an exhibition room in the scene using CE's OK_Room_Builder.

    Args:
        preset_name: Optional preset to use from the Room preset database
        width: Room width in feet (default 30)
        length: Room length in feet (default 40)
        height: Room height in feet (default 12)
        wall_material: Wall material preset name (default "white")
        position: World position [x, y, z] for the room
        **kwargs: Additional Builder properties to set

    Returns:
        Created room GameObject with OK_Room_Builder configured
    """
    component_properties = {
        "OK_Room_Builder": {
            "roomWidth": width,
            "roomLength": length,
            "roomHeight": height,
            "wallMaterialPreset": wall_material
        }
    }

    # Add any additional properties
    component_properties["OK_Room_Builder"].update(kwargs)

    # If preset specified, set it
    if preset_name:
        component_properties["OK_Room_Builder"]["selectedPreset"] = preset_name

    # Create the room GameObject with Builder
    result = await Bridge.call_unity_method(
        "ManageGameObjectHandler",
        "CreateGameObject",
        {
            "name": f"Room_{width}x{length}",
            "components": ["OK_Room_Builder"],
            "component_properties": component_properties,
            "position": position or [0, 0, 0]
        }
    )

    # Trigger Draw() to manifest the room
    if result.success and result.data:
        instance_id = result.data.get("instanceID")
        if instance_id:
            await invoke_builder_method(
                instance_id=instance_id,
                method_name="Draw",
                is_async=True
            )

    return result


# Tool 3: Place a Floor Pedestal
async def place_floor_pedestal(
    preset_name: str = "StandardPedestal",
    position: Optional[List[float]] = None,
    rotation: float = 0,
    scale: Optional[List[float]] = None,
    **kwargs
) -> UnityResult:
    """
    Places a floor pedestal for displaying artwork using CE's OK_Floor_Pedestal_Builder.

    Args:
        preset_name: Pedestal preset from the database
        position: World position [x, y, z]
        rotation: Y-axis rotation in degrees
        scale: Scale factors [x, y, z]
        **kwargs: Additional Builder properties

    Returns:
        Created pedestal GameObject with OK_Floor_Pedestal_Builder configured
    """
    component_properties = {
        "OK_Floor_Pedestal_Builder": {
            "selectedPreset": preset_name
        }
    }

    component_properties["OK_Floor_Pedestal_Builder"].update(kwargs)

    result = await Bridge.call_unity_method(
        "ManageGameObjectHandler",
        "CreateGameObject",
        {
            "name": f"Pedestal_{preset_name}",
            "components": ["OK_Floor_Pedestal_Builder"],
            "component_properties": component_properties,
            "position": position or [0, 0, 0],
            "rotation": [0, rotation, 0],
            "scale": scale or [1, 1, 1]
        }
    )

    # Trigger Draw() to manifest
    if result.success and result.data:
        instance_id = result.data.get("instanceID")
        if instance_id:
            await invoke_builder_method(
                instance_id=instance_id,
                method_name="Draw",
                is_async=True
            )

    return result


# Tool 4: Mount Artwork on Wall
async def mount_artwork(
    wall_target: str,
    artwork_preset: str,
    position_x: float = 0.5,
    position_y: float = 0.5,
    frame_preset: Optional[str] = None,
    **kwargs
) -> UnityResult:
    """
    Mounts artwork on a wall using CE's frame and print system.

    Args:
        wall_target: Wall GameObject name or path
        artwork_preset: Artwork/print preset name
        position_x: Normalized position on wall width (0-1)
        position_y: Normalized position on wall height (0-1)
        frame_preset: Optional frame preset name
        **kwargs: Additional frame/print properties

    Returns:
        Created artwork GameObject mounted on the wall
    """
    # First find the wall
    wall_result = await Bridge.call_unity_method(
        "ManageGameObjectHandler",
        "FindGameObject",
        {
            "search_term": wall_target,
            "search_method": "by_name"
        }
    )

    if not wall_result.success:
        return wall_result

    wall_id = wall_result.data.get("instanceID")

    # Create frame layout on the wall
    result = await Bridge.call_unity_method(
        "ManageGameObjectHandler",
        "CreateGameObject",
        {
            "name": f"Artwork_{artwork_preset}",
            "parent_id": wall_id,
            "components": ["OK_Frame_Layout_Builder", "OK_Framed_Print_Builder"],
            "component_properties": {
                "OK_Frame_Layout_Builder": {
                    "normalizedX": position_x,
                    "normalizedY": position_y,
                    "framePreset": frame_preset
                },
                "OK_Framed_Print_Builder": {
                    "printPreset": artwork_preset,
                    **kwargs
                }
            }
        }
    )

    # Trigger Draw() on both builders
    if result.success and result.data:
        instance_id = result.data.get("instanceID")
        if instance_id:
            await invoke_builder_method(
                instance_id=instance_id,
                method_name="Draw",
                is_async=True,
                component_name="OK_Frame_Layout_Builder"
            )
            await invoke_builder_method(
                instance_id=instance_id,
                method_name="Draw",
                is_async=True,
                component_name="OK_Framed_Print_Builder"
            )

    return result


# Tool 5: Configure Lighting
async def configure_lighting(
    room_target: str,
    lighting_preset: str = "GalleryTrack",
    intensity: float = 1.0,
    color_temperature: float = 5600,
    **kwargs
) -> UnityResult:
    """
    Configures room lighting using CE's OK_Room_Light_Builder.

    Args:
        room_target: Room GameObject name or path
        lighting_preset: Lighting configuration preset
        intensity: Light intensity multiplier
        color_temperature: Color temperature in Kelvin
        **kwargs: Additional lighting properties

    Returns:
        Updated room lighting configuration
    """
    # Find the room
    room_result = await Bridge.call_unity_method(
        "ManageGameObjectHandler",
        "FindGameObject",
        {
            "search_term": room_target,
            "search_method": "by_name"
        }
    )

    if not room_result.success:
        return room_result

    room_id = room_result.data.get("instanceID")

    # Add or update Room Light Builder
    result = await Bridge.call_unity_method(
        "ManageGameObjectHandler",
        "UpdateComponent",
        {
            "target_id": room_id,
            "component_name": "OK_Room_Light_Builder",
            "properties": {
                "lightingPreset": lighting_preset,
                "intensity": intensity,
                "colorTemperature": color_temperature,
                **kwargs
            }
        }
    )

    # Trigger Draw() to update lighting
    if result.success:
        await invoke_builder_method(
            instance_id=room_id,
            method_name="Draw",
            is_async=True,
            component_name="OK_Room_Light_Builder"
        )

    return result


# Tool 6: Create Exhibition Space from Description
async def create_exhibition_space(
    description: str,
    use_ai_parsing: bool = True
) -> UnityResult:
    """
    Creates a complete exhibition space from a natural language description.
    This is the main curator interface for creating spaces.

    Args:
        description: Natural language description of the desired exhibition space
        use_ai_parsing: Whether to use AI to parse the description (future feature)

    Returns:
        Created exhibition space with all components

    Example:
        "Create a 30x40 foot gallery with white walls, track lighting, and three pedestals"
    """
    # For now, use simple parsing - in future, integrate with LLM
    parsed = parse_exhibition_description(description)

    results = {
        "room": None,
        "pedestals": [],
        "lighting": None
    }

    # Create the room
    if parsed.get("room"):
        room_params = parsed["room"]
        room_result = await place_room(**room_params)
        results["room"] = room_result.data if room_result.success else None

    # Add pedestals
    for pedestal_params in parsed.get("pedestals", []):
        pedestal_result = await place_floor_pedestal(**pedestal_params)
        if pedestal_result.success:
            results["pedestals"].append(pedestal_result.data)

    # Configure lighting
    if parsed.get("lighting") and results["room"]:
        lighting_params = parsed["lighting"]
        lighting_params["room_target"] = results["room"]["name"]
        lighting_result = await configure_lighting(**lighting_params)
        results["lighting"] = lighting_result.data if lighting_result.success else None

    return UnityResult(
        success=True,
        data=results,
        message=f"Created exhibition space from description"
    )


# Tool 7: Invoke Builder Method
async def invoke_builder_method(
    instance_id: int,
    method_name: str,
    component_name: str = None,
    is_async: bool = False,
    parameters: Optional[Dict[str, Any]] = None
) -> UnityResult:
    """
    Invokes a method on a CE Builder component.

    Args:
        instance_id: GameObject instance ID
        method_name: Method name to invoke (e.g., "Draw", "Erase")
        component_name: Specific component name if multiple Builders
        is_async: Whether the method is async (UniTask)
        parameters: Optional method parameters

    Returns:
        Method execution result
    """
    return await Bridge.call_unity_method(
        "ManageGameObjectHandler",
        "InvokeComponentMethod",
        {
            "instance_id": instance_id,
            "component_name": component_name,
            "method_name": method_name,
            "is_async": is_async,
            "parameters": parameters or {}
        }
    )


# Helper function to parse exhibition descriptions
def parse_exhibition_description(description: str) -> Dict[str, Any]:
    """
    Simple parser for exhibition descriptions.
    In production, this would use an LLM for better parsing.
    """
    description_lower = description.lower()

    parsed = {}

    # Parse room dimensions
    if "room" in description_lower or "gallery" in description_lower or "space" in description_lower:
        room_params = {"preset_name": None}

        # Look for dimensions (e.g., "30x40")
        import re
        dim_pattern = r'(\d+)\s*x\s*(\d+)'
        dim_match = re.search(dim_pattern, description)
        if dim_match:
            room_params["width"] = float(dim_match.group(1))
            room_params["length"] = float(dim_match.group(2))

        # Look for height
        height_pattern = r'(\d+)\s*(?:foot|feet|ft)?\s*(?:tall|high|height)'
        height_match = re.search(height_pattern, description_lower)
        if height_match:
            room_params["height"] = float(height_match.group(1))

        # Look for wall color
        if "white" in description_lower:
            room_params["wall_material"] = "white"
        elif "black" in description_lower:
            room_params["wall_material"] = "black"
        elif "gray" in description_lower or "grey" in description_lower:
            room_params["wall_material"] = "gray"

        parsed["room"] = room_params

    # Parse pedestals
    if "pedestal" in description_lower:
        pedestal_count = 1

        # Look for count
        count_patterns = [
            r'(\d+)\s+pedestals?',
            r'(one|two|three|four|five)\s+pedestals?'
        ]

        number_words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}

        for pattern in count_patterns:
            match = re.search(pattern, description_lower)
            if match:
                count_str = match.group(1)
                if count_str.isdigit():
                    pedestal_count = int(count_str)
                elif count_str in number_words:
                    pedestal_count = number_words[count_str]
                break

        # Create pedestals with distributed positions
        pedestals = []
        for i in range(pedestal_count):
            # Simple grid layout
            x_pos = (i % 3 - 1) * 10  # -10, 0, 10
            z_pos = (i // 3) * 10

            pedestals.append({
                "preset_name": "StandardPedestal",
                "position": [x_pos, 0, z_pos]
            })

        parsed["pedestals"] = pedestals

    # Parse lighting
    if "lighting" in description_lower or "light" in description_lower:
        lighting_params = {}

        if "track" in description_lower:
            lighting_params["lighting_preset"] = "GalleryTrack"
        elif "spot" in description_lower:
            lighting_params["lighting_preset"] = "Spotlight"
        elif "ambient" in description_lower:
            lighting_params["lighting_preset"] = "Ambient"
        else:
            lighting_params["lighting_preset"] = "GalleryTrack"

        # Look for intensity
        if "bright" in description_lower:
            lighting_params["intensity"] = 1.5
        elif "dim" in description_lower:
            lighting_params["intensity"] = 0.5
        else:
            lighting_params["intensity"] = 1.0

        parsed["lighting"] = lighting_params

    return parsed


# Register all tools when module is imported
def register_ce_builder_tools(mcp):
    """Register all CE Builder tools with the MCP server."""
    import logging
    logger = logging.getLogger("mcp-for-unity-server")

    tools = [
        ("get_builder_control_surface", get_builder_control_surface,
         "Extract control surface from CE Builder"),
        ("place_room", place_room,
         "Place an exhibition room using CE's OK_Room_Builder"),
        ("place_floor_pedestal", place_floor_pedestal,
         "Place a floor pedestal using CE's OK_Floor_Pedestal_Builder"),
        ("mount_artwork", mount_artwork,
         "Mount artwork on a wall using CE's frame system"),
        ("configure_lighting", configure_lighting,
         "Configure room lighting using CE's OK_Room_Light_Builder"),
        ("create_exhibition_space", create_exhibition_space,
         "Create complete exhibition from natural language description"),
        ("invoke_builder_method", invoke_builder_method,
         "Invoke a method on a CE Builder component")
    ]

    for name, func, description in tools:
        try:
            # Register with MCP following the existing pattern
            mcp.tool(name=name, description=description)(func)
            logger.info(f"Registered CE Builder tool: {name}")
        except Exception as e:
            logger.error(f"Failed to register CE Builder tool {name}: {e}")

    logger.info(f"Registered {len(tools)} CE Builder tools successfully")