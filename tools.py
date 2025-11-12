#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool registration and discovery
"""

import inspect
import json
from typing import Callable, Dict, Any

def register_tool(func: Callable) -> Callable:
    """
    A decorator to register a function as a tool.
    It attaches the tool description to the function.
    """
    func._is_tool = True
    return func

def get_tool_description(func: Callable) -> Dict[str, Any]:
    """
    Get the description of a tool from its docstring.
    """
    if not hasattr(func, '_is_tool') or not func._is_tool:
        raise TypeError("Function is not a registered tool.")

    doc = inspect.getdoc(func)
    if not doc:
        raise ValueError("Tool function must have a docstring.")

    lines = doc.split('\n')
    description = lines[0]
    
    args_section = False
    params = {"type": "object", "properties": {}, "required": []}
    
    for line in lines[1:]:
        line = line.strip()
        if line.startswith("Args:"):
            args_section = True
            continue
        if args_section:
            if ":" in line:
                arg_name, arg_desc = line.split(":", 1)
                arg_name = arg_name.strip()
                arg_desc = arg_desc.strip()
                
                # Infer type from annotation
                arg_type = "string" # default
                if arg_name in func.__annotations__:
                    param_type = func.__annotations__[arg_name]
                    if param_type == int:
                        arg_type = "integer"
                    elif param_type == float:
                        arg_type = "number"
                    elif param_type == bool:
                        arg_type = "boolean"

                params["properties"][arg_name] = {"type": arg_type, "description": arg_desc}
                params["required"].append(arg_name)

    return {
        "name": func.__name__,
        "description": description,
        "parameters": params,
        "executor": func,
    }

def load_tools(module_name: str) -> list:
    """

    Load all tools from a module.
    """
    tools = []
    module = __import__(module_name, fromlist=['*'])
    for name in dir(module):
        obj = getattr(module, name)
        if callable(obj) and hasattr(obj, '_is_tool') and obj._is_tool:
            tools.append(get_tool_description(obj))
    return tools
