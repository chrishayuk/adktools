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

### Tool Discovery

```python
from adktools import discover_adk_tools
from google.adk.agents import Agent

# Import your modules containing tools
import myagent.weather_tools
import myagent.time_tools

# Create an agent with auto-discovered tools
agent = Agent(
    name="my_assistant",
    description="A helpful assistant",
    tools=discover_adk_tools(myagent.weather_tools)
)

# Or discover tools across multiple modules
all_tools = discover_adk_tools_in_modules([
    myagent.weather_tools,
    myagent.time_tools
])
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

### Response Models

ADK Tools provides standardized response models:

```python
from adktools.models import ErrorResponse, SuccessResponse, DomainError

# Success response
success = SuccessResponse(result={"key": "value"})
# Or without data
empty_success = SuccessResponse()  # result is optional

# Error response
error = ErrorResponse(error_message="Something went wrong")

# Domain-specific error base class
class MyCustomError(DomainError):
    error_type: Literal["custom_error"] = "custom_error"
    error_message: str  # Matches ErrorResponse field name
    additional_field: str
```

### Helper Functions

```python
from adktools import success_response, error_response

# Create success response dictionary
response = success_response({"data": "value"})
# {"status": "success", "result": {"data": "value"}}

# Create success response without data
empty_response = success_response()
# {"status": "success"}

# Create error response dictionary
response = error_response("Something went wrong")
# {"status": "error", "error_message": "Something went wrong"}
```

## Response Format

By default, ADK Tools uses the following standardized response formats:

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