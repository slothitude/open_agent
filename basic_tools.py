#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Built-in tools for MiniAgent
"""

import platform
import datetime
import ast
import operator
from typing import Dict, Any, Optional


def calculator(expression: str) -> float:
    """
    Safely evaluate a mathematical expression
    
    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 2", "3.14 * 2")
    
    Returns:
        Result of the calculation
    """
    # Define safe operations
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
    }
    
    def eval_expr(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            left = eval_expr(node.left)
            right = eval_expr(node.right)
            return operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = eval_expr(node.operand)
            return operators[type(node.op)](operand)
        else:
            raise ValueError(f"Unsupported expression: {ast.dump(node)}")
    
    try:
        tree = ast.parse(expression, mode='eval')
        result = eval_expr(tree.body)
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid mathematical expression: {str(e)}")


def get_current_time(timezone: str = "UTC") -> str:
    """
    Get the current date and time
    
    Args:
        timezone: Timezone (currently only UTC is supported)
    
    Returns:
        Current datetime as a formatted string
    """
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def system_info() -> Dict[str, str]:
    """
    Get system information
    
    Returns:
        Dictionary containing system information
    """
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version()
    }


# Tool registry with descriptions
BUILTIN_TOOLS = {
    "calculator": {
        "name": "calculator",
        "description": "Safely evaluate a mathematical expression. Supports basic arithmetic operations (+, -, *, /, **, %).",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate (e.g., '2 + 2', '3.14 * 2', '10 ** 2')"
                }
            },
            "required": ["expression"]
        },
        "executor": calculator
    },
    "get_current_time": {
        "name": "get_current_time",
        "description": "Get the current date and time in a specified timezone.",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "Timezone (default: UTC)",
                    "default": "UTC"
                }
            },
            "required": []
        },
        "executor": get_current_time
    },
    "system_info": {
        "name": "system_info",
        "description": "Get information about the current system including OS, version, and Python version.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "executor": system_info
    }
}


def get_builtin_tool(tool_name: str) -> Optional[Dict[str, Any]]:
    """
    Get a built-in tool by name
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        Tool dictionary or None if not found
    """
    return BUILTIN_TOOLS.get(tool_name)


def list_builtin_tools() -> list:
    """
    List all available built-in tools
    
    Returns:
        List of tool names
    """
    return list(BUILTIN_TOOLS.keys())
