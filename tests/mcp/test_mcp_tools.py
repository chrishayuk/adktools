"""Tests for the MCP tools module."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from contextlib import AsyncExitStack

from adktools.mcp.mcp_tools import get_mcp_tools


@pytest.mark.asyncio
async def test_get_mcp_tools_stdio():
    """Test getting MCP tools with stdio connection."""
    # Mock MCPToolset.from_server
    mock_tools = [MagicMock(), MagicMock()]
    mock_exit_stack = AsyncExitStack()
    
    with patch('adktools.mcp.mcp_tools.MCPToolset.from_server', new_callable=AsyncMock) as mock_from_server:
        # Set up the mock to return our tools and exit stack
        mock_from_server.return_value = (mock_tools, mock_exit_stack)
        
        # Call the function
        tools, exit_stack = await get_mcp_tools(
            connection_type="stdio",
            command="test_command",
            args=["arg1", "arg2"]
        )
        
        # Check the result
        assert tools == mock_tools
        assert exit_stack == mock_exit_stack
        
        # Verify MCPToolset.from_server was called with correct parameters
        mock_from_server.assert_called_once()
        args, kwargs = mock_from_server.call_args
        
        # Check connection_params is StdioServerParameters with correct values
        connection_params = kwargs.get('connection_params')
        assert connection_params is not None
        assert connection_params.command == "test_command"
        assert connection_params.args == ["arg1", "arg2"]


@pytest.mark.asyncio
async def test_get_mcp_tools_sse():
    """Test getting MCP tools with SSE connection."""
    # Mock MCPToolset.from_server
    mock_tools = [MagicMock(), MagicMock()]
    mock_exit_stack = AsyncExitStack()
    
    with patch('adktools.mcp.mcp_tools.MCPToolset.from_server', new_callable=AsyncMock) as mock_from_server:
        # Set up the mock to return our tools and exit stack
        mock_from_server.return_value = (mock_tools, mock_exit_stack)
        
        # Call the function
        tools, exit_stack = await get_mcp_tools(
            connection_type="sse",
            url="http://test-url.com",
            headers={"key": "value"}
        )
        
        # Check the result
        assert tools == mock_tools
        assert exit_stack == mock_exit_stack
        
        # Verify MCPToolset.from_server was called with correct parameters
        mock_from_server.assert_called_once()
        args, kwargs = mock_from_server.call_args
        
        # Check connection_params is SseServerParams with correct values
        connection_params = kwargs.get('connection_params')
        assert connection_params is not None
        assert connection_params.url == "http://test-url.com"
        assert connection_params.headers == {"key": "value"}


@pytest.mark.asyncio
async def test_get_mcp_tools_sse_missing_url():
    """Test getting MCP tools with SSE connection but missing URL."""
    with pytest.raises(ValueError, match="URL is required for SSE connections"):
        await get_mcp_tools(connection_type="sse")


@pytest.mark.asyncio
async def test_get_mcp_tools_invalid_connection_type():
    """Test getting MCP tools with invalid connection type."""
    with pytest.raises(ValueError, match="Unsupported connection type: invalid"):
        await get_mcp_tools(connection_type="invalid")


@pytest.mark.asyncio
async def test_get_mcp_tools_default_args():
    """Test getting MCP tools with default arguments."""
    # Mock MCPToolset.from_server
    mock_tools = [MagicMock()]
    mock_exit_stack = AsyncExitStack()
    
    with patch('adktools.mcp.mcp_tools.MCPToolset.from_server', new_callable=AsyncMock) as mock_from_server:
        # Set up the mock to return our tools and exit stack
        mock_from_server.return_value = (mock_tools, mock_exit_stack)
        
        # Call the function with minimal arguments
        tools, exit_stack = await get_mcp_tools()
        
        # Verify default values were used
        mock_from_server.assert_called_once()
        args, kwargs = mock_from_server.call_args
        
        connection_params = kwargs.get('connection_params')
        assert connection_params.command == "npx"
        assert connection_params.args == []