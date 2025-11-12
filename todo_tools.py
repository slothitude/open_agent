#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Custom tools for managing a to-do list
"""

from typing import Dict, List, Any
from .tools import register_tool, get_tool_description

# In-memory storage for to-do lists
TODO_LISTS: Dict[str, List[Dict[str, Any]]] = {}

@register_tool
def create_todo_list(list_name: str) -> str:
    """
    Creates a new to-do list.

    Args:
        list_name: The name of the to-do list.

    Returns:
        A confirmation message.
    """
    if list_name in TODO_LISTS:
        return f"Error: To-do list '{list_name}' already exists."
    TODO_LISTS[list_name] = []
    return f"To-do list '{list_name}' created successfully."

@register_tool
def add_todo_item(list_name: str, item: str) -> str:
    """
    Adds an item to a to-do list.

    Args:
        list_name: The name of the to-do list.
        item: The item to add.

    Returns:
        A confirmation message.
    """
    if list_name not in TODO_LISTS:
        return f"Error: To-do list '{list_name}' not found."
    TODO_LISTS[list_name].append({"task": item, "completed": False})
    return f"Item '{item}' added to to-do list '{list_name}'."

@register_tool
def view_todo_list(list_name: str) -> str:
    """
    Views the items in a to-do list.

    Args:
        list_name: The name of the to-do list.

    Returns:
        A string representation of the to-do list.
    """
    if list_name not in TODO_LISTS:
        return f"Error: To-do list '{list_name}' not found."
    
    if not TODO_LISTS[list_name]:
        return f"To-do list '{list_name}' is empty."

    output = f"To-do list '{list_name}':\n"
    for i, item in enumerate(TODO_LISTS[list_name]):
        status = "✓" if item["completed"] else " "
        output += f"{i + 1}. [{status}] {item['task']}\n"
    return output

@register_tool
def mark_item_complete(list_name: str, item_number: int) -> str:
    """
    Marks an item in a to-do list as complete.

    Args:
        list_name: The name of the to-do list.
        item_number: The number of the item to mark as complete.

    Returns:
        A confirmation message.
    """
    if list_name not in TODO_LISTS:
        return f"Error: To-do list '{list_name}' not found."
    
    if not (1 <= item_number <= len(TODO_LISTS[list_name])):
        return f"Error: Invalid item number. Please choose a number between 1 and {len(TODO_LISTS[list_name])}."

    TODO_LISTS[list_name][item_number - 1]["completed"] = True
    item_text = TODO_LISTS[list_name][item_number - 1]['task']
    return f"Item '{item_text}' in to-do list '{list_name}' marked as complete."

def get_todo_tools():
    """Returns a list of all to-do tool descriptions."""
    return [
        get_tool_description(create_todo_list),
        get_tool_description(add_todo_item),
        get_tool_description(view_todo_list),
        get_tool_description(mark_item_complete),
    ]
