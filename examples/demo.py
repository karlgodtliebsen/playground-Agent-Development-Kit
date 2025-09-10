#!/usr/bin/env python3
"""
Quick demonstration of the ADK setup
This script shows all the key features working
"""
import sys
import os
import asyncio

# Add src to path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from adk import setup_logging
from adk.agents import EchoAgent, AVAILABLE_AGENTS
from adk.utils import print_environment_status, validate_environment
from adk.config import get_config


async def demonstrate_adk():
    """Demonstrate ADK functionality"""
    
    print("🚀 Google Agent Development Kit (ADK) - Quick Demo")
    print("=" * 60)
    
    # Setup logging
    setup_logging(level="INFO", format_type="console")
    
    # Show environment status
    print("\n📋 Environment Status:")
    print_environment_status()
    
    # Show configuration
    print("\n⚙️  Configuration:")
    try:
        config = get_config()
        print(f"   Project: {config.google_cloud_project}")
        print(f"   Location: {config.vertex_ai_location}")
        print(f"   Agent Name: {config.agent_name}")
        print(f"   Server: {config.host}:{config.port}")
    except Exception as e:
        print(f"   ⚠️  Configuration issue: {e}")
    
    # Show available agents
    print(f"\n🤖 Available Agent Types: {list(AVAILABLE_AGENTS.keys())}")
    
    # Demonstrate echo agent
    print("\n🧪 Testing Echo Agent:")
    echo_agent = EchoAgent(name="DemoAgent")
    await echo_agent.initialize()
    
    test_messages = [
        "Hello, World!",
        "This is a test message",
        "ADK is working!"
    ]
    
    for i, message in enumerate(test_messages, 1):
        response = await echo_agent.process_message(message)
        print(f"   Test {i}: {response}")
    
    # Health check
    health = await echo_agent.health_check()
    print(f"   Health: {health['status']}")
    
    print("\n✅ ADK Demo Complete!")
    print("\n📚 Next Steps:")
    print("   1. Copy .env.example to .env and configure your Google Cloud project")
    print("   2. Run 'python examples/server.py' to start the API server")
    print("   3. Open 'examples/getting_started.ipynb' in Jupyter for interactive development")
    print("   4. Check the README.md for detailed setup instructions")
    
    return True


if __name__ == "__main__":
    asyncio.run(demonstrate_adk())