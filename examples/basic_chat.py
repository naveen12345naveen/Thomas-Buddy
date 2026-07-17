"""Basic chat example."""

from src.config import Config, setup_logging
from src.agent import AIAgent


def main():
    """Run basic chat example."""
    # Setup
    config = Config()
    logger = setup_logging(config)
    
    # Create agent
    agent = AIAgent(name="Thomas", config=config)
    
    print(f"Agent: {agent.name}")
    print(f"Session: {agent.session_id}\n")
    
    # Example conversations
    conversations = [
        "What is Python?",
        "Can you calculate 15 * 8?",
        "What's the current time?",
        "Tell me a joke"
    ]
    
    for user_message in conversations:
        print(f"User: {user_message}")
        response = agent.chat(user_message)
        print(f"Agent: {response.content}")
        print(f"Time: {response.processing_time:.2f}s\n")


if __name__ == "__main__":
    main()
