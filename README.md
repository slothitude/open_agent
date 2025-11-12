# MiniAgent - OpenRouter Edition

🚀 **Build an LLM Agent in 5 minutes using OpenRouter!**

A lightweight, easy-to-understand LLM Agent framework that works with **any model on OpenRouter** - including Claude, GPT-4, Llama, Gemini, and more.

## Why MiniAgent-OpenRouter?

- **🌐 Universal Compatibility**: Works with 100+ models through OpenRouter's unified API
- **💡 Simple to Learn**: Clear, readable code that teaches agent fundamentals
- **🔧 Easy Tool Integration**: Add custom tools with simple Python decorators
- **⚡ Lightweight**: Minimal dependencies, easy to modify and extend
- **🤖 ReAct Pattern**: Uses the proven Reason-Act-Observe loop for reliable tool usage

## What is OpenRouter?

[OpenRouter](https://openrouter.ai/) provides a unified API to access many AI models:
- Anthropic Claude (3.5 Sonnet, 3 Opus, etc.)
- OpenAI GPT (GPT-4, GPT-3.5-turbo)
- Google Gemini
- Meta Llama
- And 100+ more models!

You only need one API key to access all of them.

## Quick Start

### 1. Installation

```bash
# Clone or download this repository
cd MiniAgent-OpenRouter

# Install dependencies
pip install -r requirements.txt
```

### 2. Get Your OpenRouter API Key

1. Go to [OpenRouter](https://openrouter.ai/)
2. Sign up for an account
3. Get your API key from the dashboard
4. Add credits to your account (starts at $1)

### 3. Configure

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

### 4. Run Examples

```bash
# Simple example with built-in tools
python examples/simple_example.py

# Custom tools example
python examples/custom_tools_example.py
```

## Usage

### Basic Usage

```python
from miniagent import MiniAgent

# Initialize agent with your preferred model
agent = MiniAgent(
    model="anthropic/claude-3.5-sonnet",  # or any OpenRouter model
    api_key="your_openrouter_api_key"
)

# Load built-in tools
agent.load_builtin_tool("calculator")
agent.load_builtin_tool("get_current_time")

# Ask a question
response = agent.run("What time is it? Also calculate 15 * 23.")
print(response)
```

### Creating Custom Tools

```python
from miniagent import MiniAgent, register_tool

# Define a custom tool
@register_tool
def get_weather(city: str) -> str:
    """
    Get weather information for a city
    
    Args:
        city: Name of the city
    """
    # Your weather API call here
    return f"Weather in {city}: Sunny, 72°F"

# Create agent
agent = MiniAgent(
    model="anthropic/claude-3.5-sonnet",
    api_key="your_key"
)

# Add your custom tool
from miniagent import get_tool_description
agent.tools.append(get_tool_description(get_weather))

# Use it!
response = agent.run("What's the weather in San Francisco?")
```

## Available Models

Here are some popular models you can use:

### Anthropic Claude
- `anthropic/claude-3.5-sonnet` (Recommended - best balance)
- `anthropic/claude-3-opus` (Most capable)
- `anthropic/claude-3-sonnet`
- `anthropic/claude-3-haiku` (Fastest, cheapest)

### OpenAI
- `openai/gpt-4-turbo`
- `openai/gpt-4`
- `openai/gpt-3.5-turbo`

### Google
- `google/gemini-pro`
- `google/gemini-pro-vision`

### Meta
- `meta-llama/llama-3-70b-instruct`
- `meta-llama/llama-3-8b-instruct`

### And many more!

See the full list at [OpenRouter Models](https://openrouter.ai/models)

## Built-in Tools

MiniAgent comes with these built-in tools:

- **calculator**: Safe mathematical expression evaluation
- **get_current_time**: Get current date and time
- **system_info**: Get system information

## How It Works

MiniAgent uses the **ReAct** (Reason + Act) pattern:

1. **Reason**: The LLM thinks about what to do
2. **Act**: It decides to use a tool
3. **Observe**: It sees the tool's result
4. **Repeat**: Until it has enough info to answer

Example flow:
```
User: "What is 25 * 4 and what time is it?"

LLM Thinks: "I need to calculate 25 * 4 and get the time"
LLM Acts: Uses calculator tool with "25 * 4"
Tool Returns: 100
LLM Thinks: "Good, now I need the time"
LLM Acts: Uses get_current_time tool
Tool Returns: "2025-11-12 14:30:00"
LLM Thinks: "I have all the information now"
LLM Answers: "25 * 4 = 100, and the current time is 2:30 PM"
```

## Advanced Configuration

```python
agent = MiniAgent(
    model="anthropic/claude-3.5-sonnet",
    api_key="your_key",
    temperature=0.7,           # Creativity level (0.0-1.0)
    max_tokens=4096,           # Max response length
    max_iterations=10,         # Max reasoning loops
    system_prompt="custom..."  # Custom instructions
)
```

## Project Structure

```
MiniAgent-OpenRouter/
├── miniagent/
│   ├── __init__.py          # Main exports
│   ├── agent.py             # Core agent logic
│   ├── logger.py            # Logging utilities
│   └── tools/
│       ├── __init__.py      # Tool registration
│       └── basic_tools.py   # Built-in tools
├── examples/
│   ├── simple_example.py    # Basic usage
│   └── custom_tools_example.py  # Custom tools
├── .env.example             # Configuration template
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## Cost Management

OpenRouter charges based on the model you use. Tips:

1. Start with cheaper models for testing:
   - `anthropic/claude-3-haiku`
   - `openai/gpt-3.5-turbo`

2. Use rate limits in your code
3. Monitor usage in OpenRouter dashboard
4. Set a `max_iterations` limit to prevent runaway costs

## Troubleshooting

### "Authentication failed"
- Check your API key in `.env`
- Ensure you have credits on OpenRouter

### "Model not found"
- Verify model name at [OpenRouter Models](https://openrouter.ai/models)
- Check for typos in model identifier

### Agent doesn't use tools
- Make sure tools are loaded before calling `run()`
- Check if the model supports function calling (most do)
- Try adjusting the `system_prompt`

### "Max iterations reached"
- Increase `max_iterations` parameter
- Simplify your query
- Try a more capable model

## Contributing

This is a learning-focused project. Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Apache License 2.0 - see LICENSE file

## Credits

Based on the original [MiniAgent](https://github.com/ZhuLinsen/MiniAgent) by ZhuLinsen, adapted for OpenRouter compatibility.

## Support

- OpenRouter Docs: https://openrouter.ai/docs
- Issues: GitHub Issues
- Questions: Open a discussion

---

**Happy Agent Building!** 🤖✨
