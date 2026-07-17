"""Tool registry and tool implementations."""

import json
import requests
from typing import Callable, Dict, Any, Optional, List
from datetime import datetime
import logging
from src.models import ToolDefinition, ToolCall


logger = logging.getLogger(__name__)


class ToolRegistry:
    """Registry for managing tools the agent can use."""
    
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
    
    def register(
        self,
        name: str,
        description: str,
        func: Callable,
        parameters: Optional[Dict[str, Any]] = None
    ) -> None:
        """Register a tool."""
        if parameters is None:
            parameters = {}
        
        self.tools[name] = {
            "func": func,
            "description": description,
            "parameters": parameters
        }
        logger.info(f"Registered tool: {name}")
    
    def get_tool(self, name: str) -> Optional[Callable]:
        """Get a tool by name."""
        if name in self.tools:
            return self.tools[name]["func"]
        return None
    
    def get_definitions(self) -> List[Dict[str, Any]]:
        """Get all tool definitions in OpenAI format."""
        definitions = []
        for name, tool in self.tools.items():
            definitions.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool["description"],
                    "parameters": {
                        "type": "object",
                        "properties": tool.get("parameters", {}),
                        "required": list(tool.get("parameters", {}).keys())
                    }
                }
            })
        return definitions
    
    def execute(self, tool_name: str, **kwargs) -> str:
        """Execute a tool."""
        tool_func = self.get_tool(tool_name)
        if not tool_func:
            error_msg = f"Tool '{tool_name}' not found"
            logger.error(error_msg)
            return json.dumps({"error": error_msg})
        
        try:
            logger.info(f"Executing tool: {tool_name} with args: {kwargs}")
            result = tool_func(**kwargs)
            logger.info(f"Tool {tool_name} executed successfully")
            return json.dumps({"success": True, "result": result})
        except Exception as e:
            error_msg = f"Error executing tool '{tool_name}': {str(e)}"
            logger.error(error_msg, exc_info=True)
            return json.dumps({"error": error_msg})


# Create global tool registry
tool_registry = ToolRegistry()


# ============= Built-in Tools =============

def search_web(query: str, max_results: int = 5) -> str:
    """
    Search the web for information.
    
    Args:
        query: Search query
        max_results: Maximum number of results to return
    
    Returns:
        Search results as formatted string
    """
    try:
        # Placeholder - replace with actual API (e.g., Google Search, DuckDuckGo)
        logger.info(f"Web search for: {query}")
        return f"Search results for '{query}' (Note: Real API integration needed)\n1. Result 1\n2. Result 2\n3. Result 3"
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return f"Failed to search: {str(e)}"


def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate(expression: str) -> str:
    """
    Perform a mathematical calculation.
    
    Args:
        expression: Mathematical expression to evaluate
    
    Returns:
        Result of the calculation
    """
    try:
        # Safe evaluation - only numbers and basic operators
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Invalid characters in expression"
        
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        logger.error(f"Calculation failed: {e}")
        return f"Calculation error: {str(e)}"


def get_weather(location: str) -> str:
    """
    Get weather information for a location.
    
    Args:
        location: City name or location
    
    Returns:
        Weather information
    """
    try:
        # Placeholder - replace with actual weather API
        logger.info(f"Fetching weather for: {location}")
        return f"Weather for {location}: Sunny, 72°F (Note: Real API integration needed)"
    except Exception as e:
        logger.error(f"Weather fetch failed: {e}")
        return f"Failed to get weather: {str(e)}"


def text_analysis(text: str, analysis_type: str = "summary") -> str:
    """
    Analyze text content.
    
    Args:
        text: Text to analyze
        analysis_type: Type of analysis (summary, sentiment, keywords)
    
    Returns:
        Analysis result
    """
    try:
        if analysis_type == "summary":
            # Simple summary - first 100 chars
            summary = text[:100] + "..." if len(text) > 100 else text
            return f"Summary: {summary}"
        elif analysis_type == "sentiment":
            return "Sentiment: Neutral (sentiment analysis not implemented)"
        elif analysis_type == "keywords":
            words = text.split()[:5]
            return f"Keywords: {', '.join(words)}"
        else:
            return f"Unknown analysis type: {analysis_type}"
    except Exception as e:
        logger.error(f"Text analysis failed: {e}")
        return f"Analysis error: {str(e)}"


def code_snippet(language: str, description: str) -> str:
    """
    Generate a code snippet.
    
    Args:
        language: Programming language
        description: What the code should do
    
    Returns:
        Generated code snippet
    """
    snippets = {
        "python": "print('Hello, World!')",
        "javascript": "console.log('Hello, World!');",
        "java": "System.out.println(\"Hello, World!\");",
        "csharp": "Console.WriteLine(\"Hello, World!\");",
    }
    
    code = snippets.get(language.lower(), "# Language not found")
    return f"```{language}\n{code}\n```"


# Register all built-in tools
def register_builtin_tools():
    """Register all built-in tools."""
    tool_registry.register(
        "search_web",
        "Search the web for information",
        search_web,
        {"query": {"type": "string", "description": "Search query"}}
    )
    
    tool_registry.register(
        "get_current_time",
        "Get the current date and time",
        get_current_time,
        {}
    )
    
    tool_registry.register(
        "calculate",
        "Perform mathematical calculations",
        calculate,
        {"expression": {"type": "string", "description": "Mathematical expression"}}
    )
    
    tool_registry.register(
        "get_weather",
        "Get weather information for a location",
        get_weather,
        {"location": {"type": "string", "description": "City name or location"}}
    )
    
    tool_registry.register(
        "text_analysis",
        "Analyze text content",
        text_analysis,
        {
            "text": {"type": "string", "description": "Text to analyze"},
            "analysis_type": {"type": "string", "description": "Type of analysis"}
        }
    )
    
    tool_registry.register(
        "code_snippet",
        "Generate code snippets",
        code_snippet,
        {
            "language": {"type": "string", "description": "Programming language"},
            "description": {"type": "string", "description": "What the code should do"}
        }
    )
