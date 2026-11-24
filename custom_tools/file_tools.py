
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent


def get_safe_path(file_path):
    target = (PROJECT_DIR / file_path).resolve()

    if not target.is_relative_to(PROJECT_DIR):
        raise ValueError("Access denied: Outside project directory")

    return target


def create_project_file(file_path: str, content: str):
    try:
        target = get_safe_path(file_path)

        target.parent.mkdir(parents=True, exist_ok=True)

        target.write_text(content, encoding="utf-8")

        return f"SUCCESS: File saved: {file_path}"

    except Exception as e:
        return f"ERROR: {str(e)}"


def read_project_file(file_path: str):
    try:
        target = get_safe_path(file_path)

        if not target.exists():
            return "ERROR: File does not exist"

        return target.read_text(encoding="utf-8")

    except Exception as e:
        return f"ERROR: {str(e)}"