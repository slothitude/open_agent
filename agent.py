#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MiniAgent - OpenRouter Compatible Version
A lightweight LLM Agent framework that works with OpenRouter API
"""

import json
import re
from typing import List, Dict, Any, Optional, Callable
import requests
from .logger import get_logger

logger = get_logger("miniagent")


class MiniAgent:
    """
    A lightweight LLM Agent that can use tools via OpenRouter API
    
    This agent uses a ReAct-style approach where the LLM thinks, acts, and observes
    in a loop until it can provide a final answer.
    """
    
    def __init__(
        self,
        model: str = "anthropic/claude-3.5-sonnet",
        api_key: str = "",
        base_url: str = "https://api.openrouter.ai/api/v1",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None,
        use_reflector: bool = False,
        max_iterations: int = 10
    ):
        """
        Initialize MiniAgent with OpenRouter configuration
        
        Args:
            model: Model identifier (e.g., "anthropic/claude-3.5-sonnet", "openai/gpt-4")
            api_key: OpenRouter API key
            base_url: OpenRouter API base URL
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            system_prompt: Custom system prompt (optional)
            use_reflector: Enable reflection on tool usage (optional)
            max_iterations: Maximum number of reasoning iterations
        """
        self.model = model
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.use_reflector = use_reflector
        self.max_iterations = max_iterations
        self.tools: List[Dict] = []
        
        # Default system prompt if none provided
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        
        logger.info(f"Initialized MiniAgent with model: {model}")
    
    def _get_default_system_prompt(self) -> str:
        """Get the default system prompt for the agent"""
        return """You are a helpful AI assistant that can use tools to answer questions.

When you need to use a tool, respond in this exact format:

Thought: [Your reasoning about what to do next]
Action: [tool_name]
Action Input: [JSON input for the tool]

After using a tool, you will receive:
Observation: [Result from the tool]

Then continue reasoning until you have enough information to answer.

When you have the final answer, respond in this format:

Thought: I now have enough information to answer
Final Answer: [Your complete answer to the user]

