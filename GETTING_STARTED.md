# 🚀 Getting Started with MiniAgent-OpenRouter

Welcome! This guide will get you up and running in under 5 minutes.

## 📋 What You'll Need

- Python 3.8 or higher
- Internet connection
- OpenRouter API key (free to create)
- $1 minimum credit on OpenRouter

## 🎯 Step-by-Step Setup

### Step 1: Install Python Dependencies

Open your terminal and navigate to the project directory:

```bash
cd MiniAgent-OpenRouter
pip install -r requirements.txt
```

This installs only 2 dependencies:
- `requests` - For API calls
- `python-dotenv` - For configuration

### Step 2: Get Your OpenRouter API Key

1. **Visit**: [https://openrouter.ai](https://openrouter.ai)
2. **Sign up** with your email or GitHub
3. **Go to Keys**: [https://openrouter.ai/keys](https://openrouter.ai/keys)
4. **Create a new key** - Click "Create Key"
5. **Copy the key** - It looks like: `sk-or-v1-abc123...`
6. **Add credits**: [https://openrouter.ai/credits](https://openrouter.ai/credits)
   - Minimum: $1
   - Recommended: $5 for testing

### Step 3: Configure Your Environment

Create your `.env` file:

```bash
# On Mac/Linux
cp .env.example .env

# On Windows
copy .env.example .env
```

Edit the `.env` file (use any text editor):

```env
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

**Important**: Replace `sk-or-v1-your-actual-key-here` with your real API key!

### Step 4: Validate Your Setup

Run the validation script:

```bash
python validate_setup.py
```

You should see:
```
✓ All dependencies installed
✓ API key found
✓ API connection successful!
✓ All checks passed! You're ready to use MiniAgent
```

If you see errors, check:
- Your API key is correct
- You have credits on OpenRouter
- Your internet connection is working

### Step 5: Run Your First Agent!

```bash
python examples/simple_example.py
```

You should see the agent:
1. Think about what to do
2. Use tools (calculator, get time)
3. Provide a final answer

## 🎉 Success!

If everything worked, you're ready to build agents! 

## 📚 What's Next?

### Try the Examples

```bash
# Simple usage with built-in tools
python examples/simple_example.py

# Create and use custom tools
python examples/custom_tools_example.py

# Complex multi-tool workflows
python examples/advanced_example.py

# Interactive chatbot
python examples/chatbot_example.py
```

### Read the Guides

1. **README.md** - Comprehensive guide
2. **QUICKSTART.md** - Quick reference
3. **MODEL_GUIDE.md** - Choosing the right model
4. **PROJECT_SUMMARY.md** - What's included

### Build Your First Agent

Create a new file `my_agent.py`:

```python
from miniagent import MiniAgent, register_tool
import os
from dotenv import load_dotenv

# Load configuration
load_dotenv()

# Create a custom tool
@register_tool
def greet(name: str) -> str:
    """Greet someone by name"""
    return f"Hello, {name}! Welcome to MiniAgent!"

# Create agent
agent = MiniAgent(
    model=os.getenv("OPENROUTER_MODEL"),
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Add your tool
from miniagent import get_tool_description
agent.tools.append(get_tool_description(greet))

# Use it!
response = agent.run("Please greet Alice")
print(response)
```

Run it:
```bash
python my_agent.py
```

## 🔧 Common Issues & Solutions

### Issue: "Authentication failed"

**Problem**: Invalid or missing API key

**Solution**:
1. Check `.env` file exists
2. Verify API key is correct (copy from OpenRouter)
3. Make sure no extra spaces in the key
4. Ensure the key is active at https://openrouter.ai/keys

### Issue: "Insufficient credits"

**Problem**: No credits in your OpenRouter account

**Solution**:
1. Go to https://openrouter.ai/credits
2. Add at least $1 (recommended $5)
3. Wait a few seconds for it to activate

### Issue: "Module not found"

**Problem**: Dependencies not installed

**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: "Tool not being used"

**Problem**: Agent not recognizing tools

**Solution**:
1. Make sure you added the tool before calling `run()`
2. Check tool description is clear
3. Try a more capable model (Claude 3.5 Sonnet)
4. Make your query more explicit

### Issue: "Max iterations reached"

**Problem**: Agent can't complete task

**Solution**:
1. Simplify your query
2. Increase `max_iterations` parameter
3. Try a more capable model
4. Check if tools are working correctly

## 💡 Pro Tips

### Tip 1: Start with Haiku for Development

While developing, use the cheaper model:

```env
OPENROUTER_MODEL=anthropic/claude-3-haiku
```

Switch to Sonnet for production:

```env
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

### Tip 2: Enable Debug Logging

Add this to your code for more details:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Tip 3: Test Your Tools First

Before running the full agent, test tools individually:

```python
from miniagent.tools.basic_tools import calculator

result = calculator("2 + 2")
print(result)  # Should print 4.0
```

### Tip 4: Use Simple Queries First

Start with simple, clear queries:
- ✅ "What is 5 + 3?"
- ✅ "What time is it?"
- ❌ "Do complex math and tell me about history"

### Tip 5: Monitor Your Usage

Check your usage at: https://openrouter.ai/activity

## 🎓 Learning Path

### Week 1: Basics
- [ ] Run all example files
- [ ] Understand how agents work
- [ ] Create 1-2 custom tools
- [ ] Experiment with different models

### Week 2: Intermediate
- [ ] Build a multi-tool workflow
- [ ] Create a small application
- [ ] Learn about error handling
- [ ] Optimize for cost

### Week 3: Advanced
- [ ] Study the agent.py code
- [ ] Customize the ReAct pattern
- [ ] Build something real
- [ ] Share your creation!

## 🌟 Your First Project Ideas

### Easy Projects
1. **Personal Assistant**: Answer questions + get time
2. **Calculator Bot**: Complex math solver
3. **Text Analyzer**: Count words, analyze text
4. **Unit Converter**: Convert between units

### Medium Projects
1. **Research Assistant**: Search knowledge + summarize
2. **Data Processor**: Load data + analyze + report
3. **Task Manager**: Track tasks with tools
4. **Code Helper**: Answer code questions

### Advanced Projects
1. **Multi-Agent System**: Multiple specialized agents
2. **Workflow Automator**: Chain multiple operations
3. **Custom RAG System**: Retrieval + generation
4. **API Integrator**: Connect multiple services

## 📞 Getting Help

### Documentation
- **README.md** - Main documentation
- **QUICKSTART.md** - Quick reference
- **MODEL_GUIDE.md** - Model selection help
- **PROJECT_SUMMARY.md** - Project overview

### External Resources
- OpenRouter Docs: https://openrouter.ai/docs
- OpenRouter Discord: https://discord.gg/openrouter
- Model Comparison: https://openrouter.ai/models

### Troubleshooting Checklist
- [ ] Python 3.8+ installed?
- [ ] Dependencies installed?
- [ ] .env file created?
- [ ] API key correct?
- [ ] Credits added?
- [ ] validate_setup.py passes?

## ✅ Quick Reference Card

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key

# Validate
python validate_setup.py

# Run Examples
python examples/simple_example.py
python examples/custom_tools_example.py
python examples/advanced_example.py
python examples/chatbot_example.py

# Your Code
from miniagent import MiniAgent
agent = MiniAgent(model="...", api_key="...")
agent.load_builtin_tool("calculator")
response = agent.run("Your query")
```

## 🎯 Success Criteria

You're ready to build when you can:
- ✅ Run validate_setup.py successfully
- ✅ Execute simple_example.py without errors
- ✅ Understand how tools work
- ✅ Create a basic custom tool
- ✅ Know how to check your OpenRouter usage

## 🚀 Ready to Build!

You now have everything you need to create powerful LLM agents.

Start simple, experiment often, and have fun building! 

**Questions?** Check the documentation files or run `validate_setup.py` for diagnostics.

---

**Happy Building!** 🎉

*P.S. - Don't forget to star the project if you find it useful!*
