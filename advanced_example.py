#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advanced example with multiple custom tools
Demonstrates building a more complex agent
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from miniagent import MiniAgent, register_tool, get_tool_description
from miniagent.logger import get_logger

logger = get_logger("advanced_example")


# Advanced custom tools
@register_tool
def search_knowledge_base(query: str) -> str:
    """
    Search a simulated knowledge base for information
    
    Args:
        query: The search query
    
    Returns:
        Relevant information from the knowledge base
    """
    # Simulated knowledge base
    knowledge_base = {
        "python": "Python is a high-level programming language known for readability and versatility.",
        "openrouter": "OpenRouter is a unified API that provides access to 100+ AI models.",
        "agents": "AI agents are autonomous systems that can perceive, reason, and act to achieve goals.",
        "react": "ReAct (Reason+Act) is a pattern where AI models alternate between reasoning and taking actions."
    }
    
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return f"Found information: {value}"
    
    return f"No specific information found for '{query}'"


@register_tool
def create_summary(text: str, max_words: int = 50) -> str:
    """
    Create a summary of the given text
    
    Args:
        text: The text to summarize
        max_words: Maximum number of words in summary (default: 50)
    
    Returns:
        A summarized version of the text
    """
    words = text.split()
    if len(words) <= max_words:
        return text
    
    # Simple summary: take first max_words words
    summary = ' '.join(words[:max_words]) + "..."
    return summary


@register_tool
def list_operations(numbers: List[float], operation: str) -> float:
    """
    Perform operations on a list of numbers
    
    Args:
        numbers: List of numbers to operate on
        operation: Operation to perform (sum, average, max, min)
    
    Returns:
        Result of the operation
    """
    if not numbers:
        return 0.0
    
    operation = operation.lower()
    if operation == "sum":
        return sum(numbers)
    elif operation == "average" or operation == "mean":
        return sum(numbers) / len(numbers)
    elif operation == "max":
        return max(numbers)
    elif operation == "min":
        return min(numbers)
    else:
        return 0.0


@register_tool
def format_data(data: Dict, format_type: str = "json") -> str:
    """
    Format data in different formats
    
    Args:
        data: Dictionary data to format
        format_type: Output format (json, text)
    
    Returns:
        Formatted string
    """
    if format_type.lower() == "json":
        return json.dumps(data, indent=2)
    else:
        # Text format
        result = []
        for key, value in data.items():
            result.append(f"{key}: {value}")
        return "\n".join(result)


def main():
    """Run advanced example"""
    
    # Load environment
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.error("OPENROUTER_API_KEY not found")
        return
    
    model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
    
    logger.info(f"Initializing advanced MiniAgent with model: {model}")
    
    # Create agent with custom system prompt
    agent = MiniAgent(
        model=model,
        api_key=api_key,
        temperature=0.7,
        system_prompt="""You are a helpful research assistant with access to various tools.
Your goal is to provide comprehensive, accurate answers by using the available tools effectively.

When you need information:
1. Search the knowledge base first
2. Perform calculations or data operations as needed
3. Format your results clearly
4. Provide a well-structured final answer

Always explain your reasoning and show your work."""
    )
    
    # Register all custom tools
    for tool_func in [search_knowledge_base, create_summary, list_operations, format_data]:
        tool_desc = get_tool_description(tool_func)
        agent.tools.append(tool_desc)
    
    # Add built-in tools
    agent.load_builtin_tool("calculator")
    agent.load_builtin_tool("get_current_time")
    
    logger.info(f"Loaded {len(agent.tools)} tools: {[tool['name'] for tool in agent.tools]}")
    
    # Complex query
    query = """I need help with a research task:

1. Search for information about 'ReAct' pattern in AI
2. Calculate the average of these numbers: [10, 20, 30, 40, 50]
3. Get the current time
4. Format this data as JSON: {"task": "research", "status": "complete", "tools_used": 4}

Please provide a comprehensive summary of what you found and did."""
    
    print("\n" + "="*70)
    print("MiniAgent - Advanced Example with Multiple Tools")
    print("="*70)
    print(f"\nUser Query:\n{query}")
    print("-"*70)
    
    # Run agent
    try:
        response = agent.run(query)
        print(f"\nAgent Response:\n{response}")
        print("="*70)
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
