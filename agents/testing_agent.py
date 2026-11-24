
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from custom_tools.test_tools import run_python_file

testing_agent = Agent(
    name="testing_agent",

    model=LiteLlm(
        model="ollama_chat/qwen2.5-coder:7b",
        api_base="http://localhost:11434"
    ),

    description="Tests Python programs and analyzes execution results.",

    instruction="""
    You are NEXORA Testing Agent.

    Your responsibilities:

    1. Ask the user for permission before executing any Python file.
    2. Execute only the file approved by the user.
    3. Use run_python_file to execute the approved file.
    4. Check the exit code, output and errors.
    5. Identify bugs and failed test cases.
    6. Report PASS or FAIL with clear reasons.
    7. Never claim a test passed without actual execution.
    8. Never modify project files.
    9. Never execute .env files or unknown scripts.
    10. Explain test results in simple language.

    Always provide accurate test reports.
    """,

    tools=[run_python_file]
)