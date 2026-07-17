"""Example with custom tools."""

from src.config import Config, setup_logging
from src.agent import AIAgent
from src.tools import tool_registry


def main():
    """Run example with custom tools."""
    # Setup
    config = Config()
    logger = setup_logging(config)
    
    # Create agent
    agent = AIAgent(name="Thomas", config=config)
    
    # Add custom tools
    def get_stock_price(symbol: str) -> str:
        """Get stock price (placeholder)."""
        prices = {"AAPL": "$150.25", "GOOGL": "$140.80", "MSFT": "$380.50"}
        return prices.get(symbol.upper(), f"Price for {symbol} not found")
    
    def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
        """Convert currency (placeholder)."""
        rates = {"USD": 1.0, "EUR": 0.92, "GBP": 0.73, "JPY": 149.50}
        
        if from_currency.upper() not in rates or to_currency.upper() not in rates:
            return "Currency not found"
        
        result = amount * (rates[to_currency.upper()] / rates[from_currency.upper()])
        return f"{amount} {from_currency.upper()} = {result:.2f} {to_currency.upper()}"
    
    # Register custom tools
    tool_registry.register(
        "get_stock_price",
        "Get current stock price for a symbol",
        get_stock_price,
        {"symbol": {"type": "string", "description": "Stock ticker symbol"}}
    )
    
    tool_registry.register(
        "convert_currency",
        "Convert between currencies",
        convert_currency,
        {
            "amount": {"type": "number", "description": "Amount to convert"},
            "from_currency": {"type": "string", "description": "Source currency"},
            "to_currency": {"type": "string", "description": "Target currency"}
        }
    )
    
    print(f"Agent: {agent.name}")
    print(f"Session: {agent.session_id}\n")
    print("Available custom tools:")
    print("- get_stock_price")
    print("- convert_currency\n")
    
    # Example conversations
    conversations = [
        "What's the price of Apple stock?",
        "Convert 100 USD to EUR",
        "How much is Microsoft stock in Japanese Yen?"
    ]
    
    for user_message in conversations:
        print(f"User: {user_message}")
        response = agent.chat(user_message, use_tools=True)
        print(f"Agent: {response.content}")
        if response.tool_calls:
            print(f"Tools: {[tc.tool_name for tc in response.tool_calls]}")
        print()


if __name__ == "__main__":
    main()
