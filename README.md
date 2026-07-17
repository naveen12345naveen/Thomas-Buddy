# Thomas Buddy - AI Agent

A production-ready, customizable AI agent built with Python and OpenAI's GPT models. Create intelligent agents with tool integration, multi-turn conversations, and extensible architecture.

## Features

✨ **Core Capabilities**
- Multi-turn conversation with full history management
- Tool/function calling support for extending agent capabilities
- Session management with unique session IDs
- Configurable system prompts and behavior
- Error handling and logging

🛠️ **Built-in Tools**
- Web search
- Mathematical calculations
- Time/date information
- Weather lookup
- Text analysis
- Code snippet generation

🔧 **Developer Friendly**
- Easy-to-use Python API
- Extensible tool registry for custom tools
- Comprehensive configuration system
- Unit tests included
- Docker support

📊 **Production Ready**
- Structured logging
- Error tracking
- Performance monitoring
- Environment-based configuration
- Interactive CLI interface

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/naveen12345naveen/Thomas-Buddy.git
cd Thomas-Buddy
```

2. Install dependencies:
```bash
make install
```

3. Setup environment:
```bash
make setup
```

4. Add your OpenAI API key to `.env`:
```bash
OPENAI_API_KEY=your_api_key_here
```

### Running the Agent

**Interactive mode:**
```bash
make run
```

**As a library:**
```python
from src.agent import AIAgent
from src.config import Config

# Create agent
agent = AIAgent(name="Thomas", config=Config())

# Chat with the agent
response = agent.chat("What is Python?")
print(response.content)
```

## Usage Examples

### Basic Chat

```python
from src.agent import AIAgent

agent = AIAgent(name="Thomas")
response = agent.chat("Hello! How can you help me?")
print(response.content)
```

### Using Tools

```python
agent = AIAgent(name="Thomas")

# Agent can use built-in tools automatically
response = agent.chat("What is 25 * 4?", use_tools=True)
print(response.content)

# Access tool calls made
for tool_call in response.tool_calls:
    print(f"Tool: {tool_call.tool_name}, Args: {tool_call.arguments}")
```

### Custom Tools

```python
from src.agent import AIAgent
from src.tools import tool_registry

def get_user_data(user_id: int) -> str:
    return f"User {user_id} data: ..."

# Register custom tool
tool_registry.register(
    "get_user_data",
    "Fetch user data by ID",
    get_user_data,
    {"user_id": {"type": "integer", "description": "User ID"}}
)

# Use it
agent = AIAgent(name="Thomas")
response = agent.chat("Get data for user 123", use_tools=True)
```

## Project Structure

```
Thomas-Buddy/
├── src/
│   ├── agent.py          # Core agent implementation
│   ├── config.py         # Configuration management
│   ├── models.py         # Data models (Pydantic)
│   ├── tools.py          # Tool registry and built-in tools
│   └── __init__.py
├── tests/
│   ├── test_agent.py     # Agent unit tests
│   └── __init__.py
├── examples/
│   ├── basic_chat.py     # Basic usage example
│   ├── custom_tools.py   # Custom tools example
│   └── advanced_usage.py # Advanced examples
├── main.py               # Entry point
├── requirements.txt      # Dependencies
├── .env.example          # Environment template
├── Dockerfile            # Docker image
├── docker-compose.yml    # Docker compose
├── Makefile             # Build commands
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Docker

Build and run with Docker:

```bash
# Build image
make docker-build

# Run container
make docker-run
```

## Testing

Run all tests:
```bash
make test
```

## Configuration

Configuration via `.env`:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4
AGENT_NAME=Thomas
AGENT_TEMPERATURE=0.7
AGENT_MAX_TOKENS=2000
LOG_LEVEL=INFO
DEBUG=False
```

## License

MIT License

## Support

- 📧 GitHub Issues: https://github.com/naveen12345naveen/Thomas-Buddy/issues
- 💬 Discussions: https://github.com/naveen12345naveen/Thomas-Buddy/discussions