Important:
- Always use the exact format shown above
- Action Input must be valid JSON
- Keep iterating until you can provide a Final Answer
- Use tools when you need external information or computation"""
    
    def _build_tool_descriptions(self) -> str:
        """Build a formatted description of available tools"""
        if not self.tools:
            return "No tools available."
        
        tool_desc = "Available Tools:\n\n"
        for tool in self.tools:
            tool_desc += f"Tool: {tool['name']}\n"
            tool_desc += f"Description: {tool['description']}\n"
            tool_desc += f"Parameters: {json.dumps(tool['parameters'], indent=2)}\n\n"
        
        return tool_desc
    
    def _call_llm(self, messages: List[Dict[str, str]]) -> str:
        """
        Call the OpenRouter API
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            The assistant's response text
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/miniagent",  # Optional, for rankings
            "X-Title": "MiniAgent"  # Optional, for rankings
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed: {e}")
            raise
    
    def _parse_action(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Parse the LLM's response to extract action and input
        
        Args:
            text: The LLM's response text
            
        Returns:
            Dictionary with 'action', 'action_input', and 'thought' or None
        """
        # Look for Action and Action Input
        action_match = re.search(r'Action:\s*(\w+)', text, re.IGNORECASE)
        action_input_match = re.search(r'Action Input:\s*(\{.*?\}|\[.*?\]|".*?"|\d+)', text, re.IGNORECASE | re.DOTALL)
        thought_match = re.search(r'Thought:\s*(.*?)(?=\nAction:|$)', text, re.IGNORECASE | re.DOTALL)
        
        if action_match:
            action = action_match.group(1).strip()
            thought = thought_match.group(1).strip() if thought_match else ""
            
            # Parse action input
            action_input = {}
            if action_input_match:
                input_str = action_input_match.group(1).strip()
                try:
                    # Try to parse as JSON
                    action_input = json.loads(input_str)
                except json.JSONDecodeError:
                    # If not JSON, use as string
                    action_input = {"input": input_str.strip('"')}
            
            return {
                "action": action,
                "action_input": action_input,
                "thought": thought
            }
        
        return None
    
    def _check_final_answer(self, text: str) -> Optional[str]:
        """
        Check if the response contains a final answer
        
        Args:
            text: The LLM's response text
            
        Returns:
            The final answer if found, None otherwise
        """
        final_answer_match = re.search(r'Final Answer:\s*(.*)', text, re.IGNORECASE | re.DOTALL)
        if final_answer_match:
            return final_answer_match.group(1).strip()
        return None
    
    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """
        Execute a tool by name with given input
        
        Args:
            tool_name: Name of the tool to execute
            tool_input: Input parameters for the tool
            
        Returns:
            Result from the tool execution
        """
        # Find the tool
        tool = None
        for t in self.tools:
            if t['name'] == tool_name:
                tool = t
                break
        
        if not tool:
            return f"Error: Tool '{tool_name}' not found. Available tools: {[t['name'] for t in self.tools]}"
        
        try:
            logger.info(f"Executing tool: {tool_name} with input: {tool_input}")
            result = tool['executor'](**tool_input)
            logger.info(f"Tool result: {result}")
            return str(result)
        except Exception as e:
            error_msg = f"Error executing tool {tool_name}: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def run(self, query: str, tools: Optional[List[Dict]] = None) -> str:
        """
        Run the agent on a query using ReAct loop
        
        Args:
            query: User's question or task
            tools: Optional list of tools (uses self.tools if not provided)
            
        Returns:
            The agent's final answer
        """
        if tools is not None:
            self.tools = tools
        
        # Build system message with tool descriptions
        system_message = self.system_prompt
        if self.tools:
            system_message += "\n\n" + self._build_tool_descriptions()
        
        # Initialize conversation
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ]
        
        # ReAct loop
        for iteration in range(self.max_iterations):
            logger.info(f"--- Iteration {iteration + 1} ---")
            
            # Get LLM response
            response = self._call_llm(messages)
            logger.info(f"LLM Response:\n{response}")
            
            # Check for final answer
            final_answer = self._check_final_answer(response)
            if final_answer:
                logger.info("Final answer received")
                return final_answer
            
            # Parse action
            action_info = self._parse_action(response)
            if action_info:
                # Execute the action
                observation = self._execute_tool(
                    action_info['action'],
                    action_info['action_input']
                )
                
                # Add to conversation
                messages.append({"role": "assistant", "content": response})
                messages.append({"role": "user", "content": f"Observation: {observation}"})
            else:
                # No action found, might be conversational or needs clarification
                if "final answer" not in response.lower() and iteration < self.max_iterations - 1:
                    # Prompt for proper format
                    messages.append({"role": "assistant", "content": response})
                    messages.append({
                        "role": "user", 
                        "content": "Please respond in the required format with either an Action or Final Answer."
                    })
                else:
                    # Last iteration or seems like an answer
                    return response
        
        # Max iterations reached
        logger.warning(f"Max iterations ({self.max_iterations}) reached")
        return "I apologize, but I couldn't complete the task within the maximum number of steps. Please try rephrasing your question or breaking it into smaller parts."
    
    def load_builtin_tool(self, tool_name: str):
        """
        Load a built-in tool by name
        
        Args:
            tool_name: Name of the built-in tool to load
        """
        from .tools.basic_tools import get_builtin_tool
        tool = get_builtin_tool(tool_name)
        if tool:
            self.tools.append(tool)
            logger.info(f"Loaded built-in tool: {tool_name}")
        else:
            logger.warning(f"Built-in tool not found: {tool_name}")
    
    def chat(self, message: str) -> str:
        """
        Simple chat without tool usage (for convenience)
        
        Args:
            message: User message
            
        Returns:
            Assistant's response
        """
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": message}
        ]
        return self._call_llm(messages)
