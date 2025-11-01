# modules/sql_manager/SqlSetupHandler/__init__.py
"""
SqlSetupHandler - Database setup and management for Zync project.

This module provides the SqlSetupHandler class which orchestrates
database operations by using functions from modular files:
- schema.py: Database schema definitions
- database.py: Database creation and operations
- validators.py: Schema validation
- prompts.py: User input and instructions
- main.py: Setup wizard orchestration

Usage:
    from modules.sql_manager.SqlSetupHandler import SqlSetupHandler
    
    handler = SqlSetupHandler()
    handler.run_setup_wizard()
"""

import os
import sys
from dotenv import load_dotenv

# Import functions from modular files
from .schema import DEFAULT_SCHEMA, REQUIRED_TABLES
from .database import create_database_and_setup
from .validators import check_database_schema
from .prompts import prompt_user, get_raw_password, create_env_instructions
from .main import run_setup_wizard as main_run_setup_wizard, create_env_file


class SqlSetupHandler:
    """
    Database setup and management handler for Zync project.
    
    This class orchestrates database operations using functions from:
    - schema.py: Database schema definitions
    - database.py: Database creation and operations
    - validators.py: Schema validation
    - prompts.py: User input and instructions
    - main.py: Setup wizard orchestration
    
    Attributes:
        REQUIRED_TABLES: Tables that must exist in the database
        DEFAULT_SCHEMA: SQL CREATE TABLE statements (idempotent)
    """
    
    # Import schema definitions from schema.py
    REQUIRED_TABLES = REQUIRED_TABLES
    DEFAULT_SCHEMA = DEFAULT_SCHEMA
    
    def __init__(self):
        """Initialize SqlSetupHandler and load environment."""
        load_dotenv()
        self.env_vars_exist = False
        self.dot_env_file_exists = False
        self._check_env_status()
    
    def _check_env_status(self) -> None:
        """
        Check if .env file exists and environment variables are set.
        Sets self.env_vars_exist and self.dot_env_file_exists flags.
        """
        self.dot_env_file_exists = os.path.exists(".env")
        
        DB_HOST = os.getenv("DB_HOST")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        
        self.env_vars_exist = bool(DB_HOST and DB_USER and DB_PASSWORD)
    
    def create_database_and_setup(self, host, user, password, db_name, schema_sql=None, port=3306, charset="utf8mb4"):
        """
        Create database and execute schema SQL statements.
        Delegates to database.py::create_database_and_setup()
        
        Args:
            host: MySQL server hostname/IP
            user: MySQL username
            password: MySQL password
            db_name: Name of database to create
            schema_sql: None, string, or list of SQL statements
            port: MySQL port (default 3306)
            charset: Character set for database (default utf8mb4)
        
        Returns:
            bool: True on success, False on failure
        """
        return create_database_and_setup(host, user, password, db_name, schema_sql, port, charset)
    
    def check_database_schema(self, host, user, password, db_name, port=3306):
        """
        Validate database schema and check for required tables.
        Delegates to validators.py::check_database_schema()
        
        Args:
            host: MySQL server hostname/IP
            user: MySQL username
            password: MySQL password
            db_name: Database name to check
            port: MySQL port (default 3306)
        
        Returns:
            Tuple[bool, list]: (success, missing_tables)
        """
        return check_database_schema(host, user, password, db_name, port)
    
    def prompt_user(self, question):
        """
        Prompt user with a yes/no question.
        Delegates to prompts.py::prompt_user()
        
        Args:
            question: The question to ask the user
        
        Returns:
            str: User's response (lowercase)
        """
        return prompt_user(question)
    
    def get_raw_password(self, prompt="Enter password: "):
        """
        Get password input from user (raw input, not masked).
        Delegates to prompts.py::get_raw_password()
        
        Args:
            prompt: Custom prompt text
        
        Returns:
            str: Password entered by user
        """
        return get_raw_password(prompt)
    
    def create_env_instructions(self, host, user, password, db_name):
        """
        Display .env file creation instructions to user.
        Delegates to prompts.py::create_env_instructions()
        
        Args:
            host: MySQL host
            user: MySQL user
            password: MySQL password
            db_name: Database name
        """
        return create_env_instructions(host, user, password, db_name)
    
    def run_setup_wizard(self):
        """
        Main setup wizard flow.
        Delegates to main.py::run_setup_wizard()
        
        The main orchestration that:
        1. Checks for existing .env and environment variables
        2. Asks user if project is already set up
        3. If not: collects credentials, creates database, validates schema
        4. If yes: verifies existing database schema
        5. Shows .env creation instructions
        
        Exits with status 0 on success or 1 on failure.
        """
        return main_run_setup_wizard()
    
    def setup(self):
        """
        MAIN FUNCTION: Complete database setup orchestration.
        
        This is the primary function that performs all setup tasks:
        1. Checks environment variables and .env file
        2. If env vars exist: validates schema and exits
        3. If not: asks if project is already set up
           - If YES: gets credentials, validates existing DB schema
           - If NO: gets credentials, creates DB + schema, validates
        4. Shows .env creation instructions
        5. Validates complete schema
        
        This function orchestrates:
        - _check_env_status() from __init__
        - prompt_user() from prompts.py
        - get_raw_password() from prompts.py
        - create_database_and_setup() from database.py
        - check_database_schema() from validators.py
        - create_env_instructions() from prompts.py
        
        Returns:
            bool: True on complete success, False on failure
        """
        print("\n" + "=" * 70)
        print("ZYNC DATABASE SETUP WIZARD")
        print("=" * 70)

        # Step 1: Check environment status
        print(f"\n[*] Checking environment...")
        print(f"    .env file exists: {self.dot_env_file_exists}")
        print(f"    Environment variables set: {self.env_vars_exist}")

        # Step 2: If env vars already set, validate and return
        if self.env_vars_exist:
            DB_HOST = os.getenv("DB_HOST")
            DB_USER = os.getenv("DB_USER")
            DB_PASSWORD = os.getenv("DB_PASSWORD")
            DB_NAME = os.getenv("DB_NAME", "zyncdb_users")
            
            print(f"\n[✓] Environment variables are already configured.")
            print(f"    Host: {DB_HOST}")
            print(f"    User: {DB_USER}")
            print(f"    Database: {DB_NAME}")
            
            # Validate schema using check_database_schema()
            success, missing = self.check_database_schema(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
            if success:
                print("\n[✓] All done! Your database is ready to use.")
                return True
            else:
                print("\n[✗] Schema validation failed. Please fix the issues above.")
                return False
        
        # Step 3: Ask user if project is already set up
        print("\n" + "-" * 70)
        response = self.prompt_user("Have you already set up the database project on this system?")
        
        if response.lower() in ["yes", "y"]:
            # User says project is already set up
            print("\n[*] Assuming database already exists...")
            print("\n[!] Please provide your database credentials to verify the setup.\n")
            
            # Get credentials from user
            host = input("Enter DB_HOST (default: 169.254.196.213): ").strip() or "169.254.196.213"
            user = input("Enter DB_USER (default: zync): ").strip() or "zync"
            password = self.get_raw_password("Enter DB_PASSWORD: ")
            db_name = input("Enter DB_NAME (default: zyncdb_users): ").strip() or "zyncdb_users"
            
            # Show .env instructions using create_env_instructions()
            self.create_env_instructions(host, user, password, db_name)
            
            # Validate existing schema using check_database_schema()
            print("[*] Verifying database schema...")
            success, missing = self.check_database_schema(host, user, password, db_name)
            
            if success:
                print("\n[✓] Setup verified! Your database is ready.")
                return True
            else:
                print("\n[✗] Database schema is incomplete or missing.")
                print(f"    Missing tables: {', '.join(missing)}")
                return False
        
        else:
            # User says project needs to be set up
            print("\n[*] Starting fresh project setup...\n")
            
            # Get credentials from user
            print("Please provide your MySQL credentials:\n")
            host = input("Enter DB_HOST (default: localhost): ").strip() or "localhost"
            user = input("Enter DB_USER (default: root): ").strip() or "root"
            password = self.get_raw_password("Enter DB_PASSWORD: ")
            db_name = input("Enter DB_NAME (default: zyncdb_users): ").strip() or "zyncdb_users"
            
            # Create database and schema using create_database_and_setup()
            print("\n[*] Setting up database...")
            success = self.create_database_and_setup(host, user, password, db_name, schema_sql=self.DEFAULT_SCHEMA)
            
            if success:
                print("\n[✓] Database and schema created successfully!\n")
                
                # Show .env instructions using create_env_instructions()
                self.create_env_instructions(host, user, password, db_name)
                
                # Verify the setup using check_database_schema()
                print("[*] Verifying setup...")
                success, missing = self.check_database_schema(host, user, password, db_name)
                
                if success:
                    # Create .env file automatically
                    print("\n[*] Creating .env file...")
                    env_created = create_env_file(host, user, password, db_name)
                    
                    if env_created:
                        print("\n[✓] All done! Your database is ready and .env file has been created.")
                        return True
                    else:
                        print("\n[!] Database is ready but .env file creation failed.")
                        print("    You can create it manually with the credentials shown above.")
                        return False
                else:
                    print("\n[!] Database created but schema verification failed.")
                    print(f"    Missing tables: {', '.join(missing)}")
                    return False
            else:
                print("\n[✗] Failed to set up database. Please check your credentials and try again.")
                return False


# For CLI usage
if __name__ == "__main__":
    handler = SqlSetupHandler()
    success = handler.setup()
    
    print("\n" + "=" * 70)
    if success:
        print("Setup complete! You can now start your Flask app.")
    else:
        print("Setup encountered errors. Please review the messages above.")
    print("=" * 70 + "\n")
    
    sys.exit(0 if success else 1)
