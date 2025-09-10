#!/usr/bin/env python3
"""
FastAPI server for ADK agents
"""
import sys
import os
from typing import Dict, Any, Optional

# Add src to path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from adk import setup_logging, Config
from adk.agents import AVAILABLE_AGENTS, BaseAgent
from adk.utils import validate_environment


# Pydantic models for API
class MessageRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    agent_type: str = "echo"


class MessageResponse(BaseModel):
    response: str
    agent_name: str
    agent_type: str


class HealthResponse(BaseModel):
    status: str
    environment: Dict[str, Any]
    agents: Dict[str, Dict[str, Any]]


# Initialize FastAPI app
app = FastAPI(
    title="ADK Agent Server",
    description="Agent Development Kit - API Server for agent interactions",
    version="0.1.0"
)

# Global agent instances
agents: Dict[str, BaseAgent] = {}


@app.on_event("startup")
async def startup_event():
    """Initialize agents on startup"""
    setup_logging()
    
    # Initialize available agents
    for agent_type, agent_class in AVAILABLE_AGENTS.items():
        try:
            agent = agent_class(name=f"server-{agent_type}")
            await agent.initialize()
            agents[agent_type] = agent
            print(f"✅ Initialized {agent_type} agent")
        except Exception as e:
            print(f"⚠️  Failed to initialize {agent_type} agent: {e}")


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "ADK Agent Server",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    env_status = validate_environment()
    agent_status = {}
    
    for agent_type, agent in agents.items():
        try:
            health = await agent.health_check()
            agent_status[agent_type] = health
        except Exception as e:
            agent_status[agent_type] = {"status": "error", "error": str(e)}
    
    return HealthResponse(
        status="healthy",
        environment=env_status,
        agents=agent_status
    )


@app.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    """Process a message with an agent"""
    if request.agent_type not in agents:
        raise HTTPException(
            status_code=400,
            detail=f"Agent type '{request.agent_type}' not available. Available types: {list(agents.keys())}"
        )
    
    try:
        agent = agents[request.agent_type]
        response = await agent.process_message(request.message, request.context)
        
        return MessageResponse(
            response=response,
            agent_name=agent.name,
            agent_type=request.agent_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@app.get("/agents")
async def list_agents():
    """List available agents"""
    return {
        "available_agents": list(AVAILABLE_AGENTS.keys()),
        "initialized_agents": list(agents.keys()),
        "agent_details": {
            agent_type: {
                "name": agent.name,
                "description": agent.description
            }
            for agent_type, agent in agents.items()
        }
    }


def main():
    """Run the server"""
    config = Config()
    
    print("🚀 Starting ADK Agent Server")
    print(f"   Host: {config.host}")
    print(f"   Port: {config.port}")
    print(f"   Debug: {config.debug}")
    
    uvicorn.run(
        "server:app",
        host=config.host,
        port=config.port,
        reload=config.debug
    )


if __name__ == "__main__":
    main()