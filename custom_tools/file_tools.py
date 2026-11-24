
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

MAX_FILE_SIZE = 1_000_000  # 1 MB

PROTECTED_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".git",
    ".ssh",
    "id_rsa",
    "id_ed25519",
    "credentials.json",
    "secrets.json",
}

PROTECTED_EXTENSIONS = {
    ".pem",
    ".key",
    ".p12",
    ".pfx",
}


def get_safe_path(file_path: str):
    """Validate and return a safe project path."""

    if not isinstance(file_path, str) or not file_path.strip():
        raise ValueError("Invalid file path.")

    target = (PROJECT_DIR / file_path).resolve()

    if not target.is_relative_to(PROJECT_DIR):
        raise ValueError("Access denied: Outside project directory.")

    for part in target.relative_to(PROJECT_DIR).parts:
        name = part.casefold()

        if name in PROTECTED_NAMES or name.startswith(".env"):
            raise ValueError("Access denied: Protected file or folder.")

        if Path(name).suffix in PROTECTED_EXTENSIONS:
            raise ValueError("Access denied: Protected file extension.")

    return target


def create_project_file(
    file_path: str,
    content: str,
    overwrite_approved: bool = False
):
    """Create a project file. Existing files need explicit approval."""

    try:
        if not isinstance(content, str):
            return "ERROR: Content must be text."

        if len(content.encode("utf-8")) > MAX_FILE_SIZE:
            return "ERROR: File size exceeds 1 MB limit."

        target = get_safe_path(file_path)

        if target.exists() and not overwrite_approved:
            return (
                "APPROVAL REQUIRED: File already exists. "
                "Ask the user before overwriting it."
            )

        target.parent.mkdir(parents=True, exist_ok=True)

        if overwrite_approved:
            target.write_text(content, encoding="utf-8")
        else:
            with target.open("x", encoding="utf-8") as file:
                file.write(content)

        return f"SUCCESS: File saved: {file_path}"

    except FileExistsError:
        return "ERROR: File already exists. Approval is required to overwrite."

    except Exception as e:
        return f"ERROR: {str(e)}"


def read_project_file(file_path: str):
    """Read a permitted project file."""

    try:
        target = get_safe_path(file_path)

        if not target.is_file():
            return "ERROR: File does not exist."

        if target.stat().st_size > MAX_FILE_SIZE:
            return "ERROR: File exceeds 1 MB read limit."

        return target.read_text(encoding="utf-8")

    except Exception as e:
        return f"ERROR: {str(e)}"