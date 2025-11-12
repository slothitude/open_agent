# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MiniAgent is a lightweight LLM Agent framework that uses the OpenRouter API to work with 100+ different AI models. It implements the ReAct (Reason-Act-Observe) pattern for tool-based agent interactions.

**Key characteristics:**
- OpenRouter-compatible: Single API key accesses Claude, GPT-4, Llama, Gemini, and more
- Educational focus: Clear, readable code designed to teach agent fundamentals
- Minimal dependencies: Only requires `requests` and `python-dotenv`

## Development Commands

### Running Examples

```bash
# Basic example with built-in tools
python simple_example.py

# Custom tools demonstration
python custom_tools_example.py

# Todo list example
python todo_example.py

# File system operations example
python file_system_example.py

# Advanced example with custom configurations
python advanced_example.py
```

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment (create .env from template)
# Set OPENROUTER_API_KEY and optionally OPENROUTER_MODEL
```

## Architecture

### Core Components

**1. MiniAgent (`agent.py`)**
The central orchestrator that implements the ReAct loop:
- `run(query, tools)`: Main execution loop with max_iterations limit
- `_call_llm(messages)`: OpenRouter API interaction via `/chat/completions`
- `_parse_action(text)`: Extracts Action/Action Input from LLM responses using regex
- `_execute_tool(tool_name, tool_input)`: Executes tools by name lookup
- `_check_final_answer(text)`: Detects "Final Answer:" to exit the loop

**ReAct Flow:**
1. LLM receives system prompt + tool descriptions + user query
2. LLM responds with "Thought:", "Action:", "Action Input:" format
3. Agent parses and executes the action
4. Result returned as "Observation:" to LLM
5. Loop continues until LLM provides "Final Answer:" or max_iterations reached

**2. Tool System (`tools.py`)**
Decorator-based tool registration:
- `@register_tool`: Marks functions as tools (sets `_is_tool=True`)
- `get_tool_description(func)`: Extracts tool metadata from docstrings and type annotations
- Tool format: `{name, description, parameters, executor}`
- Parameters auto-generated from function signature using `inspect` and `__annotations__`

**3. Built-in Tools (`basic_tools.py`)**
Pre-defined tools in `BUILTIN_TOOLS` dict:
- `calculator`: Safe math eval using AST parsing (no `eval()`)
- `get_current_time`: Returns formatted datetime
- `system_info`: Platform/Python version info

**4. Custom Tool Collections**
Two additional tool modules demonstrating extensibility:
- `todo_tools.py`: In-memory todo list management (create_todo_list, add_todo_item, view_todo_list, mark_item_complete)
- `file_system_tools.py`: File operations (read_file, write_file, replace_text, list_files_recursive, create_directory, run_shell_command)

### Key Design Patterns

**Tool Registration Pattern:**
```python
@register_tool
def my_tool(param: str) -> str:
    """
    Tool description (first line becomes tool description)

    Args:
        param: Parameter description (parsed into tool schema)
    """
    return result
```

**Agent Initialization:**
```python
agent = MiniAgent(
    model="anthropic/claude-3.5-sonnet",  # Any OpenRouter model
    api_key=api_key,
    temperature=0.7,
    max_tokens=4096,
    max_iterations=10,  # Prevents infinite loops
    system_prompt=custom_prompt  # Optional override
)
```

**Adding Tools:**
```python
# Method 1: Built-in tools
agent.load_builtin_tool("calculator")

# Method 2: Custom tools via decorator
from miniagent import get_tool_description
agent.tools.append(get_tool_description(my_tool))

# Method 3: Tool collections
from miniagent import get_todo_tools
agent.tools.extend(get_todo_tools())
```

## Important Implementation Details

### OpenRouter API Integration
- Endpoint: `{base_url}/chat/completions` (default: `https://api.openrouter.ai/api/v1`)
- Headers must include: `Authorization: Bearer {api_key}`
- Optional headers for OpenRouter rankings: `HTTP-Referer`, `X-Title`
- Standard OpenAI-compatible chat completion format

### Response Parsing
The agent expects LLM responses in strict format:
```
Thought: [reasoning]
Action: [tool_name]
Action Input: [valid JSON]
```
Or for completion:
```
Thought: I now have enough information
Final Answer: [response]
```

**Parsing logic** (`agent.py:143-194`):
- Regex-based extraction (case-insensitive, multiline)
- Action Input accepts JSON objects, arrays, strings, or numbers
- Falls back to wrapping in `{"input": value}` if JSON parse fails
- No action found triggers format reminder to LLM

### Security Considerations
- `calculator` tool uses AST parsing instead of `eval()` for safe math evaluation
- `run_shell_command` executes arbitrary shell commands - use with caution
- No input sanitization on file operations - vulnerable to path traversal
- Todo list uses in-memory storage (`TODO_LISTS` dict) - not persistent

### Error Handling
- Max iterations protection (default: 10) prevents infinite loops
- Tool execution errors return error strings to LLM as observations
- API failures raise `RequestException` with 60s timeout
- Missing tools return available tool list in error message

## Module Structure

```
open_agent/
├── __init__.py              # Package exports (MiniAgent, tools, utilities)
├── agent.py                 # Core MiniAgent class with ReAct loop
├── tools.py                 # Tool registration system (@register_tool decorator)
├── basic_tools.py           # Built-in tools (calculator, time, system_info)
├── todo_tools.py            # Todo list tool collection
├── file_system_tools.py     # File operation tool collection
├── logger.py                # Logging configuration
├── *_example.py             # Various usage examples
└── validate_setup.py        # Environment validation script
```

## Configuration

**Environment variables** (`.env` file):
- `OPENROUTER_API_KEY` (required): API key from openrouter.ai
- `OPENROUTER_MODEL` (optional): Model identifier, defaults to `anthropic/claude-3.5-sonnet`

**Common model options:**
- `anthropic/claude-3.5-sonnet` (recommended)
- `anthropic/claude-3-haiku` (faster, cheaper)
- `openai/gpt-4-turbo`
- `google/gemini-pro`
- Full list: https://openrouter.ai/models

## Testing Tools Without Running Full Agent

To test custom tools in isolation:
```python
from miniagent import register_tool, get_tool_description

@register_tool
def my_tool(arg: str) -> str:
    """Tool description
    Args:
        arg: Argument description
    """
    return f"Result: {arg}"

# Get tool description
tool_desc = get_tool_description(my_tool)
print(tool_desc)

# Execute directly
result = my_tool(arg="test")
```
