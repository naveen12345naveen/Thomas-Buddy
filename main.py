"""Main entry point for the AI Agent."""

import sys
import logging
from src.config import Config, setup_logging
from src.agent import AIAgent


def main():
    """Main function."""
    # Setup configuration and logging
    config = Config()
    logger = setup_logging(config)
    
    logger.info("Starting AI Agent: Thomas Buddy")
    logger.info(f"Model: {config.OPENAI_MODEL}")
    logger.info(f"Debug mode: {config.DEBUG}")
    
    try:
        # Create agent
        agent = AIAgent(
            name=config.AGENT_NAME,
            config=config
        )
        
        # Start interactive chat
        agent.interactive_chat()
    
    except KeyboardInterrupt:
        logger.info("Agent interrupted by user")
        print("\nAgent stopped.")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
