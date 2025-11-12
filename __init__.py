#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MiniAgent - A lightweight LLM Agent framework
OpenRouter Compatible Version
"""

from .agent import MiniAgent
from .tools import register_tool, load_tools, get_tool_description

__version__ = "1.0.0-openrouter"

__all__ = [
    'MiniAgent',
    'register_tool',
    'load_tools',
    'get_tool_description'
]
