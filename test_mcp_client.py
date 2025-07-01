import asyncio
import os
from dotenv import load_dotenv

from agno.agent import Agent
from uvicorn import Config, Server
from agno.tools.mcp import MCPTools
from agno.models.google import Gemini
from agno.playground import Playground
from agno.storage.agent.sqlite import SqliteAgentStorage

agent_storage_file: str = "tmp/agents.db"
server_url = "http://localhost:8000/mcp"

load_dotenv()

async def run_server() -> None:
    mcp_tools = MCPTools(transport="streamable-http", url=server_url)
    await mcp_tools.__aenter__()  # manually enter context manager

    agent = Agent(
        name="Agent X",
        model=Gemini(id=os.environ["DEFAULT_MODEL"]),
        tools=[mcp_tools],
        instructions=[
            "you are an helpful agent"
        ],
        storage=SqliteAgentStorage(table_name="agent_x", db_file=agent_storage_file),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )

    playground = Playground(agents=[agent])
    app = playground.get_app()

    # Replace playground.serve() to avoid asyncio.run nesting
    config = Config(app=app, host="0.0.0.0", port=7777)
    server = Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run_server())
