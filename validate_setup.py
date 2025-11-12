#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Validation script to test OpenRouter connection
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from miniagent.logger import get_logger

logger = get_logger("validate")


def validate_api_key():
    """Validate OpenRouter API key"""
    
    # Load environment
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        logger.error("❌ No .env file found")
        logger.info("💡 Create a .env file from .env.example")
        return False
    
    load_dotenv(env_path)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.error("❌ OPENROUTER_API_KEY not set in .env")
        return False
    
    if api_key == "your_openrouter_api_key_here":
        logger.error("❌ Please replace the example API key with your actual key")
        return False
    
    logger.info("✓ API key found")
    
    # Test the API key
    try:
        logger.info("Testing API connection...")
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-3-haiku",  # Use cheapest model for testing
                "messages": [
                    {"role": "user", "content": "Say 'Hello!' if you can hear me."}
                ],
                "max_tokens": 10
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            logger.info(f"✓ API connection successful!")
            logger.info(f"✓ Test response: {message}")
            return True
        elif response.status_code == 401:
            logger.error("❌ Invalid API key")
            logger.info("💡 Get your key from https://openrouter.ai/keys")
            return False
        elif response.status_code == 402:
            logger.error("❌ Insufficient credits")
            logger.info("💡 Add credits at https://openrouter.ai/credits")
            return False
        else:
            logger.error(f"❌ API error: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        logger.error("❌ Connection timeout")
        logger.info("💡 Check your internet connection")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Connection error: {e}")
        return False


def validate_dependencies():
    """Check if all dependencies are installed"""
    try:
        import requests
        import dotenv
        logger.info("✓ All dependencies installed")
        return True
    except ImportError as e:
        logger.error(f"❌ Missing dependency: {e}")
        logger.info("💡 Run: pip install -r requirements.txt")
        return False


def main():
    """Run all validations"""
    print("\n" + "="*60)
    print("MiniAgent-OpenRouter Validation")
    print("="*60 + "\n")
    
    # Check dependencies
    if not validate_dependencies():
        return
    
    # Check API key
    if not validate_api_key():
        return
    
    print("\n" + "="*60)
    print("✓ All checks passed! You're ready to use MiniAgent")
    print("="*60)
    print("\nTry running an example:")
    print("  python examples/simple_example.py")
    print()


if __name__ == "__main__":
    main()
