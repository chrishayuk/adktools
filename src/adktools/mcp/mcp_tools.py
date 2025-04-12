# adktools/mcp/mcp_tools.py
"""
MCP tools utilities for ADK agents.

This module provides utilities for working with Model Context Protocol (MCP) servers.
"""
from typing import List, Optional, Tuple, Dict, Any
from contextlib import AsyncExitStack

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams, StdioServerParameters


async def get_mcp_tools(
    connection_type: str = "stdio",
    command: str = "npx",
    args: Optional[List[str]] = None,
    url: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
) -> Tuple[List[Any], AsyncExitStack]:
    """
    Get tools from an MCP server.
    
    Args:
        connection_type: Type of connection to use ("stdio" or "sse")
        command: Command to run for stdio connections
        args: Arguments for the command
        url: URL for SSE server connections
        headers: Headers for SSE server connections
        
    Returns:
        Tuple containing a list of tools and the exit stack for cleanup
    """
    if args is None:
        args = []
        
    if connection_type.lower() == "stdio":
        connection_params = StdioServerParameters(
            command=command,
            args=args
        )
    elif connection_type.lower() == "sse":
        if not url:
            raise ValueError("URL is required for SSE connections")
        connection_params = SseServerParams(
            url=url,
            headers=headers or {}
        )
    else:
        raise ValueError(f"Unsupported connection type: {connection_type}")
    
    # Get tools from MCP server
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=connection_params
    )
    
    return tools, exit_stack