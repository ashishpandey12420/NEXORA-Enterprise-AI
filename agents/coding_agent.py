
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from custom_tools.file_tools import create_project_file

coding_agent = Agent(
    name="coding_agent",
    model=LiteLlm(
        model="ollama_chat/qwen2.5-coder:7b",
        api_base="http://localhost:11434"
    ),
    description="Writes code and creates project files.",
    instruction="""
    You are NEXORA Coding Agent.

    1. Write clean and efficient code.
    2. Create project files using create_project_file.
    3. Never modify the .env file.
    4. Never claim a file was saved unless the tool confirms success.
    5. Explain your work clearly.
    """,
    tools=[create_project_file]
)