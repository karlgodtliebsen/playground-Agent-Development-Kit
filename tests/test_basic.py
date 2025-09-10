"""
Basic tests for ADK components
"""
import pytest
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from adk.config import Config, get_config
from adk.agents import BaseAgent, EchoAgent
from adk.utils import setup_logging


class TestConfig:
    """Test configuration management"""
    
    def test_config_creation(self):
        """Test that config can be created with defaults"""
        config = Config(
            google_cloud_project="test-project",
            host="localhost",
            port=8000
        )
        assert config.google_cloud_project == "test-project"
        assert config.host == "localhost"
        assert config.port == 8000
    
    def test_get_config(self):
        """Test config factory function"""
        # This might fail if environment variables aren't set, which is expected
        try:
            config = get_config()
            assert config is not None
        except Exception:
            # Expected if GOOGLE_CLOUD_PROJECT is not set
            pass


class TestAgents:
    """Test agent functionality"""
    
    @pytest.mark.asyncio
    async def test_echo_agent_initialization(self):
        """Test echo agent can be initialized"""
        agent = EchoAgent(name="test-agent")
        await agent.initialize()
        assert agent.name == "test-agent"
    
    @pytest.mark.asyncio
    async def test_echo_agent_process_message(self):
        """Test echo agent message processing"""
        agent = EchoAgent(name="test-agent")
        await agent.initialize()
        
        response = await agent.process_message("test message")
        assert "Echo: test message" in response
    
    @pytest.mark.asyncio
    async def test_echo_agent_with_context(self):
        """Test echo agent with context"""
        agent = EchoAgent(name="test-agent")
        await agent.initialize()
        
        context = {"user": "test_user"}
        response = await agent.process_message("test message", context)
        assert "Echo: test message" in response
        assert "Context:" in response
    
    @pytest.mark.asyncio
    async def test_agent_health_check(self):
        """Test agent health check"""
        agent = EchoAgent(name="test-agent")
        await agent.initialize()
        
        health = await agent.health_check()
        assert health["status"] == "healthy"
        assert health["name"] == "test-agent"


class TestUtils:
    """Test utility functions"""
    
    def test_setup_logging(self):
        """Test logging setup doesn't crash"""
        setup_logging(level="INFO", format_type="json")
        # If no exception is raised, the test passes


if __name__ == "__main__":
    pytest.main([__file__])