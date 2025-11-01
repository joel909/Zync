# modules/sql_manager/SqlSetupHandler/main.py
"""
Main setup wizard orchestration.
Coordinates the entire database setup flow.
"""

import os
import sys
from dotenv import load_dotenv
from .schema import DEFAULT_SCHEMA
from .database import create_database_and_setup
from .validators import check_database_schema
from .prompts import prompt_user, get_raw_password, create_env_instructions


def create_env_file(host: str, user: str, password: str, db_name: str) -> bool:
    """
    Create .env file in project root with database credentials.
    
    Args:
        host: MySQL host
        user: MySQL user
        password: MySQL password
        db_name: Database name
    
    Returns:
        bool: True on success, False on failure
    """
    try:
        env_content = f"""DB_HOST={host}
DB_USER={user}
DB_PASSWORD={password}
DB_NAME={db_name}
"""
        
        # Write to .env file in current working directory (project root)
        with open(".env", "w") as env_file:
            env_file.write(env_content)
        
        print("\n[✓] .env file created successfully at: .env")
        print(f"    DB_HOST={host}")
        print(f"    DB_USER={user}")
        print(f"    DB_PASSWORD={'*' * len(password)}")  # Hide password in output
        print(f"    DB_NAME={db_name}")
        return True
        
    except Exception as e:
        print(f"\n[✗] Failed to create .env file: {e}")
        return False


def run_setup_wizard() -> None:
    """
    Main setup wizard flow.
    
    This is the primary orchestration function that:
    1. Checks for existing .env and environment variables
    2. Asks user if project is already set up
    3. If not: collects credentials, creates database, validates schema
    4. If yes: verifies existing database schema
    5. Shows .env creation instructions
    
    The function will exit with status 0 on success or 1 on failure.
    """
    # Load .env if it exists
    load_dotenv()
    
    # Check environment status
    dot_env_file_exists = os.path.exists(".env")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME", "zyncdb_users")
    
    env_vars_exist = bool(DB_HOST and DB_USER and DB_PASSWORD)
    
    # Display header
    print("\n" + "=" * 70)
    print("ZYNC DATABASE SETUP WIZARD")
    print("=" * 70)

    # Check current status
    print(f"\n[*] Checking environment...")
    print(f"    .env file exists: {dot_env_file_exists}")
    print(f"    Environment variables set: {env_vars_exist}")

    # If env vars already set, verify and exit
    if env_vars_exist:
        print(f"\n[✓] Environment variables are already configured.")
        print(f"    Host: {DB_HOST}")
        print(f"    User: {DB_USER}")
        print(f"    Database: {DB_NAME}")
        
        # Proceed to schema check
        success, missing = check_database_schema(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
        if success:
            print("\n[✓] All done! Your database is ready to use.")
            sys.exit(0)
        else:
            print("\n[✗] Schema validation failed. Please fix the issues above.")
            sys.exit(1)
    
    # Ask user if project is set up
    print("\n" + "-" * 70)
    response = prompt_user("Have you already set up the database project on this system?")
    
    if response.lower() in ["yes", "y"]:
        # User says project is already set up
        print("\n[*] Assuming database already exists...")
        print("\n[!] Please provide your database credentials to verify the setup.\n")
        
        host = input("Enter DB_HOST (default: 169.254.196.213): ").strip() or "169.254.196.213"
        user = input("Enter DB_USER (default: zync): ").strip() or "zync"
        password = get_raw_password("Enter DB_PASSWORD: ")
        db_name = input("Enter DB_NAME (default: zyncdb_users): ").strip() or "zyncdb_users"
        
        # Show .env instructions
        create_env_instructions(host, user, password, db_name)
        
        # Check schema
        print("[*] Verifying database schema...")
        success, missing = check_database_schema(host, user, password, db_name)
        
        if success:
            print("\n[✓] Setup verified! Your database is ready.")
        else:
            print("\n[✗] Database schema is incomplete or missing.")
            print(f"    Missing tables: {', '.join(missing)}")
            sys.exit(1)
    
    else:
        # User says project needs to be set up
        print("\n[*] Starting fresh project setup...\n")
        
        # Get credentials from user
        print("Please provide your MySQL credentials:\n")
        host = input("Enter DB_HOST (default: localhost): ").strip() or "localhost"
        user = input("Enter DB_USER (default: root): ").strip() or "root"
        password = get_raw_password("Enter DB_PASSWORD: ")
        db_name = input("Enter DB_NAME (default: zyncdb_users): ").strip() or "zyncdb_users"
        
        # Create database and schema
        print("\n[*] Setting up database...")
        success = create_database_and_setup(host, user, password, db_name, schema_sql=DEFAULT_SCHEMA)
        
        if success:
            print("\n[✓] Database and schema created successfully!\n")
            
            # Show .env instructions
            create_env_instructions(host, user, password, db_name)
            
            # Verify the setup
            print("[*] Verifying setup...")
            success, missing = check_database_schema(host, user, password, db_name)
            
            if success:
                # Create .env file automatically
                print("\n[*] Creating .env file...")
                env_created = create_env_file(host, user, password, db_name)
                
                if env_created:
                    print("\n[✓] All done! Your database is ready and .env file has been created.")
                else:
                    print("\n[!] Database is ready but .env file creation failed.")
                    print("    You can create it manually with the credentials shown above.")
            else:
                print("\n[!] Database created but schema verification failed.")
                print(f"    Missing tables: {', '.join(missing)}")
                sys.exit(1)
        else:
            print("\n[✗] Failed to set up database. Please check your credentials and try again.")
            sys.exit(1)

    print("\n" + "=" * 70)
    print("Setup complete! You can now start your Flask app.")
    print("=" * 70 + "\n")
