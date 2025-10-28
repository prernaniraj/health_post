#!/usr/bin/env python3
import asyncio
import json
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

async def test_mcp_tools():
    """Test MCP server tools"""
    
    # Connect to MCP server
    async with stdio_client() as (read, write):
        async with ClientSession(read, write) as session:
            
            # Initialize
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")
            
            # Test Instagram post generation
            print("\n=== Testing Instagram Post ===")
            result = await session.call_tool(
                "generate_instagram_post",
                {"topic": "natural stress relief"}
            )
            print(result.content[0].text)
            
            # Test Facebook post generation
            print("\n=== Testing Facebook Post ===")
            result = await session.call_tool(
                "generate_facebook_post", 
                {"topic": "immune system support"}
            )
            print(result.content[0].text)
            
            # Test LinkedIn post generation
            print("\n=== Testing LinkedIn Post ===")
            result = await session.call_tool(
                "generate_linkedin_post",
                {"topic": "mind-body wellness"}
            )
            print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())