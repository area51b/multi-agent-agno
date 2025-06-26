import os
from fastapi import FastAPI
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, ".env"))

router = FastAPI()

class Body(BaseModel):
    message: str

storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agents.db")
memory = Memory(
    db=SqliteMemoryDb(table_name="memory", db_file="tmp/memory.db"),
    model=Gemini(
        id=os.environ["DEFAULT_MODEL"],
    ),
)

# Ensure environment variables are set
required_vars = [
    "GOOGLE_API_KEY",
]

agent = Agent(
    session_id="s_1234",
    user_id="u_123",
    model=Gemini(
        id=os.environ["DEFAULT_MODEL"],
    ),
    add_history_to_messages=True,
    storage=storage,
    memory=memory,
    enable_agentic_memory=True,
)

#if __name__ == "__main__":
    #agent.print_response("My name is Bala")
    #agent.print_response("What is my name?")

@router.post("/run")
async def run(body: Body):
    response = agent.run(body.message)
    return {"response": response.content}

#run like this ->
#python -m uvicorn storage_example:router --reload
