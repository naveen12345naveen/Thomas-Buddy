"""Advanced usage examples."""

import json
from src.config import Config, setup_logging
from src.agent import AIAgent
from src.tools import tool_registry


def example_1_specialized_agent():
    """Example 1: Create a specialized domain expert agent."""
    print("="*60)
    print("Example 1: Specialized Domain Expert Agent")
    print("="*60)
    
    config = Config()
    logger = setup_logging(config)
    
    # Create specialized agent
    python_expert_prompt = """You are an expert Python developer with 15+ years of experience.

Your specializations:
- Advanced Python patterns and best practices
- Performance optimization
- Design patterns
- Testing and debugging
- Code reviews

Always provide:
- Detailed explanations
- Code examples
- Performance considerations
- Alternative approaches
- Best practices

Be concise but thorough in your responses."""
    
    agent = AIAgent(name="PythonExpert")
    agent.set_system_prompt(python_expert_prompt)
    
    response = agent.chat("What are the best practices for writing async code in Python?")
    print(f"\nAgent: {response.content}\n")


def example_2_multi_turn_conversation():
    """Example 2: Multi-turn conversation with context."""
    print("="*60)
    print("Example 2: Multi-turn Conversation")
    print("="*60)
    
    config = Config()
    logger = setup_logging(config)
    
    agent = AIAgent(name="Thomas")
    
    # Simulate a multi-turn conversation
    messages = [
        "Tell me about machine learning",
        "What are the main types?",
        "How does neural networks work?",
        "Can you give me a simple example?"
    ]
    
    for msg in messages:
        print(f"\nUser: {msg}")
        response = agent.chat(msg)
        print(f"Agent: {response.content}")
        print(f"Processing time: {response.processing_time:.2f}s")


def main():
    """Run all examples."""
    examples = [
        example_1_specialized_agent,
        example_2_multi_turn_conversation,
    ]
    
    for example in examples:
        try:
            example()
            print("\n")
        except Exception as e:
            print(f"Error in {example.__name__}: {e}\n")


if __name__ == "__main__":
    main()
