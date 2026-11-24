
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from custom_tools.file_tools import (
    read_project_file,
    create_project_file
)

debugging_agent = Agent(
    name="debugging_agent",

    model=LiteLlm(
        model="ollama_chat/qwen2.5-coder:7b",
        api_base="http://localhost:11434"
    ),

    description="Reads project files, finds coding errors and saves corrected code.",

    instruction="""
    You are NEXORA Debugging Agent.

    1. Read project files using read_project_file.
    2. Analyze code and find actual errors.
    3. Explain the cause of each error.
    4. Fix errors without unnecessary changes.
    5. Save corrected code using create_project_file.
    6. Never claim code was tested unless actually tested.
    7. Never modify .env files.
    8. Explain changes before replacing existing files.
    9. Ask user approval before modifying existing files.
    """,

    tools=[
        read_project_file,
        create_project_file
    ]
)