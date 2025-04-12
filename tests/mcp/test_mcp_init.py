"""Tests for the MCP package __init__.py."""

import pytest

from adktools import mcp
from adktools.mcp import get_mcp_tools, MCPAgentBuilder
from adktools.mcp.mcp_tools import get_mcp_tools as get_mcp_tools_direct
from adktools.mcp.mcp_agent_builder import MCPAgentBuilder as MCPAgentBuilder_direct


def test_mcp_imports():
    """Test that imports from the MCP package work correctly."""
    # Test that get_mcp_tools is exposed at the package level
    assert get_mcp_tools is get_mcp_tools_direct
    
    # Test that MCPAgentBuilder is exposed at the package level
    assert MCPAgentBuilder is MCPAgentBuilder_direct
    
    # Test that these are available in __all__
    assert "get_mcp_tools" in mcp.__all__
    assert "MCPAgentBuilder" in mcp.__all__