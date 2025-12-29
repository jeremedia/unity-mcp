"""
MCP tool for getting real-time Unity Editor performance statistics.
Exposes CE_Performance_Monitor data for diagnosing Editor slowdowns.
"""
from typing import Annotated, Any, Literal

from fastmcp import Context
from services.registry import mcp_for_unity_tool
from services.tools import get_unity_instance_from_context
from transport.unity_transport import send_with_unity_instance
from transport.legacy.unity_connection import async_send_command_with_retry


@mcp_for_unity_tool(
    description="""Get real-time performance statistics from Unity Editor.

    Returns profiler marker timings including:
    - Editor markers (EditorLoop, GUI.Repaint, etc.)
    - GC allocations
    - HDRP rendering
    - CE Builder operations (Draw, Erase, Init)

    Use this to diagnose Editor slowdowns in real-time.

    Includes spike detection (2x rolling average) and bottleneck analysis
    with recommendations for addressing performance issues."""
)
async def get_performance_stats(
    ctx: Context,
    format: Annotated[
        Literal["summary", "detailed", "spikes_only"],
        "Output format: 'summary' (default) shows active markers, 'detailed' shows all data, 'spikes_only' shows only performance spikes"
    ] | None = None,
    include_markers: Annotated[
        list[str],
        "Optional list of marker names to include (filters output)"
    ] | None = None,
) -> dict[str, Any]:
    """
    Get real-time performance statistics from Unity Editor.

    Useful for diagnosing slowdowns in Edit Mode by examining:
    - Which profiler markers are taking the most time
    - Whether any markers are spiking above their rolling average
    - Bottleneck identification with actionable recommendations

    Returns:
        Performance snapshot with markers, spikes, bottleneck, and recommendation.
    """
    # Get active instance from request state (injected by middleware)
    unity_instance = get_unity_instance_from_context(ctx)

    try:
        # Prepare parameters
        params = {
            "format": format or "summary",
        }

        if include_markers:
            params["includeMarkers"] = include_markers

        # Send command to Unity
        response = await send_with_unity_instance(
            async_send_command_with_retry,
            unity_instance,
            "get_performance_stats",
            params
        )

        # Handle response
        if isinstance(response, dict):
            if response.get("success"):
                return {
                    "success": True,
                    "message": response.get("message", "Performance stats retrieved"),
                    "data": response.get("data")
                }
            else:
                return response

        return {"success": False, "message": str(response)}

    except Exception as e:
        return {"success": False, "message": f"Python error getting performance stats: {str(e)}"}
