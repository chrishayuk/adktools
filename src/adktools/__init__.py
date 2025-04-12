"""
ADK Tools - Utilities for building Agent Development Kit (ADK) applications.

This package provides tools, patterns, and utilities for building agents with
Google's Agent Development Kit (ADK).
"""

__version__ = "0.2.0"  # Bumped version for new MCP functionality

# Import main components for easy access
from adktools.decorators import adk_tool
from adktools.discovery import discover_adk_tools
from adktools.models import ErrorResponse, SuccessResponse, DomainError
from adktools.responses import error_response, success_response

# Import MCP components
import adktools.mcp

# Make these available at the top level
__all__ = [
    # Core components
    "adk_tool",
    "ErrorResponse",
    "SuccessResponse",
    "DomainError",
    "success_response",
    "error_response",
    "discover_adk_tools",
    
    # MCP subpackage
    "mcp",
]