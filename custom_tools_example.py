#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example demonstrating custom tool registration with OpenRouter
"""

import os
import sys
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from miniagent import MiniAgent, register_tool, get_tool_description
from miniagent.logger import get_logger

logger = get_logger("custom_tools_example")


# Define custom tools
@register_tool
def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number
    
    Args:
        n: The position in the Fibonacci sequence (starting from 0)
    
    Returns:
        The nth Fibonacci number
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


@register_tool
def text_analyzer(text: str) -> Dict:
    """
    Analyze text and return statistics
    
    Args:
        text: The text to analyze
    
    Returns:
        Dictionary with character count, word count, and sentence count
    """
    char_count = len(text)
    words = text.split()
    word_count = len(words)
    sentences = [s for s in text.split('.') if s.strip()]
    sentence_count = len(sentences)
    
    return {
        "character_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count
    }


@register_tool
def reverse_string(text: str) -> str:
    """
    Reverse a string
    
    Args:
        text: The string to reverse
    
    Returns:
        The reversed string
    """
    return text[::-1]


def main():
    """Run custom tools example"""
    
    # Load environment variables
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    # Get configuration
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.error("OPENROUTER_API_KEY not found")
        return
    
    model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
    
    logger.info(f"Initializing MiniAgent with model: {model}")
    
    # Create agent
    agent = MiniAgent(
        model=model,
        api_key=api_key,
        temperature=0.7
    )
    
    # Register custom tools
    for tool_func in [fibonacci, text_analyzer, reverse_string]:
        tool_desc = get_tool_description(tool_func)
        agent.tools.append(tool_desc)
    
    # Also add calculator for good measure
    agent.load_builtin_tool("calculator")
    
    logger.info(f"Loaded tools: {[tool['name'] for tool in agent.tools]}")
    
    # Test query
    query = """Please help me with these tasks:
1. Calculate the 10th Fibonacci number
2. Analyze this text: "The quick brown fox jumps over the lazy dog"
3. Reverse the string "OpenRouter"
4. Calculate 2^10
"""
    
    print("\n" + "="*60)
    print("MiniAgent - Custom Tools Example")
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
