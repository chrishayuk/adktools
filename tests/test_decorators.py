"""Tests for the adk_tool decorator."""

from pydantic import BaseModel

from adktools import adk_tool
from adktools.models import DomainError


# Test models (renamed to avoid pytest warnings)
class ResultModel(BaseModel):
    value: str


class ErrorModel(DomainError):
    error_type: str = "test_error"
    param: str


# Test functions with decorator
@adk_tool
def simple_tool(param: str) -> ResultModel:
    """A simple test tool."""
    if param == "error":
        raise ValueError("Error occurred")
    return ResultModel(value=param)


@adk_tool(name="custom_name", description="Custom description")
def custom_tool(param: str) -> ResultModel:
    """Original description."""
    return ResultModel(value=param)


@adk_tool
def error_model_tool(param: str) -> ResultModel | ErrorModel:
    """Tool returning domain error model."""
    if param == "error":
        return ErrorModel(param=param, message="Error occurred")
    return ResultModel(value=param)


def test_successful_result():
    """Test that successful results are properly wrapped."""
    result = simple_tool("test")
    assert result["status"] == "success"
    assert result["result"]["value"] == "test"


def test_exception_handling():
    """Test that exceptions are caught and formatted."""
    result = simple_tool("error")
    assert result["status"] == "error"
    assert "Error occurred" in result["error_message"]


def test_metadata_override():
    """Test that name and description are properly overridden."""
    assert custom_tool.__name__ == "custom_name"
    assert custom_tool.__doc__ == "Custom description"


def test_tool_marking():
    """Test that functions are marked as ADK tools."""
    assert hasattr(simple_tool, "_is_adk_tool")
    assert simple_tool._is_adk_tool is True
    assert simple_tool._adk_tool_name == "simple_tool"
    assert "A simple test tool" in simple_tool._adk_tool_description


def test_domain_error_handling():
    """Test that domain error models are properly converted."""
    result = error_model_tool("test")
    assert result["status"] == "success"
    assert result["result"]["value"] == "test"

    result = error_model_tool("error")
    assert result["status"] == "error"
    assert "Error occurred" in result["error_message"]
