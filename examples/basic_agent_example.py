#!/usr/bin/env python3
"""
Basic example of using ADK agents
"""
import asyncio
import sys
import os

# Add src to path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from adk import setup_logging
from adk.agents import EchoAgent, VertexAIAgent
from adk.utils import print_environment_status


async def main():
    """Main example function"""
    # Setup logging
    setup_logging(level="INFO", format_type="console")
    
    # Print environment status
    print_environment_status()
    print("\n" + "="*50)
    
    # Test Echo Agent
    print("\n🤖 Testing Echo Agent")
    echo_agent = EchoAgent(name="TestEcho", description="Test echo agent")
    await echo_agent.initialize()
    
    response = await echo_agent.process_message("Hello, World!")
    print(f"Response: {response}")
    
    # Test with context
    response = await echo_agent.process_message(
        "Hello with context!", 
        context={"user": "test_user", "session": "12345"}
    )
    print(f"Response with context: {response}")
    
    # Health check
    health = await echo_agent.health_check()
    print(f"Health check: {health}")
    
    print("\n" + "="*50)
    
    # Test Vertex AI Agent (if configured)
    print("\n🧠 Testing Vertex AI Agent")
    try:
        vertex_agent = VertexAIAgent(name="TestVertex", model_name="text-bison")
        await vertex_agent.initialize()
        
        response = await vertex_agent.process_message(
            "Write a short poem about artificial intelligence."
        )
        print(f"Vertex AI Response: {response}")
        
    except Exception as e:
        print(f"⚠️  Vertex AI not available: {e}")
        print("💡 Make sure you have:")
        print("   - Set GOOGLE_CLOUD_PROJECT in .env")
        print("   - Configured authentication (GOOGLE_APPLICATION_CREDENTIALS)")
        print("   - Enabled Vertex AI API in your Google Cloud project")


if __name__ == "__main__":
    asyncio.run(main())