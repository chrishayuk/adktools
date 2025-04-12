# adktools/decorators.py
"""
Decorators for ADK tools.

This module provides the adk_tool decorator for standardizing tool functions.
"""

import inspect
import traceback
from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar, Union, cast

from pydantic import BaseModel, ValidationError

from adktools.responses import error_response, success_response

# Type variables for better typing
T = TypeVar("T")
FuncType = TypeVar("FuncType", bound=Callable[..., Any])


def adk_tool(
    func: Optional[Callable] = None,
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    detailed_errors: bool = False,
) -> Union[Callable[[FuncType], FuncType], FuncType]:
    """Decorator for ADK tool functions that standardizes response handling and metadata.

    This decorator:
    1. Provides structured success and error responses
    2. Handles domain-specific error models
    3. Catches unexpected exceptions as a safety net
    4. Allows customizing tool name and description

    Args:
        func: The function to decorate (when used without parameters)
        name: Optional custom name for the tool
        description: Optional custom description for the tool
        detailed_errors: Whether to include stack traces in error responses (default: False)

    Returns:
        Decorated function that provides standardized ADK responses and tool metadata

    Examples:
        # Basic usage
        @adk_tool
        def get_weather(location: str):
            # function implementation
            ...

        # With custom metadata
        @adk_tool(name="get_time", description="Get current time")
        def get_current_time(timezone: str):
            # function implementation
            ...
    """

    def decorator(fn: FuncType) -> FuncType:
        @wraps(fn)
        def wrapper(*args, **kwargs) -> Dict[str, Any]:
            try:
                # Call the original function
                result = fn(*args, **kwargs)

                # If the result is already a dict with status, assume it's already formatted
                if isinstance(result, dict) and "status" in result:
                    return result

                # Check for special error models - any model with 'error_type' attribute
                # will be converted to an error response
                if isinstance(result, BaseModel) and hasattr(result, "error_type"):
                    # Create an error response based on the domain error model
                    error_msg = getattr(result, "message", str(result))
                    return error_response(error_msg)

                # If the result is a Pydantic model (but not an error model), convert it to dict
                if isinstance(result, BaseModel):
                    result = result.model_dump()

                # Return success response
                return success_response(result)

            except ValidationError as e:
                # Handle validation errors
                error_msg = f"Validation error: {str(e)}"
                if detailed_errors:
                    error_msg += f"\n{traceback.format_exc()}"
                return error_response(error_msg)

            except Exception as e:
                # Handle other exceptions (safety net)
                error_msg = f"Error: {str(e)}"
                if detailed_errors:
                    error_msg += f"\n{traceback.format_exc()}"
                return error_response(error_msg)

        # Set tool metadata if provided
        if name:
            wrapper.__name__ = name
        if description:
            wrapper.__doc__ = description

        # Mark this function as an ADK tool for potential discovery
        wrapper._is_adk_tool = True
        wrapper._adk_tool_name = name or fn.__name__
        wrapper._adk_tool_description = description or inspect.getdoc(fn)

        return cast(FuncType, wrapper)

    # Handle both @adk_tool and @adk_tool(name="xyz") syntax
    if func is not None:
        return decorator(func)
    return decorator
