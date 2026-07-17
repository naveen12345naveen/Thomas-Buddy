"""Configuration management for the AI Agent."""

import os
from dotenv import load_dotenv
from typing import Optional
import logging

load_dotenv()


class Config:
    """Main configuration class."""
    
    # OpenAI Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Agent Settings
    AGENT_NAME: str = os.getenv("AGENT_NAME", "Thomas")
    AGENT_TEMPERATURE: float = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
    AGENT_MAX_TOKENS: int = int(os.getenv("AGENT_MAX_TOKENS", "2000"))
    AGENT_TIMEOUT: int = int(os.getenv("AGENT_TIMEOUT", "60"))
    
    # Logging Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/agent.log")
    
    # System Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    MAX_CONVERSATION_HISTORY: int = 50
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set. Please configure it in .env file.")
        return True


def setup_logging(config: Config) -> logging.Logger:
    """Setup logging configuration."""
    log_dir = os.path.dirname(config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)
