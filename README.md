# playground-Agent-Development-Kit

A playground environment for experimenting with Google Agent Development Kit (ADK). This repository provides a structured foundation for building, testing, and deploying AI agents using Google Cloud AI services, Vertex AI, and Dialogflow.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Cloud Project with AI services enabled
- Git

### 1. Clone and Setup

```bash
git clone https://github.com/karlgodtliebsen/playground-Agent-Development-Kit.git
cd playground-Agent-Development-Kit

# Run automated setup
python scripts/setup.py
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# At minimum, set:
# GOOGLE_CLOUD_PROJECT=your-project-id
```

### 3. Google Cloud Authentication

Choose one of these authentication methods:

**Option A: Service Account Key (Recommended for development)**
```bash
# Download service account key from Google Cloud Console
# Save as credentials.json in project root
export GOOGLE_APPLICATION_CREDENTIALS="./credentials.json"
```

**Option B: Application Default Credentials**
```bash
# Install Google Cloud CLI and authenticate
gcloud auth application-default login
```

### 4. Test the Setup

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Test basic functionality
python examples/basic_agent_example.py

# Start the API server
python examples/server.py
```

## 📁 Project Structure

```
playground-Agent-Development-Kit/
├── src/adk/                    # Main package
│   ├── agents/                 # Agent implementations
│   ├── config/                 # Configuration management
│   └── utils/                  # Utility functions
├── examples/                   # Example scripts and applications
│   ├── basic_agent_example.py  # Basic agent usage
│   └── server.py              # FastAPI server
├── scripts/                    # Setup and utility scripts
│   └── setup.py              # Automated setup script
├── tests/                     # Test files
├── docs/                      # Documentation
├── .env.example              # Environment template
├── requirements.txt          # Python dependencies
└── pyproject.toml           # Project configuration
```

## 🤖 Available Agents

### Echo Agent
Simple agent that echoes messages back - useful for testing:

```python
from adk.agents import EchoAgent

agent = EchoAgent()
await agent.initialize()
response = await agent.process_message("Hello!")
```

### Vertex AI Agent
Agent that uses Google Vertex AI for text generation:

```python
from adk.agents import VertexAIAgent

agent = VertexAIAgent(model_name="text-bison")
await agent.initialize()
response = await agent.process_message("Write a poem about AI")
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_CLOUD_PROJECT` | Your Google Cloud project ID | Required |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to service account key | Optional |
| `VERTEX_AI_LOCATION` | Vertex AI region | `us-central1` |
| `AGENT_NAME` | Default agent name | `playground-agent` |
| `HOST` | Server host | `localhost` |
| `PORT` | Server port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Google Cloud Services

Enable these APIs in your Google Cloud project:
- Vertex AI API
- Dialogflow API (if using Dialogflow)
- Cloud Storage API (for file storage)

## 💻 Usage Examples

### Basic Agent Interaction

```python
import asyncio
from adk.agents import EchoAgent

async def main():
    agent = EchoAgent(name="MyAgent")
    await agent.initialize()
    
    response = await agent.process_message(
        "Hello, World!",
        context={"user_id": "123", "session": "abc"}
    )
    print(response)

asyncio.run(main())
```

### API Server Usage

Start the server:
```bash
python examples/server.py
```

Test with curl:
```bash
# Chat with echo agent
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello!", "agent_type": "echo"}'

# Chat with Vertex AI agent (if configured)
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Write a haiku", "agent_type": "vertex"}'

# Health check
curl http://localhost:8000/health
```

### Creating Custom Agents

```python
from adk.agents import BaseAgent

class MyCustomAgent(BaseAgent):
    async def initialize(self):
        # Setup your agent
        self.logger.info("Custom agent initialized")
    
    async def process_message(self, message: str, context=None) -> str:
        # Implement your logic
        return f"Processed: {message}"

# Register your agent
from adk.agents import AVAILABLE_AGENTS
AVAILABLE_AGENTS["custom"] = MyCustomAgent
```

## 🧪 Development

### Install Development Dependencies

```bash
pip install -e .[dev,ai,jupyter]
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/ examples/ tests/
flake8 src/ examples/ tests/
```

### Type Checking

```bash
mypy src/
```

## 📊 Monitoring and Logging

The project uses structured logging with `structlog`. Logs are output in JSON format by default for easy parsing and monitoring.

### Log Levels
- `DEBUG`: Detailed debugging information
- `INFO`: General information about agent operations
- `WARNING`: Warning messages
- `ERROR`: Error conditions

### Health Checks

Monitor agent health via the `/health` endpoint:
```bash
curl http://localhost:8000/health
```

## 🔒 Security

- Never commit credentials to version control
- Use service accounts with minimal required permissions
- Regularly rotate API keys and credentials
- Enable audit logging in Google Cloud

## 📚 Resources

- [Google Cloud AI Documentation](https://cloud.google.com/ai)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Dialogflow Documentation](https://cloud.google.com/dialogflow/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**"GOOGLE_CLOUD_PROJECT not set"**
- Set the environment variable in your `.env` file

**"Credentials not found"**
- Check your `GOOGLE_APPLICATION_CREDENTIALS` path
- Ensure the service account has necessary permissions

**"Vertex AI not available"**
- Enable Vertex AI API in Google Cloud Console
- Check your project billing is enabled

**Import errors**
- Activate the virtual environment
- Install dependencies: `pip install -e .[ai]`

### Getting Help

- Check the `/health` endpoint for system status
- Review logs for detailed error messages
- Ensure all required environment variables are set