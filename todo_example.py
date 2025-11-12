#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example demonstrating the to-do list custom tool
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from open_agent import MiniAgent
from open_agent.logger import get_logger
from open_agent.todo_tools import create_todo_list, add_todo_item, view_todo_list, mark_item_complete
from open_agent.tools import get_tool_description

logger = get_logger("todo_example")

def main():
    """Run to-do list example"""
    
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
    for tool_func in [create_todo_list, add_todo_item, view_todo_list, mark_item_complete]:
        tool_desc = get_tool_description(tool_func)
        agent.tools.append(tool_desc)
    
    logger.info(f"Loaded tools: {[tool['name'] for tool in agent.tools]}")
    
    # Test query
    query = """
I need to manage my tasks. Here's what I need to do:
1. Create a new to-do list called 'My Tasks'.
2. Add the following items to the list: 'Buy groceries', 'Finish report', 'Call mom'.
3. Show me my to-do list.
4. Mark 'Buy groceries' as complete.
5. Show me my to-do list again.
"""
    
    print("\n" + "="*60)
    print("MiniAgent - To-Do List Example")
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
