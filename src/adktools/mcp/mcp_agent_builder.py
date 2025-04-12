# adktools/mcp/mcp_agent_builder.py
"""
MCP agent builder for ADK agents.

This module provides a builder for creating and managing MCP-enabled agents.
"""
from typing import List, Optional, Dict, Any

from google.adk.agents.llm_agent import LlmAgent
from contextlib import AsyncExitStack

# imports
from adktools.mcp.mcp_tools import get_mcp_tools


class MCPAgentBuilder:
    """Builder for creating and running MCP-enabled agents."""
    
    def __init__(
        self,
        connection_type: str = "stdio",
        command: str = "npx",
        args: Optional[List[str]] = None,
        url: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize the MCP agent builder.
        
        Args:
            connection_type: Type of connection to use ("stdio" or "sse")
            command: Command to run for stdio connections
            args: Arguments for the command
            url: URL for SSE server connections
            headers: Headers for SSE server connections
        """
        self.connection_type = connection_type
        self.command = command
        self.args = args or []
        self.url = url
        self.headers = headers or {}
        self.agent = None
        self.exit_stack = None
        
    async def build_agent(
        self,
        model: str = "gemini-2.0-flash",
        name: str = "mcp_agent",
        instruction: str = "Help the user with their tasks.",
        additional_tools: Optional[List[Any]] = None,
    ) -> LlmAgent:
        """
        Build an LLM agent with MCP tools.
        """
        # Get MCP tools
        mcp_tools, self.exit_stack = await get_mcp_tools(
            connection_type=self.connection_type,
            command=self.command,
            args=self.args,
            url=self.url,
            headers=self.headers,
        )
        
        # Combine with additional tools if provided
        tools = list(mcp_tools)  # Create a new list to avoid reference issues
        if additional_tools:
            tools.extend(additional_tools)
            
        # Create the agent
        self.agent = LlmAgent(
            model=model,
            name=name,
            instruction=instruction,
            tools=tools,
        )
        
        return self.agent
    
    async def cleanup(self):
        """Clean up MCP server connection."""
        if self.exit_stack:
            await self.exit_stack.aclose()
            self.exit_stack = None