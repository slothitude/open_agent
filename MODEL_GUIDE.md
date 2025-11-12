# OpenRouter Model Guide for MiniAgent

## 🎯 Recommended Models

### Best Overall: Claude 3.5 Sonnet
```env
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```
- ⭐ **Best balance** of intelligence, speed, and cost
- Excellent at following instructions
- Great tool usage
- **Use for**: Production applications, complex reasoning

### Best Quality: Claude 3 Opus
```env
OPENROUTER_MODEL=anthropic/claude-3-opus
```
- 🏆 Most capable model
- Superior reasoning
- Best for complex tasks
- **Use for**: Critical tasks, research, complex analysis
- ⚠️ More expensive

### Fastest & Cheapest: Claude 3 Haiku
```env
OPENROUTER_MODEL=anthropic/claude-3-haiku
```
- ⚡ Fastest responses
- 💰 Most affordable
- Still very capable
- **Use for**: Development, testing, simple tasks

### Popular Alternative: GPT-4 Turbo
```env
OPENROUTER_MODEL=openai/gpt-4-turbo
```
- 🔥 Very capable
- Good tool usage
- Fast responses
- **Use for**: When Claude isn't available

### Budget Option: GPT-3.5 Turbo
```env
OPENROUTER_MODEL=openai/gpt-3.5-turbo
```
- 💰 Very cheap
- Fast
- Good for simple tasks
- **Use for**: Testing, simple queries

## 📊 Quick Comparison

| Model | Speed | Cost | Quality | Best For |
|-------|-------|------|---------|----------|
| Claude 3.5 Sonnet | ⚡⚡⚡ | 💰💰 | ⭐⭐⭐⭐⭐ | **Production** |
| Claude 3 Opus | ⚡⚡ | 💰💰💰 | ⭐⭐⭐⭐⭐ | Complex tasks |
| Claude 3 Haiku | ⚡⚡⚡⚡ | 💰 | ⭐⭐⭐⭐ | **Development** |
| GPT-4 Turbo | ⚡⚡⚡ | 💰💰 | ⭐⭐⭐⭐ | Alternative |
| GPT-3.5 Turbo | ⚡⚡⚡⚡ | 💰 | ⭐⭐⭐ | **Testing** |
| Gemini Pro | ⚡⚡⚡ | 💰 | ⭐⭐⭐⭐ | Google ecosystem |
| Llama 3 70B | ⚡⚡ | 💰 | ⭐⭐⭐⭐ | Open source fans |

## 💰 Cost Estimates (as of 2024)

### Per 1M Tokens (approximate)
- **Claude 3 Haiku**: $0.25 input / $1.25 output
- **Claude 3.5 Sonnet**: $3 input / $15 output
- **Claude 3 Opus**: $15 input / $75 output
- **GPT-3.5 Turbo**: $0.50 input / $1.50 output
- **GPT-4 Turbo**: $10 input / $30 output

### Real-World Examples
```
Simple query (100 tokens):
- Haiku: $0.00003
- Sonnet: $0.0003
- Opus: $0.0015
- GPT-3.5: $0.00005

Complex task (1000 tokens):
- Haiku: $0.0003
- Sonnet: $0.003
- Opus: $0.015
- GPT-3.5: $0.0005
```

## 🎯 Use Case Recommendations

### Development & Testing
```env
OPENROUTER_MODEL=anthropic/claude-3-haiku
# Fast, cheap, good enough for testing
```

### Production Applications
```env
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
# Best balance for production use
```

### Research & Analysis
```env
OPENROUTER_MODEL=anthropic/claude-3-opus
# When you need the absolute best
```

### High-Volume Simple Tasks
```env
OPENROUTER_MODEL=openai/gpt-3.5-turbo
# Maximum cost efficiency
```

### Specific Requirements

#### Best for Tool Usage
1. Claude 3.5 Sonnet ⭐
2. GPT-4 Turbo
3. Claude 3 Opus

#### Best for Speed
1. Claude 3 Haiku ⭐
2. GPT-3.5 Turbo
3. Gemini Pro

