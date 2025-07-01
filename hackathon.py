import asyncio
import os
from dotenv import load_dotenv

import nest_asyncio
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from agno.playground import Playground
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.mcp import MCPTools

# This is the URL of the MCP server we want to use.
server_url = "http://localhost:8000/mcp"

# Allow nested event loops
nest_asyncio.apply()

agent_storage_file: str = "tmp/agents.db"

load_dotenv()

async def run_server() -> None:

    # Create a client session to connect to the MCP server
    async with MCPTools(transport="streamable-http", url=server_url) as mcp_tools:
        agent = Agent(
            name="Finance Agent",
            model=Gemini(
                id=os.environ["DEFAULT_MODEL"],
            ),
            tools=[mcp_tools],
            instructions=["Always use tables to display data. If the stock is related to Indian Stock use .NS to the symbol for example if the stock symbol is SBIN then add SBIN.NS to it"],
            storage=SqliteAgentStorage(table_name="finance_agent", db_file=agent_storage_file),
            add_datetime_to_instructions=True,
            add_history_to_messages=True,
            num_history_responses=5,
            markdown=True,
        )

        playground = Playground(agents=[agent])
        app = playground.get_app()

        # Serve the app while keeping the MCPTools context manager alive
        playground.serve(app)

if __name__ == "__main__":
    asyncio.run(run_server())
