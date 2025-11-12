#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple example demonstrating MiniAgent with OpenRouter
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from miniagent import MiniAgent
from miniagent.logger import get_logger

logger = get_logger("simple_example")


def main():
    """Run a simple example with MiniAgent"""
    
    # Load environment variables
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    # Get configuration from environment
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.error("OPENROUTER_API_KEY not found in environment")
        logger.info("Please set OPENROUTER_API_KEY in your .env file or environment")
        return
    
    model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
    
    logger.info(f"Initializing MiniAgent with model: {model}")
    
    # Create agent
    agent = MiniAgent(
        model=model,
        api_key=api_key,
        temperature=0.7
    )
    
    # Load built-in tools
    agent.load_builtin_tool("calculator")
    agent.load_builtin_tool("get_current_time")
    agent.load_builtin_tool("system_info")
    
    logger.info(f"Loaded tools: {[tool['name'] for tool in agent.tools]}")
    
    # Test query
    query = "What is the current time? Also, calculate 123 * 456."
    
    print("\n" + "="*60)
    print("MiniAgent - OpenRouter Example")
    print("="*60)
    print(f"\nUser Query: {query}")
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
