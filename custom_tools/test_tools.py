from pathlib import Path
import subprocess
import sys

PROJECT_DIR = Path(__file__).resolve().parent.parent


def run_python_file(file_path: str) -> str:
    """Run a Python file inside the NEXORA project."""

    try:
        target = (PROJECT_DIR / file_path).resolve()

        if not target.is_relative_to(PROJECT_DIR):
            return "ERROR: Access outside project is not allowed."

        if target.suffix != ".py":
            return "ERROR: Only Python files are allowed."

        if not target.is_file():
            return "ERROR: File does not exist."

        result = subprocess.run(
            [sys.executable, str(target)],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=20
        )

        return (
            f"Exit Code: {result.returncode}\n"
            f"Output:\n{result.stdout}\n"
            f"Errors:\n{result.stderr}"
        )

    except subprocess.TimeoutExpired:
        return "ERROR: Execution timed out."

    except Exception as e:
        return f"ERROR: {e}"