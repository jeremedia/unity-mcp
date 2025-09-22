#!/usr/bin/env python3
"""
Curation Engine MCP Demo
Demonstrates creating an exhibition using natural language commands via MCP.

Prerequisites:
1. Unity Editor running with CE project open
2. UnityMcpBridge installed in the project
3. Python MCP server running (uv run start-server)
"""

import asyncio
import json
from typing import Dict, Any


class CECuratorDemo:
    """Demonstrates CE MCP integration for natural language exhibition creation."""

    def __init__(self, mcp_client):
        self.mcp = mcp_client
        self.exhibition_data = {}

    async def create_gallery_from_description(self, description: str):
        """
        Creates a complete gallery from natural language description.

        Example:
            "Create a 30x40 foot gallery with white walls, track lighting,
             and three pedestals arranged in the center"
        """
        print(f"\n🎨 Creating Exhibition: {description}\n")
        print("=" * 60)

        # Use the natural language interface
        result = await self.mcp.call_tool(
            "create_exhibition_space",
            {
                "description": description,
                "use_ai_parsing": True
            }
        )

        if result.success:
            self.exhibition_data = result.data
            print("✅ Exhibition space created successfully!")
            self._print_exhibition_summary()
        else:
            print(f"❌ Failed to create exhibition: {result.message}")

        return result

    async def demonstrate_control_surface_extraction(self):
        """Shows how control surface extraction works for CE Builders."""
        print("\n🔍 Demonstrating Control Surface Extraction\n")
        print("=" * 60)

        # Create a simple room first
        room_result = await self.mcp.call_tool(
            "place_room",
            {
                "width": 20,
                "length": 25,
                "height": 10,
                "wall_material": "white"
            }
        )

        if room_result.success:
            room_name = room_result.data["name"]
            print(f"✅ Created room: {room_name}")

            # Extract its control surface
            surface_result = await self.mcp.call_tool(
                "get_builder_control_surface",
                {
                    "target": room_name,
                    "search_method": "by_name"
                }
            )

            if surface_result.success:
                surface = surface_result.data["controlSurface"]
                print(f"\n📋 Control Surface for OK_Room_Builder:")
                print(f"   Properties: {surface['property_count']}")
                print(f"   Methods: {surface['method_count']}")

                # Show some properties
                if "properties" in surface:
                    print("\n   Sample Properties:")
                    for prop_name, prop_data in list(surface["properties"].items())[:5]:
                        print(f"   - {prop_name}: {prop_data.get('type', 'unknown')}")

                # Show available methods
                if "methods" in surface:
                    print("\n   Available Methods:")
                    for method_name, method_data in surface["methods"].items():
                        async_tag = " [async]" if method_data.get("async") else ""
                        print(f"   - {method_name}{async_tag}")

    async def create_curated_exhibition(self):
        """Creates a professionally curated exhibition with specific artworks."""
        print("\n🖼️ Creating Curated Exhibition\n")
        print("=" * 60)

        # Step 1: Create the gallery space
        print("Step 1: Creating gallery space...")
        room = await self.mcp.call_tool(
            "place_room",
            {
                "preset_name": "ModernGallery",
                "width": 40,
                "length": 50,
                "height": 14,
                "wall_material": "white"
            }
        )

        if not room.success:
            print("Failed to create room")
            return

        room_name = room.data["name"]
        print(f"✅ Created: {room_name}")

        # Step 2: Add pedestals for sculptures
        print("\nStep 2: Placing pedestals...")
        pedestal_positions = [
            [-10, 0, 0],
            [0, 0, 0],
            [10, 0, 0]
        ]

        for i, pos in enumerate(pedestal_positions):
            pedestal = await self.mcp.call_tool(
                "place_floor_pedestal",
                {
                    "preset_name": "MarblePedestal" if i == 1 else "StandardPedestal",
                    "position": pos,
                    "rotation": i * 45  # Vary rotation
                }
            )
            if pedestal.success:
                print(f"✅ Placed pedestal {i+1} at position {pos}")

        # Step 3: Mount artwork on walls
        print("\nStep 3: Mounting artwork on walls...")

        # Assuming we have wall references (in real scenario, we'd find them)
        artworks = [
            {"wall": "Wall_North", "artwork": "MonaLisa", "x": 0.5, "y": 0.6},
            {"wall": "Wall_South", "artwork": "StarryNight", "x": 0.3, "y": 0.6},
            {"wall": "Wall_South", "artwork": "TheScream", "x": 0.7, "y": 0.6}
        ]

        for art in artworks:
            # In production, we'd actually mount these
            print(f"✅ Would mount {art['artwork']} on {art['wall']}")

        # Step 4: Configure lighting
        print("\nStep 4: Configuring gallery lighting...")
        lighting = await self.mcp.call_tool(
            "configure_lighting",
            {
                "room_target": room_name,
                "lighting_preset": "GalleryTrack",
                "intensity": 1.2,
                "color_temperature": 5600
            }
        )

        if lighting.success:
            print("✅ Lighting configured for optimal artwork viewing")

        print("\n" + "=" * 60)
        print("🎉 Curated exhibition ready for visitors!")

    async def test_builder_method_invocation(self):
        """Tests invoking methods on CE Builders."""
        print("\n⚙️ Testing Builder Method Invocation\n")
        print("=" * 60)

        # Create a test pedestal
        pedestal = await self.mcp.call_tool(
            "place_floor_pedestal",
            {
                "preset_name": "StandardPedestal",
                "position": [0, 0, 5]
            }
        )

        if pedestal.success:
            instance_id = pedestal.data["instanceID"]
            print(f"✅ Created test pedestal (ID: {instance_id})")

            # Invoke Draw method to re-render
            print("\nInvoking Draw() method...")
            draw_result = await self.mcp.call_tool(
                "invoke_builder_method",
                {
                    "instance_id": instance_id,
                    "method_name": "Draw",
                    "component_name": "OK_Floor_Pedestal_Builder",
                    "is_async": True
                }
            )

            if draw_result.success:
                print("✅ Successfully invoked Draw() method")
            else:
                print(f"❌ Failed to invoke Draw(): {draw_result.message}")

    def _print_exhibition_summary(self):
        """Prints a summary of the created exhibition."""
        if not self.exhibition_data:
            return

        print("\n📊 Exhibition Summary:")

        if "room" in self.exhibition_data:
            room = self.exhibition_data["room"]
            print(f"   Room: {room.get('name', 'Unknown')}")

        if "pedestals" in self.exhibition_data:
            count = len(self.exhibition_data["pedestals"])
            print(f"   Pedestals: {count} placed")

        if "lighting" in self.exhibition_data:
            print(f"   Lighting: Configured")


