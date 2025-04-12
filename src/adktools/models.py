# adktools/models.py
"""
Response models for ADK tools.

This module provides standardized response models used by ADK tools.
"""
from typing import Any, Literal, Union

from pydantic import BaseModel, Field


# Standardized response models
class ErrorResponse(BaseModel):
    """Standard error response for ADK tools."""

    status: Literal["error"] = "error"
    error_message: str = Field(..., description="Description of the error")


class SuccessResponse(BaseModel):
    """Standard success response for ADK tools."""

    status: Literal["success"] = "success"
    result: Any = Field(..., description="The result data")


# Type that represents either success or error response
ResponseType = Union[SuccessResponse, ErrorResponse]


# Base class for domain-specific error models
class DomainError(BaseModel):
    """Base class for domain-specific error models.

    Any model that inherits from this class will be automatically
    converted to an ErrorResponse by the adk_tool decorator.
    """

    error_type: str = Field(..., description="The type of error")
    message: str = Field(..., description="A user-friendly error message")
