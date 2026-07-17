"""Data models and schemas for the AI Agent."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class Message(BaseModel):
    """Represents a single message in the conversation."""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationHistory(BaseModel):
    """Represents the conversation history."""
    messages: List[Message] = Field(default_factory=list)
    session_id: str = Field(..., description="Unique session identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the history."""
        self.messages.append(Message(role=role, content=content))
        self.updated_at = datetime.utcnow()
    
    def get_messages_for_api(self) -> List[Dict[str, str]]:
        """Get messages in OpenAI API format."""
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]
    
    def clear(self) -> None:
        """Clear conversation history."""
        self.messages = []


class ToolDefinition(BaseModel):
    """Represents a tool the agent can use."""
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Tool parameters schema")


class ToolCall(BaseModel):
    """Represents a tool call by the agent."""
    tool_name: str = Field(..., description="Name of the tool to call")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments for the tool")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentResponse(BaseModel):
    """Represents the agent's response."""
    content: str = Field(..., description="Response content")
    tool_calls: List[ToolCall] = Field(default_factory=list, description="Any tool calls made")
    tokens_used: Optional[int] = Field(None, description="Tokens used for this response")
    processing_time: float = Field(default=0.0, description="Time taken to process in seconds")


class SystemPrompt(BaseModel):
    """System prompt configuration."""
    role: str = Field(default="assistant", description="Agent role")
    context: str = Field(..., description="Agent context and instructions")
    constraints: List[str] = Field(default_factory=list, description="Agent constraints")
    examples: List[Dict[str, str]] = Field(default_factory=list, description="Few-shot examples")
    
    def to_string(self) -> str:
        """Convert system prompt to string format."""
        prompt = f"Role: {self.role}\n\n{self.context}"
        
        if self.constraints:
            prompt += "\n\nConstraints:\n"
            for constraint in self.constraints:
                prompt += f"- {constraint}\n"
        
        return prompt