async def main():
    """Main demo entry point."""

    # In production, this would connect to the actual MCP server
    # For demo purposes, we're showing the structure

    print("=" * 60)
    print(" Curation Engine MCP Integration Demo")
    print(" Natural Language Exhibition Creation")
    print("=" * 60)

    # Mock MCP client for demonstration
    # In real usage, this would be the actual MCP client connection
    class MockMCPClient:
        async def call_tool(self, tool_name, params):
            # Mock successful response
            from types import SimpleNamespace
            return SimpleNamespace(
                success=True,
                data={"name": f"Mock_{tool_name}_Result", "instanceID": 12345},
                message="Mock success"
            )

    mcp_client = MockMCPClient()
    demo = CECuratorDemo(mcp_client)

    # Run demonstrations
    demos = [
        ("Natural Language Gallery Creation",
         lambda: demo.create_gallery_from_description(
             "Create a 30x40 foot gallery with white walls, track lighting, and three pedestals"
         )),

        ("Control Surface Extraction",
         demo.demonstrate_control_surface_extraction),

        ("Curated Exhibition Setup",
         demo.create_curated_exhibition),

        ("Builder Method Invocation",
         demo.test_builder_method_invocation)
    ]

    for title, demo_func in demos:
        print(f"\n{'=' * 60}")
        print(f" Demo: {title}")
        print(f"{'=' * 60}")

        try:
            await demo_func()
        except Exception as e:
            print(f"❌ Demo failed: {e}")

        await asyncio.sleep(1)  # Brief pause between demos

    print("\n" + "=" * 60)
    print(" Demo Complete!")
    print(" CE + MCP = Natural Language Exhibition Creation 🎨")
    print("=" * 60)


if __name__ == "__main__":
    # Run the async demo
    asyncio.run(main())