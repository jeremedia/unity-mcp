"""
MCP tool for invoking methods on Unity Builder components.
Enables calling Odin-exposed methods like AddPedestal, RemoveBuilder, etc.
"""

from typing import Any, Optional, Dict, List, Union
from ..telemetry import telemetry_tool
from ..unity_bridge import send_command_with_retry
from ..server import mcp

@mcp.tool()
@telemetry_tool("invoke_builder_method")
def invoke_builder_method(
    ctx: Any,
    target: str,
    search_method: str = "by_name",
    component_type: str = None,
    method_name: str = None,
    parameters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Invokes a method on a Unity Builder component.

    This tool enables calling methods exposed through Odin attributes (Button, ResponsiveButtonGroup)
    on Builder components, such as AddPedestal on OK_Room_Floor_Builder.

    Args:
        ctx: MCP context
        target: GameObject identifier (name, path, or instance ID)
        search_method: How to find the GameObject ("by_name", "by_path", "by_id")
        component_type: The Builder component type (e.g., "OK_Room_Floor_Builder", "OK_Floor_Pedestal_Builder")
        method_name: Name of the method to invoke (e.g., "AddPedestal", "RemoveBuilder")
        parameters: Optional dictionary of parameters for the method

    Returns:
        Dictionary with operation results including success status and any return values

    Examples:
        # Add a pedestal to a room floor
        invoke_builder_method(
            ctx=ctx,
            target="SingleRoom",
            search_method="by_name",
            component_type="OK_Room_Floor_Builder",
            method_name="AddPedestal"
        )

        # Add pedestal at specific position
        invoke_builder_method(
            ctx=ctx,
            target="Room Floor Builder",
            component_type="OK_Room_Floor_Builder",
            method_name="AddPedestal",
            parameters={"position": [5.0, 0.0, 3.0]}
        )

        # Duplicate a pedestal
        invoke_builder_method(
            ctx=ctx,
            target="MyPedestal",
            component_type="OK_Floor_Pedestal_Builder",
            method_name="Duplicate"
        )
    """

    if not component_type:
        return {
            "success": False,
            "error": "component_type is required"
        }

    if not method_name:
        return {
            "success": False,
            "error": "method_name is required"
        }

    # Build the command for Unity
    command_params = {
        "action": "invoke_method",
        "target": target,
        "search_method": search_method,
        "component_type": component_type,
        "method_name": method_name
    }

    # Add parameters if provided
    if parameters:
        command_params["parameters"] = parameters

    try:
        # First, try to find the GameObject
        find_params = {
            "action": "find",
            "search_term": target,
            "search_method": search_method
        }

        find_response = send_command_with_retry("manage_gameobject", find_params)

        if not find_response.get("success"):
            return {
                "success": False,
                "error": f"Target GameObject '{target}' not found using method '{search_method}'"
            }

        # Get the component and check if method exists
        get_component_params = {
            "action": "get_components",
            "target": target,
            "search_method": search_method
        }

        component_response = send_command_with_retry("manage_gameobject", get_component_params)

        if not component_response.get("success"):
            return {
                "success": False,
                "error": f"Failed to get components for '{target}'"
            }

        # Check if the component exists
        components_data = component_response.get("data", {})
        if component_type not in components_data:
            return {
                "success": False,
                "error": f"Component '{component_type}' not found on GameObject '{target}'"
            }

        # Invoke the method through Unity bridge
        # This requires Unity-side implementation to handle method invocation
        response = send_command_with_retry("invoke_component_method", command_params)

        if response.get("success"):
            return {
                "success": True,
                "message": f"Successfully invoked {component_type}.{method_name} on '{target}'",
                "data": response.get("data", {})
            }
        else:
            return {
                "success": False,
                "error": response.get("error", f"Failed to invoke {method_name}")
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"Exception invoking method: {str(e)}"
        }


@mcp.tool()
@telemetry_tool("get_builder_methods")
def get_builder_methods(
    ctx: Any,
    component_type: str
) -> Dict[str, Any]:
    """
    Gets available methods for a specific Builder component type.

    This tool returns all Odin-exposed methods that can be invoked on a Builder,
    based on the control surface extraction data.

    Args:
        ctx: MCP context
        component_type: The Builder component type (e.g., "OK_Room_Floor_Builder")

    Returns:
        Dictionary with available methods and their signatures
    """

    # This would ideally load from our control surface extractions
    # For now, return known methods for common builders

    known_methods = {
        "OK_Room_Floor_Builder": {
            "AddPedestal": {
                "description": "Add a single pedestal at floor center",
                "parameters": [],
                "async": False
            },
            "AddPedestalCollection": {
                "description": "Add a collection of pedestals using selected preset",
                "parameters": [],
                "async": True
            },
            "RemovePedestals": {
                "description": "Remove all pedestals from the floor",
                "parameters": [],
                "async": False
            },
            "AddDecor": {
                "description": "Add decorative element",
                "parameters": [],
                "async": False
            },
            "AddStairCase": {
                "description": "Add a staircase to the floor",
                "parameters": [],
                "async": True
            }
        },
        "OK_Floor_Pedestal_Builder": {
            "Duplicate": {
                "description": "Duplicate pedestal",
                "parameters": [],
                "async": True
            },
            "RemoveBuilder": {
                "description": "Remove builder",
                "parameters": [],
                "async": True
            },
            "ResetToPreset": {
                "description": "Reset to preset",
                "parameters": [],
                "async": False
            },
            "Rotate_90": {
                "description": "Rotate 90 degrees",
                "parameters": [],
                "async": False
            },
            "UpdateExhibitDisplay": {
                "description": "Update exhibit display",
                "parameters": [],
                "async": True
            }
        },
        "OK_Room_Builder": {
            "UpdateRoom": {
                "description": "Update room with current configuration",
                "parameters": [],
                "async": True
            },
            "DuplicateRoom": {
                "description": "Create a duplicate of this room",
                "parameters": [],
                "async": True
            },
            "DeleteRoom": {
                "description": "Delete this room",
                "parameters": [],
                "async": True
            }
        }
    }

    if component_type in known_methods:
        return {
            "success": True,
            "component_type": component_type,
            "methods": known_methods[component_type]
        }
    else:
        return {
            "success": False,
            "error": f"Unknown component type: {component_type}",
            "hint": f"Known types: {', '.join(known_methods.keys())}"
        }