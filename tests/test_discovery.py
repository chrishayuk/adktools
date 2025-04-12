"""Tests for the tool discovery functions."""

import types

from adktools import adk_tool
from adktools.discovery import discover_adk_tools, discover_adk_tools_in_modules


# Create test modules dynamically
def create_test_module(name, num_tools=2, num_regular_functions=1):
    """Create a test module with ADK tools and regular functions."""
    module = types.ModuleType(name)

    # Add ADK tools
    for i in range(num_tools):

        @adk_tool
        def tool_func(param: str):
            return param

        tool_name = f"tool_{i}"
        tool_func.__name__ = tool_name
        setattr(module, tool_name, tool_func)

    # Add regular functions
    for i in range(num_regular_functions):

        def regular_func(param: str):
            return param

        func_name = f"func_{i}"
        regular_func.__name__ = func_name
        setattr(module, func_name, regular_func)

    return module


def test_discover_adk_tools():
    """Test discovering ADK tools in a module."""
    # Create test module with 3 tools and 2 regular functions
    module = create_test_module("test_module", num_tools=3, num_regular_functions=2)

    # Discover tools
    tools = discover_adk_tools(module)

    # Should find exactly the 3 ADK tools
    assert len(tools) == 3

    # All discovered functions should be marked as ADK tools
    for tool in tools:
        assert hasattr(tool, "_is_adk_tool")
        assert tool._is_adk_tool is True


def test_discover_adk_tools_in_modules():
    """Test discovering ADK tools across multiple modules."""
    # Create test modules
    module1 = create_test_module("module1", num_tools=2, num_regular_functions=1)
    module2 = create_test_module("module2", num_tools=3, num_regular_functions=2)

    # Discover tools across both modules
    tools = discover_adk_tools_in_modules([module1, module2])

    # Should find all 5 tools from both modules
    assert len(tools) == 5

    # All discovered functions should be marked as ADK tools
    for tool in tools:
        assert hasattr(tool, "_is_adk_tool")
        assert tool._is_adk_tool is True


def test_empty_module():
    """Test discovering ADK tools in a module with no tools."""
    # Create module with no tools
    module = create_test_module("empty_module", num_tools=0, num_regular_functions=2)

    # Should find no tools
    tools = discover_adk_tools(module)
    assert len(tools) == 0
