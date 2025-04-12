# adktools/discovery.py
"""
Tool discovery utilities for ADK.

This module provides utilities for discovering tools decorated with @adk_tool.
"""

import inspect
from typing import Any, Callable, Iterable, List


def discover_adk_tools(module: Any) -> List[Callable]:
    """Discover all functions decorated with @adk_tool in a module.

    Args:
        module: The module to scan for ADK tools

    Returns:
        A list of functions decorated with @adk_tool

    Examples:
        # Import your tools module
        import myagent.tools

        # Discover all tools in the module
        tools = discover_adk_tools(myagent.tools)

        # Create an agent with the discovered tools
        agent = Agent(
            name="my_agent",
            tools=tools
        )
    """
    tools = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and hasattr(obj, "_is_adk_tool"):
            tools.append(obj)

    return tools


def discover_adk_tools_in_modules(modules: Iterable[Any]) -> List[Callable]:
    """Discover all functions decorated with @adk_tool across multiple modules.

    Args:
        modules: An iterable of modules to scan for ADK tools

    Returns:
        A list of functions decorated with @adk_tool

    Examples:
        # Import your tools modules
        import myagent.time_tools
        import myagent.weather_tools

        # Discover all tools across multiple modules
        tools = discover_adk_tools_in_modules([
            myagent.time_tools,
            myagent.weather_tools
        ])

        # Create an agent with the discovered tools
        agent = Agent(
            name="my_agent",
            tools=tools
        )
    """
    tools = []
    for module in modules:
        tools.extend(discover_adk_tools(module))

    return tools
