"""Core AI Agent implementation."""

import json
import time
import logging
import uuid
from typing import Optional, List, Dict, Any
from openai import OpenAI, APIError

from src.config import Config
from src.models import (
    ConversationHistory, Message, AgentResponse, SystemPrompt, ToolCall
)
from src.tools import tool_registry, register_builtin_tools


logger = logging.getLogger(__name__)


class AIAgent:
    """Main AI Agent class."""
    
    def __init__(
        self,
        name: str = "Thomas",
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None
    ):
        """
        Initialize the AI Agent.
        
        Args:
            name: Agent name
            system_prompt: System prompt for the agent
            config: Configuration object
        """
        self.name = name
        self.config = config or Config()
        self.config.validate()
        
        self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
        self.model = self.config.OPENAI_MODEL
        self.temperature = self.config.AGENT_TEMPERATURE
        self.max_tokens = self.config.AGENT_MAX_TOKENS
        
        # Session management
        self.session_id = str(uuid.uuid4())
        self.conversation_history = ConversationHistory(session_id=self.session_id)
        
        # System prompt
        self.system_prompt = system_prompt or self._default_system_prompt()
        
        # Register built-in tools
        register_builtin_tools()
        
        logger.info(f"Agent '{self.name}' initialized with session ID: {self.session_id}")
    
    def _default_system_prompt(self) -> str:
        """Get the default system prompt."""
        return f"""You are {self.name}, a helpful and intelligent AI assistant.

You are designed to:
- Answer questions accurately and thoroughly
- Help users with various tasks and problems
- Use available tools when appropriate to get information
- Think step-by-step to provide better solutions
- Be honest about limitations and uncertainties

When you need information, use the available tools. Always provide clear explanations of your reasoning."""
    
    def chat(self, user_message: str, use_tools: bool = True) -> AgentResponse:
        """
        Send a message to the agent and get a response.
        
        Args:
            user_message: User's message
            use_tools: Whether the agent can use tools
        
        Returns:
            AgentResponse object
        """
        start_time = time.time()
        
        try:
            # Add user message to history
            self.conversation_history.add_message("user", user_message)
            logger.info(f"User: {user_message}")
            
            # Prepare messages for API
            messages = self.conversation_history.get_messages_for_api()
            
            # Prepare API call kwargs
            api_kwargs = {
                "model": self.model,
                "messages": messages,
                "system": self.system_prompt,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            }
            
            # Add tools if enabled
            if use_tools:
                tools = tool_registry.get_definitions()
                if tools:
                    api_kwargs["tools"] = tools
                    api_kwargs["tool_choice"] = "auto"
            
            # Call OpenAI API
            response = self.client.chat.completions.create(**api_kwargs)
            
            # Process response
            assistant_message = response.choices[0].message
            tool_calls: List[ToolCall] = []
            
            # Handle tool calls if present
            if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
                tool_calls = self._handle_tool_calls(assistant_message.tool_calls)
            
            # Get assistant's text response
            content = assistant_message.content or ""
            
            if content:
                self.conversation_history.add_message("assistant", content)
            
            processing_time = time.time() - start_time
            
            logger.info(f"Assistant: {content}")
            logger.info(f"Processing time: {processing_time:.2f}s")
            
            return AgentResponse(
                content=content,
                tool_calls=tool_calls,
                tokens_used=response.usage.total_tokens if response.usage else None,
                processing_time=processing_time
            )
        
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            error_msg = f"API Error: {str(e)}"
            return AgentResponse(content=error_msg, processing_time=time.time() - start_time)
        except Exception as e:
            logger.error(f"Error in chat: {e}", exc_info=True)
            error_msg = f"Error: {str(e)}"
            return AgentResponse(content=error_msg, processing_time=time.time() - start_time)
    
    def _handle_tool_calls(self, tool_calls_data: List[Any]) -> List[ToolCall]:
        """
        Handle tool calls from the assistant.
        
        Args:
            tool_calls_data: Tool calls from OpenAI response
        
        Returns:
            List of ToolCall objects
        """
        tool_calls = []
        
        for tool_call in tool_calls_data:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            logger.info(f"Tool call: {tool_name} with args: {arguments}")
            
            # Execute the tool
            result = tool_registry.execute(tool_name, **arguments)
            
            # Add tool call to history
            tool_call_obj = ToolCall(tool_name=tool_name, arguments=arguments)
            tool_calls.append(tool_call_obj)
            
            # Add tool result to conversation
            self.conversation_history.add_message("assistant", f"Tool: {tool_name}")
            self.conversation_history.add_message("user", f"Tool result: {result}")
        
        return tool_calls
    
    def reset_conversation(self) -> None:
        """Reset the conversation history."""
        self.conversation_history.clear()
        self.session_id = str(uuid.uuid4())
        logger.info(f"Conversation reset. New session ID: {self.session_id}")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        return self.conversation_history.get_messages_for_api()
    
    def set_system_prompt(self, prompt: str) -> None:
        """Set a new system prompt."""
        self.system_prompt = prompt
        logger.info("System prompt updated")
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get information about the current session."""
        return {
            "session_id": self.session_id,
            "agent_name": self.name,
            "model": self.model,
            "message_count": len(self.conversation_history.messages),
            "created_at": self.conversation_history.created_at.isoformat(),
            "updated_at": self.conversation_history.updated_at.isoformat()
        }
    
    def interactive_chat(self) -> None:
        """Start an interactive chat session."""
        print(f"\n{'='*60}")
        print(f"Welcome to {self.name}!")
        print(f"Session ID: {self.session_id}")
        print(f"Type 'exit' to quit, 'reset' to clear history, 'info' for session info")
        print(f"{'='*60}\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "exit":
                    print("Goodbye!")
                    break
                
                if user_input.lower() == "reset":
                    self.reset_conversation()
                    print("Conversation reset.\n")
                    continue
                
                if user_input.lower() == "info":
                    info = self.get_session_info()
                    print(f"\nSession Info: {json.dumps(info, indent=2)}\n")
                    continue
                
                # Get response from agent
                response = self.chat(user_input)
                print(f"\n{self.name}: {response.content}\n")
                
                if response.tool_calls:
                    print(f"Tools used: {[tc.tool_name for tc in response.tool_calls]}\n")
            
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"Error in interactive chat: {e}", exc_info=True)
                print(f"Error: {str(e)}\n")
