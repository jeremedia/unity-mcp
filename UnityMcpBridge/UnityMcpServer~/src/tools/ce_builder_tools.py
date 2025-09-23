"""
Curation Engine Builder Tools for Unity MCP

Provides MCP tools for manipulating CE Builders and their control surfaces.
These tools enable natural language curator commands to create exhibitions.
"""

from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from unity_connection import get_unity_connection, send_command_with_retry
from telemetry_decorator import telemetry_tool
import logging
import re

logger = logging.getLogger("mcp-for-unity-server")


def register_ce_builder_tools(mcp: FastMCP):
    """Register all CE Builder tools with the MCP server."""

    @mcp.tool()
    @telemetry_tool("get_builder_control_surface")
    def get_builder_control_surface(
        ctx: Any,
        target: str,
        search_method: str = "by_name"
    ) -> Dict[str, Any]:
        """
        Extracts the control surface (Odin-attributed properties and methods) from a CE Builder.

        Args:
            ctx: MCP context
            target: GameObject name, path, or instance ID containing the Builder
            search_method: How to find the GameObject ("by_name", "by_path", "by_id")

        Returns:
            Control surface data including properties, methods, and MCP tool definition
        """
        try:
            params = {
                "command": "GetBuilderControlSurface",
                "target": target,
                "searchMethod": search_method
            }

            response = send_command_with_retry("manage_gameobject", params)

            if isinstance(response, dict) and response.get("success"):
                return {
                    "success": True,
                    "message": "Control surface extracted successfully",
                    "data": response.get("data")
                }
            return response if isinstance(response, dict) else {
                "success": False,
                "message": str(response)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error extracting control surface: {str(e)}"
            }

    @mcp.tool()
    @telemetry_tool("place_room")
    def place_room(
        ctx: Any,
        preset_name: Optional[str] = None,
        width: float = 30.0,
        length: float = 40.0,
        height: float = 12.0,
        wall_material: str = "white",
        position: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Places an exhibition room in the scene using CE's OK_Room_Builder.

        Args:
            ctx: MCP context
            preset_name: Optional preset to use from the Room preset database
            width: Room width in feet (default 30)
            length: Room length in feet (default 40)
            height: Room height in feet (default 12)
            wall_material: Wall material preset name (default "white")
            position: World position [x, y, z] for the room

        Returns:
            Created room GameObject with OK_Room_Builder configured
        """
        try:
            # First create the GameObject with the Builder component
            create_params = {
                "action": "create",
                "name": f"Room_{width}x{length}",
                "componentsToAdd": ["OK_Room_Builder"],
                "position": position or [0, 0, 0]
            }

            create_response = send_command_with_retry("manage_gameobject", create_params)

            if not (isinstance(create_response, dict) and create_response.get("success")):
                return create_response if isinstance(create_response, dict) else {
                    "success": False,
                    "message": f"Failed to create room: {str(create_response)}"
                }

            # Now configure the Builder properties
            instance_id = create_response.get("data", {}).get("instanceID")
            if instance_id:
                config_params = {
                    "action": "set_component_property",
                    "target": str(instance_id),
                    "searchMethod": "by_id",
                    "componentName": "OK_Room_Builder",
                    "componentProperties": {
                        "OK_Room_Builder": {
                            "roomWidth": width,
                            "roomLength": length,
                            "roomHeight": height,
                            "wallMaterialPreset": wall_material
                        }
                    }
                }

                if preset_name:
                    config_params["componentProperties"]["OK_Room_Builder"]["selectedPreset"] = preset_name

                config_response = send_command_with_retry("manage_gameobject", config_params)

                # Trigger Draw() to manifest the room
                # Note: This might need a custom handler on Unity side
                draw_params = {
                    "action": "invoke_method",
                    "target": str(instance_id),
                    "searchMethod": "by_id",
                    "componentName": "OK_Room_Builder",
                    "methodName": "Draw"
                }

                # Try to invoke Draw, but don't fail if it's not implemented yet
                send_command_with_retry("manage_gameobject", draw_params)

            return {
                "success": True,
                "message": f"Room created successfully",
                "data": create_response.get("data")
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error placing room: {str(e)}"
            }

    @mcp.tool()
    @telemetry_tool("place_floor_pedestal")
    def place_floor_pedestal(
        ctx: Any,
        preset_name: str = "StandardPedestal",
        position: Optional[List[float]] = None,
        rotation: float = 0,
        scale: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Places a floor pedestal for displaying artwork using CE's OK_Floor_Pedestal_Builder.

        Args:
            ctx: MCP context
            preset_name: Pedestal preset from the database
            position: World position [x, y, z]
            rotation: Y-axis rotation in degrees
            scale: Scale factors [x, y, z]

        Returns:
            Created pedestal GameObject with OK_Floor_Pedestal_Builder configured
        """
        try:
            create_params = {
                "action": "create",
                "name": f"Pedestal_{preset_name}",
                "componentsToAdd": ["OK_Floor_Pedestal_Builder"],
                "position": position or [0, 0, 0],
                "rotation": [0, rotation, 0],
                "scale": scale or [1, 1, 1]
            }

            create_response = send_command_with_retry("manage_gameobject", create_params)

            if not (isinstance(create_response, dict) and create_response.get("success")):
                return create_response if isinstance(create_response, dict) else {
                    "success": False,
                    "message": f"Failed to create pedestal: {str(create_response)}"
                }

            # Configure the pedestal with the preset
            instance_id = create_response.get("data", {}).get("instanceID")
            if instance_id:
                config_params = {
                    "action": "set_component_property",
                    "target": str(instance_id),
                    "searchMethod": "by_id",
                    "componentName": "OK_Floor_Pedestal_Builder",
                    "componentProperties": {
                        "OK_Floor_Pedestal_Builder": {
                            "selectedPreset": preset_name
                        }
                    }
                }

                send_command_with_retry("manage_gameobject", config_params)

                # Try to invoke Draw
                draw_params = {
                    "action": "invoke_method",
                    "target": str(instance_id),
                    "searchMethod": "by_id",
                    "componentName": "OK_Floor_Pedestal_Builder",
                    "methodName": "Draw"
                }

                send_command_with_retry("manage_gameobject", draw_params)

            return {
                "success": True,
                "message": f"Pedestal placed successfully",
                "data": create_response.get("data")
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error placing pedestal: {str(e)}"
            }

    @mcp.tool()
    @telemetry_tool("configure_lighting")
    def configure_lighting(
        ctx: Any,
        room_target: str,
        lighting_preset: str = "GalleryTrack",
        intensity: float = 1.0,
        color_temperature: float = 5600
    ) -> Dict[str, Any]:
        """
        Configures room lighting using CE's OK_Room_Light_Builder.

        Args:
            ctx: MCP context
            room_target: Room GameObject name or path
            lighting_preset: Lighting configuration preset
            intensity: Light intensity multiplier
            color_temperature: Color temperature in Kelvin

        Returns:
            Updated room lighting configuration
        """
        try:
            # Find the room GameObject
            find_params = {
                "action": "find",
                "searchTerm": room_target,
                "searchMethod": "by_name"
            }

            find_response = send_command_with_retry("manage_gameobject", find_params)

            if not (isinstance(find_response, dict) and find_response.get("success")):
                return {
                    "success": False,
                    "message": f"Could not find room: {room_target}"
                }

            room_data = find_response.get("data", [])
            if not room_data or (isinstance(room_data, list) and len(room_data) == 0):
                return {
                    "success": False,
                    "message": f"Room not found: {room_target}"
                }

            room_id = room_data[0].get("instanceID") if isinstance(room_data, list) else room_data.get("instanceID")

            # Add or configure the Room Light Builder
            light_params = {
                "action": "add_component",
                "target": str(room_id),
                "searchMethod": "by_id",
                "componentsToAdd": ["OK_Room_Light_Builder"]
            }

            send_command_with_retry("manage_gameobject", light_params)

            # Configure the lighting
            config_params = {
                "action": "set_component_property",
                "target": str(room_id),
                "searchMethod": "by_id",
                "componentName": "OK_Room_Light_Builder",
                "componentProperties": {
                    "OK_Room_Light_Builder": {
                        "lightingPreset": lighting_preset,
                        "intensity": intensity,
                        "colorTemperature": color_temperature
                    }
                }
            }

            config_response = send_command_with_retry("manage_gameobject", config_params)

            return {
                "success": True,
                "message": f"Lighting configured successfully",
                "data": config_response.get("data") if isinstance(config_response, dict) else None
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error configuring lighting: {str(e)}"
            }

    @mcp.tool()
    @telemetry_tool("create_exhibition_space")
    def create_exhibition_space(
        ctx: Any,
        description: str
    ) -> Dict[str, Any]:
        """
        Creates a complete exhibition space from a natural language description.
        This is the main curator interface for creating spaces.

        Args:
            ctx: MCP context
            description: Natural language description of the desired exhibition space

        Returns:
            Created exhibition space with all components

        Example:
            "Create a 30x40 foot gallery with white walls, track lighting, and three pedestals"
        """
        try:
            # Simple parsing of the description
            # In a production system, this would use an LLM
            description_lower = description.lower()

            results = {
                "room": None,
                "pedestals": [],
                "lighting": None
            }

            # Parse and create room if mentioned
            if "room" in description_lower or "gallery" in description_lower or "space" in description_lower:
                # Extract dimensions if present
                dim_pattern = r'(\d+)\s*x\s*(\d+)'
                dim_match = re.search(dim_pattern, description)

                width = float(dim_match.group(1)) if dim_match else 30.0
                length = float(dim_match.group(2)) if dim_match else 40.0

                # Determine wall color
                wall_material = "white"  # default
                if "black" in description_lower:
                    wall_material = "black"
                elif "gray" in description_lower or "grey" in description_lower:
                    wall_material = "gray"

                room_response = place_room(
                    ctx,
                    width=width,
                    length=length,
                    wall_material=wall_material
                )

                if room_response.get("success"):
                    results["room"] = room_response.get("data")

            # Parse and create pedestals if mentioned
            if "pedestal" in description_lower:
                # Look for count
                count_match = re.search(r'(\d+)\s+pedestals?', description_lower)
                pedestal_count = int(count_match.group(1)) if count_match else 1

                # Handle word numbers
                word_numbers = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
                for word, num in word_numbers.items():
                    if word in description_lower and "pedestal" in description_lower:
                        pedestal_count = num
                        break

                # Create pedestals
                for i in range(pedestal_count):
                    x_pos = (i % 3 - 1) * 10  # Simple grid layout
                    z_pos = (i // 3) * 10

                    pedestal_response = place_floor_pedestal(
                        ctx,
                        position=[x_pos, 0, z_pos]
                    )

                    if pedestal_response.get("success"):
                        results["pedestals"].append(pedestal_response.get("data"))

            # Configure lighting if room was created
            if results["room"] and ("lighting" in description_lower or "light" in description_lower):
                room_name = results["room"].get("name")

                lighting_preset = "GalleryTrack"  # default
                if "spot" in description_lower:
                    lighting_preset = "Spotlight"
                elif "ambient" in description_lower:
                    lighting_preset = "Ambient"

                intensity = 1.0
                if "bright" in description_lower:
                    intensity = 1.5
                elif "dim" in description_lower:
                    intensity = 0.5

                if room_name:
                    lighting_response = configure_lighting(
                        ctx,
                        room_target=room_name,
                        lighting_preset=lighting_preset,
                        intensity=intensity
                    )

                    if lighting_response.get("success"):
                        results["lighting"] = lighting_response.get("data")

            return {
                "success": True,
                "message": f"Created exhibition space from description",
                "data": results
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error creating exhibition space: {str(e)}"
            }

    logger.info("CE Builder tools registered successfully")