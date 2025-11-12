#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Custom tools for file system operations
"""

import os
import subprocess
from typing import List
from .tools import register_tool

@register_tool
def run_shell_command(command: str) -> str:
    """
    Executes a shell command.

    Args:
        command: The command to execute.

    Returns:
        The output of the command.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return f"Command executed successfully:\n{result.stdout}"
        else:
            return f"Error executing command:\n{result.stderr}"
    except Exception as e:
        return f"Error executing command: {e}"

@register_tool
def write_file(path: str, content: str) -> str:
    """
    Writes content to a file.

    Args:
        path: The path to the file.
        content: The content to write.

    Returns:
        A confirmation message.
    """
    try:
        with open(path, 'w') as f:
            f.write(content)
        return f"File '{path}' written successfully."
    except Exception as e:
        return f"Error writing file: {e}"

@register_tool
def read_file(path: str) -> str:
    """
    Reads the content of a file.

    Args:
        path: The path to the file.

    Returns:
        The content of the file, or an error message.
    """
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

@register_tool
def replace_text(path: str, old_text: str, new_text: str) -> str:
    """
    Replaces text in a file.

    Args:
        path: The path to the file.
        old_text: The text to replace.
        new_text: The new text.

    Returns:
        A confirmation message.
    """
    try:
        with open(path, 'r') as f:
            content = f.read()
        content = content.replace(old_text, new_text)
        with open(path, 'w') as f:
            f.write(content)
        return f"Text in '{path}' replaced successfully."
    except Exception as e:
        return f"Error replacing text: {e}"

@register_tool
def list_files_recursive(path: str) -> List[str]:
    """
    Lists all files in a directory and its subdirectories.

    Args:
        path: The path to the directory.

    Returns:
        A list of file paths.
    """
    try:
        file_list = []
        for root, _, files in os.walk(path):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list
    except Exception as e:
        return [f"Error listing files: {e}"]

@register_tool
def create_directory(path: str) -> str:
    """
    Creates a new directory.

    Args:
        path: The path to the directory to create.

    Returns:
        A confirmation message.
    """
    try:
        os.makedirs(path, exist_ok=True)
        return f"Directory '{path}' created successfully."
    except Exception as e:
        return f"Error creating directory: {e}"
