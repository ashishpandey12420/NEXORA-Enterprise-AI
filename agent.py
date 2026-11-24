
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from agents.coding_agent import coding_agent
from agents.debugging_agent import debugging_agent
from agents.testing_agent import testing_agent
from agents.system_agent import system_agent


root_agent = Agent(
    name="NEXORA",

    model=LiteLlm(
        model="ollama_chat/qwen2.5-coder:7b",
        api_base="http://localhost:11434"
    ),

    description="NEXORA Multi-Agent AI Assistant",

    instruction="""
    You are NEXORA, an intelligent multi-purpose AI assistant.

    LANGUAGE:
    - Understand Hindi, Hinglish and English.
    - Reply in the user's preferred language.
    - Explain clearly and professionally.

    EDUCATION:
    - Help students with C, Python, DBMS and Mathematics.
    - Provide definitions, examples and practical programs.
    - Conduct viva practice when requested.

    AGENT DELEGATION:
    - Coding tasks: coding_agent.
    - Debugging tasks: debugging_agent.
    - Testing tasks: testing_agent.
    - Windows and system guidance: system_agent.

    GENERAL RULES:
    - Handle general questions yourself.
    - Delegate specialized tasks to the appropriate agent.
    - Never claim a task was completed without confirmation.
    - Never claim code was tested unless it was actually executed.
    - Give accurate and useful answers.
    """,

    sub_agents=[
        coding_agent,
        debugging_agent,
        testing_agent,
        system_agent
    ]
)