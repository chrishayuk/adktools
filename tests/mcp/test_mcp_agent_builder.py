"""Tests for the MCP agent builder module."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from contextlib import AsyncExitStack

from adktools.mcp.mcp_agent_builder import MCPAgentBuilder


@pytest.mark.asyncio
async def test_mcp_agent_builder_initialization():
    """Test initialization of MCPAgentBuilder."""
    # Test with default values
    builder = MCPAgentBuilder()
    assert builder.connection_type == "stdio"
    assert builder.command == "npx"
    assert builder.args == []
    assert builder.url is None
    assert builder.headers == {}
    assert builder.agent is None
    assert builder.exit_stack is None
    
    # Test with custom values
    builder = MCPAgentBuilder(
        connection_type="sse",
        command="custom_command",
        args=["arg1", "arg2"],
        url="http://test.com",
        headers={"key": "value"}
    )
    assert builder.connection_type == "sse"
    assert builder.command == "custom_command"
    assert builder.args == ["arg1", "arg2"]
    assert builder.url == "http://test.com"
    assert builder.headers == {"key": "value"}


@pytest.mark.asyncio
async def test_build_agent():
    """Test building an agent with MCPAgentBuilder."""
    # Create mocks
    mock_tools = [MagicMock(), MagicMock()]
    mock_exit_stack = AsyncExitStack()
    mock_agent = MagicMock()
    
    # Create builder
    builder = MCPAgentBuilder(
        connection_type="stdio",
        command="npx",
        args=["arg1", "arg2"]
    )
    
    # Patch get_mcp_tools
    with patch('adktools.mcp.mcp_agent_builder.get_mcp_tools', new_callable=AsyncMock) as mock_get_tools:
        # Set up mock to return our tools and exit stack
        mock_get_tools.return_value = (mock_tools, mock_exit_stack)
        
        # Patch LlmAgent
        with patch('adktools.mcp.mcp_agent_builder.LlmAgent') as mock_llm_agent:
            # Set up mock to return our agent
            mock_llm_agent.return_value = mock_agent
            
            # Call build_agent
            agent = await builder.build_agent(
                model="test-model",
                name="test-agent",
                instruction="Test instruction"
            )
            
            # Check the result
            assert agent == mock_agent
            assert builder.exit_stack == mock_exit_stack
            
            # Verify get_mcp_tools was called with correct parameters
            mock_get_tools.assert_called_once_with(
                connection_type="stdio",
                command="npx",
                args=["arg1", "arg2"],
                url=None,
                headers={}
            )
            
            # Verify LlmAgent was called with correct parameters
            mock_llm_agent.assert_called_once_with(
                model="test-model",
                name="test-agent",
                instruction="Test instruction",
                tools=mock_tools
            )


@pytest.mark.asyncio
async def test_build_agent_with_additional_tools():
    """Test building an agent with additional tools."""
    # Create mocks with truly distinct identities
    mock_mcp_tools = [MagicMock(name=f"mcp_tool_{i}") for i in range(2)]
    mock_additional_tools = [MagicMock(name=f"add_tool_{i}") for i in range(2)]
    mock_exit_stack = AsyncExitStack()
    mock_agent = MagicMock()
    
    # Create builder
    builder = MCPAgentBuilder()
    
    # Patch get_mcp_tools
    with patch('adktools.mcp.mcp_agent_builder.get_mcp_tools', new_callable=AsyncMock) as mock_get_tools:
        # Set up mock to return our tools and exit stack
        mock_get_tools.return_value = (mock_mcp_tools, mock_exit_stack)
        
        # Patch LlmAgent
        with patch('adktools.mcp.mcp_agent_builder.LlmAgent') as mock_llm_agent:
            # Set up mock to return our agent
            mock_llm_agent.return_value = mock_agent
            
            # Call build_agent with additional tools
            agent = await builder.build_agent(
                additional_tools=mock_additional_tools
            )
            
            # Check the result
            assert agent == mock_agent
            
            # Verify LlmAgent was called with correct tools
            mock_llm_agent.assert_called_once()
            args, kwargs = mock_llm_agent.call_args
            tools = kwargs.get('tools')
            
            # Debug output
            print("Tools passed to LlmAgent:", tools)
            print("MCP tools:", mock_mcp_tools)
            print("Additional tools:", mock_additional_tools)
            
            # Instead of checking the length, check that both sets of tools are present
            for tool in mock_mcp_tools:
                assert tool in tools, f"MCP tool {tool} not found in tools"
            for tool in mock_additional_tools:
                assert tool in tools, f"Additional tool {tool} not found in tools"
                
@pytest.mark.asyncio
async def test_cleanup():
    """Test cleanup method of MCPAgentBuilder."""
    # Create mocks
    mock_exit_stack = AsyncMock()
    
    # Create builder and set exit_stack
    builder = MCPAgentBuilder()
    builder.exit_stack = mock_exit_stack
    
    # Call cleanup
    await builder.cleanup()
    
    # Verify exit_stack.aclose was called
    mock_exit_stack.aclose.assert_called_once()
    assert builder.exit_stack is None
    
    # Test cleanup with no exit_stack
    builder = MCPAgentBuilder()
    builder.exit_stack = None
    
    # This should not raise an error
    await builder.cleanup()