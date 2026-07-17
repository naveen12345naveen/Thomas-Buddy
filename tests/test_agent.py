"""Unit tests for the AI Agent."""

import pytest
import json
from src.config import Config
from src.agent import AIAgent
from src.models import ConversationHistory, Message
from src.tools import tool_registry, search_web, calculate, get_current_time


class TestConversationHistory:
    """Test ConversationHistory model."""
    
    def test_add_message(self):
        """Test adding messages to history."""
        history = ConversationHistory(session_id="test-123")
        history.add_message("user", "Hello")
        history.add_message("assistant", "Hi there!")
        
        assert len(history.messages) == 2
        assert history.messages[0].content == "Hello"
        assert history.messages[1].content == "Hi there!"
    
    def test_get_messages_for_api(self):
        """Test getting messages in API format."""
        history = ConversationHistory(session_id="test-123")
        history.add_message("user", "Hello")
        history.add_message("assistant", "Hi!")
        
        api_messages = history.get_messages_for_api()
        assert len(api_messages) == 2
        assert api_messages[0]["role"] == "user"
        assert api_messages[0]["content"] == "Hello"
    
    def test_clear_history(self):
        """Test clearing history."""
        history = ConversationHistory(session_id="test-123")
        history.add_message("user", "Hello")
        history.clear()
        
        assert len(history.messages) == 0


class TestToolRegistry:
    """Test ToolRegistry."""
    
    def test_register_tool(self):
        """Test registering a tool."""
        registry = tool_registry
        
        # Should have built-in tools registered
        assert len(registry.tools) > 0
    
    def test_get_tool(self):
        """Test getting a tool."""
        registry = tool_registry
        tool = registry.get_tool("calculate")
        
        assert tool is not None
        assert callable(tool)
    
    def test_tool_execution(self):
        """Test executing a tool."""
        result = calculate("2 + 2")
        assert "4" in result
    
    def test_get_current_time(self):
        """Test get_current_time tool."""
        result = get_current_time()
        assert len(result) > 0
        assert "-" in result  # Date format check


class TestAgent:
    """Test AIAgent."""
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        agent = AIAgent(name="TestAgent")
        
        assert agent.name == "TestAgent"
        assert agent.session_id is not None
        assert len(agent.session_id) > 0
    
    def test_default_system_prompt(self):
        """Test default system prompt."""
        agent = AIAgent()
        
        assert "Thomas" in agent.system_prompt
        assert "helpful" in agent.system_prompt.lower()
    
    def test_set_system_prompt(self):
        """Test setting a custom system prompt."""
        agent = AIAgent()
        new_prompt = "You are a testing agent."
        agent.set_system_prompt(new_prompt)
        
        assert agent.system_prompt == new_prompt
    
    def test_reset_conversation(self):
        """Test resetting conversation."""
        agent = AIAgent()
        old_session = agent.session_id
        
        agent.conversation_history.add_message("user", "Test")
        agent.reset_conversation()
        
        assert agent.session_id != old_session
        assert len(agent.conversation_history.messages) == 0
    
    def test_get_session_info(self):
        """Test getting session info."""
        agent = AIAgent(name="InfoAgent")
        info = agent.get_session_info()
        
        assert info["agent_name"] == "InfoAgent"
        assert info["session_id"] is not None
        assert "model" in info
    
    def test_get_conversation_history(self):
        """Test getting conversation history."""
        agent = AIAgent()
        agent.conversation_history.add_message("user", "Hello")
        agent.conversation_history.add_message("assistant", "Hi!")
        
        history = agent.get_conversation_history()
        assert len(history) == 2
        assert history[0]["role"] == "user"


class TestTools:
    """Test built-in tools."""
    
    def test_calculate_addition(self):
        """Test calculate tool with addition."""
        result = calculate("5 + 3")
        assert "8" in result
    
    def test_calculate_multiplication(self):
        """Test calculate tool with multiplication."""
        result = calculate("6 * 7")
        assert "42" in result
    
    def test_calculate_invalid_characters(self):
        """Test calculate tool with invalid input."""
        result = calculate("5 + import os")
        assert "Invalid" in result or "error" in result.lower()
    
    def test_get_current_time_format(self):
        """Test get_current_time format."""
        result = get_current_time()
        parts = result.split(" ")
        
        assert len(parts) == 2  # Date and time
        assert len(parts[0].split("-")) == 3  # YYYY-MM-DD


class TestConfig:
    """Test Configuration."""
    
    def test_config_defaults(self):
        """Test config defaults."""
        config = Config()
        
        assert config.AGENT_TEMPERATURE > 0
        assert config.AGENT_MAX_TOKENS > 0
        assert config.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
