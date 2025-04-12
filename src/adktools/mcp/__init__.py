# adktools/mcp/__init__.py
"""
MCP tools and utilities for ADK agents.

This package provides tools for working with Model Context Protocol (MCP) servers.
"""

from adktools.mcp.mcp_tools import get_mcp_tools
from adktools.mcp.mcp_agent_builder import MCPAgentBuilder

# Make these available at the top level of the mcp package
__all__ = [
    "get_mcp_tools",
    "MCPAgentBuilder",
]