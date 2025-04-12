# ADK Tools

[![PyPI version](https://badge.fury.io/py/adktools.svg)](https://badge.fury.io/py/adktools)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A collection of utilities and patterns for building agents with Google's Agent Development Kit (ADK).

## Installation

```bash
pip install adktools
```

## Features

- **`@adk_tool` decorator**: Standardize your ADK tools with consistent error handling and response formatting
- **Domain error models**: Create rich, domain-specific error types that automatically convert to standard responses
- **Tool discovery**: Automatically find all tool functions in your modules
- **Response utilities**: Standardized success and error response generation
- **MCP integration**: Utilities for working with Model Context Protocol (MCP) servers
- **Type safety**: Comprehensive typing support for better IDE integration

## Quick Start

### Basic Tool Creation

```python
from adktools import adk_tool
from pydantic import BaseModel

class WeatherResult(BaseModel):
    location: str
    temperature: float
    conditions: str

@adk_tool
def get_weather(location: str) -> WeatherResult:
    """Get current weather for a location."""
    # Your implementation here
    return WeatherResult(
        location=location,
        temperature=72.5,
        conditions="Sunny"
    )
```

### Domain-Specific Error Handling

```python
from adktools import adk_tool
from adktools.models import DomainError
from typing import Literal, Union
from pydantic import BaseModel

class TimeResult(BaseModel):
    timezone: str
    datetime: str
    is_dst: bool

class InvalidTimezoneError(DomainError):
    timezone: str
    error_type: Literal["invalid_timezone"] = "invalid_timezone"

@adk_tool(
    name="get_time",
    description="Get the current time in a specified timezone."
)
def get_current_time(timezone: str) -> Union[TimeResult, InvalidTimezoneError]:
    try:
        # Implementation...
        if timezone == "invalid":
            return InvalidTimezoneError(
                timezone=timezone,
                error_message=f"Unknown timezone: {timezone}"
            )
        
        return TimeResult(
            timezone=timezone,
            datetime="2025-04-12T12:34:56",
            is_dst=True
        )
    except Exception as e:
        # The decorator will catch and format any exceptions
        raise RuntimeError(f"Error getting time: {str(e)}")
```

### Using MCP Tools

```python
import asyncio
from adktools.mcp import get_mcp_tools
from google.adk.agents.llm_agent import LlmAgent

async def main():
    # Get tools from an MCP server
    tools, exit_stack = await get_mcp_tools(
        connection_type="stdio",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "./data"]
    )
    
    try:
        # Create an agent with these tools
        agent = LlmAgent(
            model="gemini-2.0-flash",
            name="filesystem_agent",
            instruction="Help the user interact with files.",
            tools=tools
        )
        
        # Use the agent here
        # ...
    
    finally:
        # Clean up
        await exit_stack.aclose()

if __name__ == "__main__":
    asyncio.run(main())
```

### Using the MCP Agent Builder

```python
import asyncio
from adktools.mcp import MCPAgentBuilder
from adktools import adk_tool

# Define a custom tool
@adk_tool
def analyze_text(text: str) -> dict:
    word_count = len(text.split())
    return {
        "word_count": word_count,
        "char_count": len(text)
    }

async def main():
    # Create an MCP agent builder
    builder = MCPAgentBuilder(
        connection_type="stdio",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "./data"]
    )
    
    try:
        # Build agent with our custom tool
        agent = await builder.build_agent(
            model="gemini-2.0-flash",
            name="advanced_fs_agent",
            instruction="Help the user with files and analyze text.",
            additional_tools=[analyze_text]
        )
        
        # Use the agent here
        # ...
    
    finally:
        await builder.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation

### The `@adk_tool` Decorator

The decorator standardizes ADK tool responses and provides additional metadata for tools:

```python
@adk_tool  # Simple usage
def simple_tool(param: str):
    # Implementation...

@adk_tool(
    name="custom_name",  # Override function name
    description="Custom description",  # Override docstring
    detailed_errors=True  # Include stack traces in errors
)
def custom_tool(param: str):
    # Implementation...
```

### MCP Integration

ADK Tools provides utilities for working with Model Context Protocol (MCP) servers:

```python
# Low-level MCP tools access
from adktools.mcp import get_mcp_tools

tools, exit_stack = await get_mcp_tools(
    connection_type="stdio",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "./data"]
)

# Higher-level builder pattern
from adktools.mcp import MCPAgentBuilder

builder = MCPAgentBuilder(
    connection_type="stdio",  # or "sse" for remote servers
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "./data"]
)
agent = await builder.build_agent()
```

## Response Format

ADK Tools uses the following standardized response formats:

### Success Response
```json
{
  "status": "success",
  "result": { ... } // Optional result data
}
```

### Error Response
```json
{
  "status": "error",
  "error_message": "Description of what went wrong"
}
```

This consistent response format makes it easy for agents to handle tool responses predictably.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.