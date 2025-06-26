import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, ".env"))

# Ensure environment variables are set
required_vars = [
    "GOOGLE_API_KEY",
]

agent = Agent(
    model=Gemini(
        id=os.environ["DEFAULT_MODEL"],
    ),
    tools=[
        ReasoningTools(add_instructions=True),
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        )
    ],
    instructions=[
        "Use tables to display data.",
        "Include sources in your response."
        "Only include the table in your response. No other text.",
    ],
)

agent.print_response(
    "Write a report on AAPL", 
    stream=True,
    show_full_reasoning=True,
    stream_intermediate_steps=True
)
