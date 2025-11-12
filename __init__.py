#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MiniAgent - A lightweight LLM Agent framework
OpenRouter Compatible Version
"""

from .agent import MiniAgent
from .tools import register_tool, load_tools, get_tool_description
from .todo_tools import get_todo_tools
from .file_system_tools import (
    write_file,
    read_file,
    replace_text,
    list_files_recursive,
    create_directory,
    run_shell_command,
)

__version__ = "1.0.0-openrouter"

__all__ = [
    'MiniAgent',
    'register_tool',
    'load_tools',
    'get_tool_description',
    'get_todo_tools',
    'write_file',
    'read_file',
    'replace_text',
    'list_files_recursive',
    'create_directory',
    'run_shell_command',
]
