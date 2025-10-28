#!/usr/bin/env python3
import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from services import PostService
from models import PostRequest

app = Server("homeopathic-posts")

# Initialize service
post_service = PostService()

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="generate_instagram_post",
            description="Generate holistic homeopathic Instagram post",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Health topic for the post"}
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="generate_facebook_post", 
            description="Generate holistic homeopathic Facebook post",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Health topic for the post"}
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="generate_linkedin_post",
            description="Generate holistic homeopathic LinkedIn post", 
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Health topic for the post"}
                },
                "required": ["topic"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    topic = arguments.get("topic", "")
    
    if name == "generate_instagram_post":
        platform = "instagram"
    elif name == "generate_facebook_post":
        platform = "facebook"
    elif name == "generate_linkedin_post":
        platform = "linkedin"
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    # Generate post
    request = PostRequest(topic=topic, platform=platform)
    result = post_service.generate_post(request)
    
    if result.success:
        return [TextContent(type="text", text=f"Platform: {platform.title()}\nTopic: {result.topic}\n\n{result.content}")]
    else:
        return [TextContent(type="text", text=f"Error: {result.error}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())