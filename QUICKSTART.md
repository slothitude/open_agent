# Quick Start Guide

## Get Started in 3 Minutes

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Get OpenRouter API Key

1. Go to [https://openrouter.ai](https://openrouter.ai)
2. Sign up for an account
3. Navigate to [Keys](https://openrouter.ai/keys)
4. Create a new API key
5. Add some credits (minimum $1)

### Step 3: Configure

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your key
nano .env  # or use your preferred editor
```

Your `.env` should look like:
```env
OPENROUTER_API_KEY=sk-or-v1-...your-key-here...
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

### Step 4: Validate Setup

```bash
python validate_setup.py
```

If you see "✓ All checks passed!" you're ready to go!

### Step 5: Run Your First Agent

```bash
python examples/simple_example.py
```

## What's Next?

### Try Different Models

Edit your `.env` file to try different models:

```env
# For fast responses
OPENROUTER_MODEL=anthropic/claude-3-haiku

# For best quality
OPENROUTER_MODEL=anthropic/claude-3-opus

# For OpenAI
OPENROUTER_MODEL=openai/gpt-4-turbo

# For Google
OPENROUTER_MODEL=google/gemini-pro
```

See all available models: [https://openrouter.ai/models](https://openrouter.ai/models)

### Explore Examples

```bash
# Custom tools
python examples/custom_tools_example.py

# Advanced multi-tool usage
python examples/advanced_example.py
```

### Build Your Own Agent

Create a new Python file:

```python
from miniagent import MiniAgent, register_tool
import os
from dotenv import load_dotenv

load_dotenv()

# Define your custom tool
@register_tool
def my_tool(input_text: str) -> str:
    """Description of what your tool does"""
    return f"Processed: {input_text}"

# Create agent
agent = MiniAgent(
    model=os.getenv("OPENROUTER_MODEL"),
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Add tools
from miniagent import get_tool_description
agent.tools.append(get_tool_description(my_tool))
agent.load_builtin_tool("calculator")

# Run!
response = agent.run("Your question here")
print(response)
```

## Common Issues

### "Authentication failed"

**Problem**: Invalid API key

**Solution**: 
1. Check your `.env` file
2. Make sure you copied the full key
3. Verify key is active at [https://openrouter.ai/keys](https://openrouter.ai/keys)

### "Insufficient credits"

**Problem**: No credits in account

**Solution**: Add credits at [https://openrouter.ai/credits](https://openrouter.ai/credits)

### "Module not found"

**Problem**: Dependencies not installed

**Solution**: Run `pip install -r requirements.txt`

### Agent not using tools

**Problem**: Tools not loaded or model doesn't support them

**Solution**:
1. Make sure you call `agent.load_builtin_tool()` or add to `agent.tools`
2. Try a more capable model like Claude or GPT-4

## Tips

### Cost Saving

Start with cheaper models for development:
- `anthropic/claude-3-haiku` - Very fast, very cheap
- `openai/gpt-3.5-turbo` - Good balance

Use expensive models only when needed:
- `anthropic/claude-3-opus` - Most capable
- `openai/gpt-4-turbo` - Very capable

### Debugging

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Rate Limiting

Add delays between requests:

```python
import time
response1 = agent.run("Query 1")
time.sleep(1)  # Wait 1 second
response2 = agent.run("Query 2")
```

## Learn More

- **OpenRouter Docs**: [https://openrouter.ai/docs](https://openrouter.ai/docs)
- **Model Comparison**: [https://openrouter.ai/models](https://openrouter.ai/models)
- **Pricing**: [https://openrouter.ai/docs/pricing](https://openrouter.ai/docs/pricing)

## Getting Help

1. Check the main [README.md](README.md)
2. Run `python validate_setup.py` to diagnose issues
3. Review examples in `examples/` directory
4. Open an issue on GitHub

---

**Happy building!** 🚀
