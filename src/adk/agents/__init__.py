"""
Base agent classes and utilities
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import structlog
from ..config import get_config


logger = structlog.get_logger()


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.config = get_config()
        self.name = name or self.config.agent_name
        self.description = description or self.config.agent_description
        self.logger = logger.bind(agent=self.name)
        
    @abstractmethod
    async def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process a message and return a response"""
        pass
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the agent"""
        pass
    
    async def health_check(self) -> Dict[str, Any]:
        """Check agent health status"""
        return {
            "status": "healthy",
            "name": self.name,
            "description": self.description
        }


class EchoAgent(BaseAgent):
    """Simple echo agent for testing"""
    
    async def initialize(self) -> None:
        """Initialize the echo agent"""
        self.logger.info("Echo agent initialized")
    
    async def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Echo the message back with some processing info"""
        self.logger.info("Processing message", message=message, context=context)
        
        response = f"Echo: {message}"
        if context:
            response += f" (Context: {context})"
        
        return response


class VertexAIAgent(BaseAgent):
    """Agent that uses Google Vertex AI"""
    
    def __init__(self, model_name: str = "text-bison", **kwargs):
        super().__init__(**kwargs)
        self.model_name = model_name
        self.client = None
    
    async def initialize(self) -> None:
        """Initialize the Vertex AI client"""
        try:
            from google.cloud import aiplatform
            
            aiplatform.init(
                project=self.config.google_cloud_project,
                location=self.config.vertex_ai_location
            )
            
            self.logger.info("Vertex AI agent initialized", model=self.model_name)
        except ImportError:
            self.logger.error("google-cloud-aiplatform not available")
            raise
        except Exception as e:
            self.logger.error("Failed to initialize Vertex AI", error=str(e))
            raise
    
    async def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process message using Vertex AI"""
        try:
            from google.cloud import aiplatform
            
            # For text generation
            model = aiplatform.TextGenerationModel.from_pretrained(self.model_name)
            
            parameters = {
                "temperature": 0.7,
                "max_output_tokens": 1024,
                "top_p": 0.8,
                "top_k": 40
            }
            
            response = model.predict(message, **parameters)
            
            self.logger.info("Generated response", 
                           model=self.model_name, 
                           message_length=len(message),
                           response_length=len(response.text))
            
            return response.text
            
        except Exception as e:
            self.logger.error("Failed to process message", error=str(e))
            return f"Error processing message: {str(e)}"


# Agent registry
AVAILABLE_AGENTS = {
    "echo": EchoAgent,
    "vertex": VertexAIAgent,
}