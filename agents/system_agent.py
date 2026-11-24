
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

system_agent = Agent(
    name="system_agent",

    model=LiteLlm(
        model="ollama_chat/qwen2.5-coder:7b",
        api_base="http://localhost:11434"
    ),

    description="Helps manage Windows, VS Code, files and system tasks.",

    instruction="""
    You are NEXORA System Control Agent.

    1. Help manage Windows, VS Code, files and folders.
    2. Give safe step-by-step instructions.
    3. Never claim direct computer control without tools.
    4. Ask for approval before destructive actions.
    5. Explain every action clearly.
    """
)