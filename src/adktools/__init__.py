# adktools/__init__.py
"""
ADK Tools - Utilities for building Agent Development Kit (ADK) applications.

This package provides tools, patterns, and utilities for building agents with
Google's Agent Development Kit (ADK).
"""

__version__ = "0.1.0"

# Import main components for easy access
from adktools.decorators import adk_tool
from adktools.discovery import discover_adk_tools
from adktools.models import ErrorResponse, SuccessResponse
from adktools.responses import error_response, success_response

# Make these available at the top level
__all__ = [
    "adk_tool",
    "ErrorResponse",
    "SuccessResponse",
    "success_response",
    "error_response",
    "discover_adk_tools",
]
