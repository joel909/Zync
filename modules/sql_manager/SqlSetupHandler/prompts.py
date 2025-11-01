# modules/sql_manager/SqlSetupHandler/prompts.py
"""
User prompts and environment instructions.
Handles collecting user input and displaying setup instructions.
"""


def prompt_user(question: str) -> str:
    """
    Prompt user with a yes/no question.
    
    Args:
        question: The question to ask the user
    
    Returns:
        str: User's response (lowercase)
    """
    return input(f"\n{question} (yes/no): ").strip().lower()


def get_raw_password(prompt: str = "Enter password: ") -> str:
    """
    Get password input from user (raw input, not masked).
    
    Args:
        prompt: Custom prompt text
    
    Returns:
        str: Password entered by user
    """
    return input(prompt)


def create_env_instructions(host: str, user: str, password: str, db_name: str) -> None:
    """
    Display .env file creation instructions to user.
    
    This function shows:
    1. Environment variable values
    2. Manual file creation steps
    3. PowerShell automation command
    
    Args:
        host: MySQL host
        user: MySQL user
        password: MySQL password
        db_name: Database name
    """
    print("\n" + "=" * 70)
    print("ENVIRONMENT VARIABLES - CREATE .env FILE")
    print("=" * 70)
    print("\nCreate a file named '.env' in your project root with these contents:\n")
    print("DB_HOST=" + host)
    print("DB_USER=" + user)
    print("DB_PASSWORD=" + password)
    print("DB_NAME=" + db_name)
    print("\n" + "=" * 70)
    print("\nSteps to create .env:")
    print("1. Open a text editor (Notepad, VSCode, etc.)")
    print("2. Copy the above 4 lines (without this guidance text)")
    print("3. Save as '.env' in the project root directory")
    print("   Location: c:\\Users\\joelj\\Desktop\\Programing\\Zync\\.env")
    print("\nAlternatively, from PowerShell in the project root, run:")
    print("  @'")
    print("  DB_HOST=" + host)
    print("  DB_USER=" + user)
    print("  DB_PASSWORD=" + password)
    print("  DB_NAME=" + db_name)
    print("  '@ | Out-File -Encoding utf8 .env")
    print("=" * 70 + "\n")