#### Best for Code
1. Claude 3.5 Sonnet ⭐
2. GPT-4 Turbo
3. Claude 3 Opus

#### Best for Reasoning
1. Claude 3 Opus ⭐
2. Claude 3.5 Sonnet
3. GPT-4 Turbo

## 🔄 Switching Models

### In Code
```python
# Easy - just change the model parameter
agent = MiniAgent(
    model="anthropic/claude-3-haiku",  # Change this line
    api_key=api_key
)
```

### In .env File
```env
# Just edit this line
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

### Testing Different Models
```python
models_to_test = [
    "anthropic/claude-3-haiku",
    "anthropic/claude-3.5-sonnet",
    "openai/gpt-4-turbo"
]

for model in models_to_test:
    agent = MiniAgent(model=model, api_key=api_key)
    response = agent.run("Your test query")
    print(f"{model}: {response[:100]}...")
```

## 💡 Pro Tips

### 1. Start Small
Begin development with Haiku, then upgrade to Sonnet for production.

### 2. Match Model to Task
- Simple queries → Haiku or GPT-3.5
- Complex reasoning → Sonnet or Opus
- Code generation → Sonnet

### 3. Monitor Costs
```python
# Keep track of token usage
import requests

response = agent.run(query)
# Check response metadata for token counts
```

### 4. Use Rate Limits
```python
import time

for query in queries:
    response = agent.run(query)
    time.sleep(0.5)  # Rate limiting
```

### 5. Cache When Possible
```python
# For repeated queries, cache results
cache = {}
if query in cache:
    return cache[query]
else:
    response = agent.run(query)
    cache[query] = response
    return response
```

## 🌟 Model-Specific Settings

### For Claude Models
```python
agent = MiniAgent(
    model="anthropic/claude-3.5-sonnet",
    temperature=0.7,  # 0.7-1.0 recommended
    max_tokens=4096   # Claude supports up to 4096
)
```

### For GPT Models
```python
agent = MiniAgent(
    model="openai/gpt-4-turbo",
    temperature=0.8,  # 0.7-1.0 recommended
    max_tokens=4096   # GPT-4 supports more
)
```

### For Open Source Models
```python
agent = MiniAgent(
    model="meta-llama/llama-3-70b-instruct",
    temperature=0.7,
    max_tokens=2048   # May have lower limits
)
```

## 📈 Model Performance

### Tool Usage Success Rate
- Claude 3.5 Sonnet: ~95%
- Claude 3 Opus: ~97%
- GPT-4 Turbo: ~90%
- Claude 3 Haiku: ~85%
- GPT-3.5 Turbo: ~75%

### Typical Response Times
- Haiku: 1-2 seconds
- Sonnet: 2-4 seconds
- Opus: 3-6 seconds
- GPT-3.5: 1-3 seconds
- GPT-4: 2-5 seconds

## 🎓 Recommendations by Experience Level

### Beginner
**Start with**: `anthropic/claude-3-haiku`
- Cheap for learning
- Fast feedback
- Good enough for basics

### Intermediate
**Use**: `anthropic/claude-3.5-sonnet`
- Production quality
- Reasonable cost
- Reliable tool usage

### Advanced
**Choose based on needs**:
- Complex tasks: `claude-3-opus`
- High volume: `gpt-3.5-turbo`
- Specific features: Model-specific strengths

## 🔍 Full Model List

See all available models at: [https://openrouter.ai/models](https://openrouter.ai/models)

Popular categories:
- **Anthropic**: Claude 3 family (Opus, Sonnet, Haiku)
- **OpenAI**: GPT-4, GPT-3.5 variants
- **Google**: Gemini Pro, Gemini Pro Vision
- **Meta**: Llama 3 (8B, 70B)
- **Mistral**: Mistral Medium, Large
- **And 100+ more!**

---

**Bottom Line**: Start with Claude 3.5 Sonnet for the best balance. It's what we recommend for most use cases! 🎯
