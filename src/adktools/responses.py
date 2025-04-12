# adktools/responsess.py
"""
Response utilities for ADK tools.

This module provides helper functions for creating standardized responses.
"""
from typing import Any, Dict

# imports
from adktools.models import ErrorResponse, SuccessResponse


def success_response(result: Any) -> Dict[str, Any]:
    """Create a standardized success response.

    Args:
        result: The result data to include in the response.

    Returns:
        A dictionary with the standard success response format.
    """
    return SuccessResponse(result=result).model_dump()


def error_response(message: str) -> Dict[str, Any]:
    """Create a standardized error response.

    Args:
        message: The error message to include in the response.

    Returns:
        A dictionary with the standard error response format.
    """
    return ErrorResponse(error_message=message).model_dump()
