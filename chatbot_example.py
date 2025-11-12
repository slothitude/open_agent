#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interactive chatbot example with conversation history
Demonstrates multi-turn conversations with tool usage
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from miniagent import MiniAgent
from miniagent.logger import get_logger

logger = get_logger("chatbot")


class ChatBot:
    """Interactive chatbot with conversation history"""
    
    def __init__(self, agent: MiniAgent):
        self.agent = agent
        self.conversation_history = []
    
    def chat(self, user_input: str) -> str:
        """
        Send a message and get a response
        
        Args:
            user_input: User's message
            
        Returns:
            Agent's response
        """
        # For simplicity, we'll use the agent's run method
        # In a production system, you'd maintain full conversation context
        response = self.agent.run(user_input)
        
        # Store in history
        self.conversation_history.append({
            "user": user_input,
            "assistant": response
        })
        
        return response
    
    def show_history(self):
        """Display conversation history"""
        if not self.conversation_history:
            print("No conversation history yet.")
            return
        
        print("\n" + "="*60)
        print("Conversation History")
        print("="*60)
        for i, turn in enumerate(self.conversation_history, 1):
            print(f"\nTurn {i}:")
            print(f"You: {turn['user']}")
            print(f"Bot: {turn['assistant'][:200]}..." if len(turn['assistant']) > 200 else f"Bot: {turn['assistant']}")
        print("="*60)


def main():
    """Run interactive chatbot"""
    
    # Load environment
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in .env file")
        return
    
    model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
    
    print("\n" + "="*60)
    print("MiniAgent Interactive ChatBot")
    print("="*60)
    print(f"Model: {model}")
    print("\nCommands:")
    print("  Type your message to chat")
    print("  'history' - Show conversation history")
    print("  'tools' - Show available tools")
    print("  'quit' or 'exit' - Exit the chatbot")
    print("="*60)
    
    # Create agent
    agent = MiniAgent(
        model=model,
        api_key=api_key,
        temperature=0.7,
        system_prompt="""You are a helpful AI assistant with access to tools.
You can help with calculations, time queries, system information, and general questions.
Be friendly, concise, and helpful."""
    )
    
    # Load tools
    agent.load_builtin_tool("calculator")
    agent.load_builtin_tool("get_current_time")
    agent.load_builtin_tool("system_info")
    
    print(f"\n✓ Loaded {len(agent.tools)} tools")
    
    # Create chatbot
    chatbot = ChatBot(agent)
    
    # Main loop
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'history':
                chatbot.show_history()
                continue
            
            if user_input.lower() == 'tools':
                print("\n📦 Available Tools:")
                for tool in agent.tools:
                    print(f"  - {tool['name']}: {tool['description']}")
                continue
            
            # Get response
            print("\n🤖 Bot: ", end="", flush=True)
            try:
                response = chatbot.chat(user_input)
                print(response)
            except Exception as e:
                print(f"\n❌ Error: {e}")
                logger.error(f"Chat error: {e}", exc_info=True)
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break


if __name__ == "__main__":
    main()
