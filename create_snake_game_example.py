#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example demonstrating the agent's ability to create the snake game.
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
    run_shell_command,
)
from open_agent.tools import get_tool_description

logger = get_logger("create_snake_game_example")

def main():
    """Run the create snake game example"""
    
    # Load environment variables
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    # Get configuration
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.error("OPENROUTER_API_KEY not found")
        return
    
    model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku")
    
    logger.info(f"Initializing MiniAgent with model: {model}")
    
    # Create agent
    agent = MiniAgent(
        model=model,
        api_key=api_key,
        temperature=0.7
    )
    
    # Register custom tools
    for tool_func in [write_file, read_file, replace_text, list_files_recursive, create_directory, run_shell_command]:
        tool_desc = get_tool_description(tool_func)
        agent.tools.append(tool_desc)
    
    logger.info(f"Loaded tools: {[tool['name'] for tool in agent.tools]}")
    
    # Test query
    query = """
I want you to create a snake game using pygame. Here are the steps:
1. Create a new directory called 'mini_agent_snake_game'.
2. Create a file inside this new directory called 'main.py'.
3. Write the python code for a snake game using pygame and save it to 'mini_agent_snake_game/main.py'. The game should have a window size of 600x400, a black snake, and green food. The game should end when the snake hits the wall or itself.
4. Create a file called 'mini_agent_snake_game/requirements.txt' and add 'pygame' to it.
5. Install the dependencies using pip.
6. Run the game.
"""
    
    print("\n" + "="*60)
    print("MiniAgent - Create Snake Game Example")
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
