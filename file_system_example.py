#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example demonstrating the file system custom tools
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from open_agent import MiniAgent
from open_agent.logger import get_logger
from open_agent.file_system_tools import (
    write_file,
    read_file,
    replace_text,
    list_files_recursive,
    create_directory,
)
from open_agent.tools import get_tool_description

logger = get_logger("file_system_example")

def main():
    """Run file system example"""
    
    # Load environment variables
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    # Get configuration
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.error("OPENROUTER_API_KEY not found")
        return
    
    model = os.getenv("OPENROUTER_MODEL", "z-ai/glm-4.5-air:free")
    
    logger.info(f"Initializing MiniAgent with model: {model}")
    
    # Create agent
    agent = MiniAgent(
        model=model,
        api_key=api_key,
        temperature=0.7
    )
    
    # Register custom tools
    for tool_func in [write_file, read_file, replace_text, list_files_recursive, create_directory]:
        tool_desc = get_tool_description(tool_func)
        agent.tools.append(tool_desc)
    
    logger.info(f"Loaded tools: {[tool['name'] for tool in agent.tools]}")
    
    # Test query
    query = """
I need to perform some file operations. Here's what I need to do:
1. Create a new directory called 'test_dir'.
2. Create a new file in 'test_dir' called 'test_file.txt' with the content 'Hello, world!'.
3. Read the content of 'test_dir/test_file.txt'.
4. Replace the text 'world' with 'friend' in 'test_dir/test_file.txt'.
5. Read the content of 'test_dir/test_file.txt' again.
6. List all files in the 'open_agent' directory.
"""
    
    print("\n" + "="*60)
    print("MiniAgent - File System Example")
    print("="*60)
    print(f"\nUser Query:\n{query}")
    print("-"*60)
    
    # Run agent
    try:
        response = agent.run(query)
        print(f"\nAgent Response:\n{response}")
        print("="*60)
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
