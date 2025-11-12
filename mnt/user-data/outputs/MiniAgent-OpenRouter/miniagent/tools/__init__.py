#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools module for MiniAgent
Provides tool registration and management
"""

import inspect
from typing import Dict, Any, Callable, Optional, get_type_hints
from functools import wraps


# Registry for custom tools
_custom_tool_registry: Dict[str, Callable] = {}


def register_tool(func: Callable) -> Callable:
    """
    Decorator to register a custom tool function
    
    The function's docstring and type hints will be used to generate
    the tool description automatically.
    
    Example:
        @register_tool
        def my_tool(param1: str, param2: int) -> str:
            '''Tool description here'''
            return "result"
    
    Args:
        func: The function to register as a tool
        
    Returns:
        The wrapped function
    """
    _custom_tool_registry[func.__name__] = func
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    return wrapper


def get_tool_description(func: Callable) -> Dict[str, Any]:
    """
    Extract tool description from a function
    
    Args:
        func: The function to describe
        
    Returns:
        Dictionary with tool name, description, and parameters
    """
    # Get function name
    name = func.__name__
    
    # Get description from docstring
    description = func.__doc__ or "No description available"
    description = description.strip()
    
    # Get type hints
    try:
        type_hints = get_type_hints(func)
    except:
        type_hints = {}
    
    # Get function signature
    sig = inspect.signature(func)
    
    # Build parameters
    parameters = {
        "type": "object",
        "properties": {},
        "required": []
    }
    
    for param_name, param in sig.parameters.items():
        if param_name == 'self':
            continue
        
        # Get type from hints
        param_type = type_hints.get(param_name, str)
        
        # Convert Python types to JSON schema types
        json_type = "string"
        if param_type == int:
            json_type = "integer"
        elif param_type == float:
            json_type = "number"
        elif param_type == bool:
            json_type = "boolean"
        elif param_type == list:
            json_type = "array"
        elif param_type == dict:
            json_type = "object"
        
        # Extract parameter description from docstring if available
        param_desc = f"Parameter {param_name}"
        if func.__doc__:
            # Simple parsing for Args section
            doc_lines = func.__doc__.split('\n')
            in_args = False
            for line in doc_lines:
                if 'Args:' in line:
                    in_args = True
                    continue
                if in_args and param_name in line:
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        param_desc = parts[1].strip()
                    break
                if in_args and line.strip() and not line.strip().startswith(param_name):
                    in_args = False
        
        parameters["properties"][param_name] = {
            "type": json_type,
            "description": param_desc
        }
        
        # Check if parameter is required (no default value)
        if param.default == inspect.Parameter.empty:
            parameters["required"].append(param_name)
    
    return {
        "name": name,
        "description": description,
        "parameters": parameters,
        "executor": func
    }


def get_custom_tool(tool_name: str) -> Optional[Callable]:
    """
    Get a custom registered tool by name
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        The tool function or None if not found
    """
    return _custom_tool_registry.get(tool_name)


def list_custom_tools() -> list:
    """
    List all registered custom tools
    
    Returns:
        List of tool names
    """
    return list(_custom_tool_registry.keys())


def load_tools(tool_names: list) -> list:
    """
    Load tools by name (both built-in and custom)
    
    Args:
        tool_names: List of tool names to load
        
    Returns:
        List of tool dictionaries
    """
    from .basic_tools import get_builtin_tool
    
    tools = []
    for name in tool_names:
        # Try built-in tools first
        tool = get_builtin_tool(name)
        if tool:
            tools.append(tool)
            continue
        
        # Try custom tools
        func = get_custom_tool(name)
        if func:
            tools.append(get_tool_description(func))
            continue
        
        print(f"Warning: Tool '{name}' not found")
    
    return tools


# Re-export commonly used functions
__all__ = [
    'register_tool',
    'get_tool_description',
    'get_custom_tool',
    'list_custom_tools',
    'load_tools'
]
