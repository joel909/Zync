# SqlSetupHandler - Modular Database Setup

## Overview
The `SqlSetupHandler` package provides a clean, modular approach to database setup and validation for the Zync project. Each file handles a single responsibility.

## File Structure

```
SqlSetupHandler/
├── __init__.py          # Package initialization & exports
├── schema.py            # Database schema definitions
├── database.py          # Database creation & operations
├── validators.py        # Database validation & schema checks
├── prompts.py           # User input & instructions
└── main.py              # Setup wizard orchestration
```

## Files & Functions

### 1. schema.py
**Purpose:** Define database schema and required tables

**Exports:**
- `REQUIRED_TABLES`: List of table names that must exist
- `DEFAULT_SCHEMA`: List of SQL CREATE TABLE statements (idempotent)

**Tables defined:**
- `users`: id, email, password, auth_key, created_at
- `events`: id, core_event, event_name, description, ev_date, venue, created_by_auth_key, created_at
- `registrations`: id, event_id, name, school, DOB, grade, contact_details, registered_at

### 2. database.py
**Purpose:** Handle database creation and schema execution

**Function:**
- `create_database_and_setup()`: Creates DB and runs schema SQL statements
  - Input: host, user, password, db_name, schema_sql, port, charset
  - Output: bool (True on success)
  - Connects as admin, creates DB, applies schema, validates

### 3. validators.py
**Purpose:** Validate database state and schema

**Function:**
- `check_database_schema()`: Validates database and checks required tables exist
  - Input: host, user, password, db_name, port
  - Output: Tuple[bool, list] (success, missing_tables)
  - Connects to DB, lists tables, compares against REQUIRED_TABLES

### 4. prompts.py
**Purpose:** Handle user input and display instructions

**Functions:**
- `prompt_user()`: Ask yes/no question, return response
  - Input: question (string)
  - Output: str (lowercase response)

- `get_raw_password()`: Get password input (not masked)
  - Input: prompt (string)
  - Output: str (password)

- `create_env_instructions()`: Display .env creation steps
  - Input: host, user, password, db_name
  - Output: None (prints to console)

### 5. main.py
**Purpose:** Orchestrate the complete setup flow

**Function:**
- `run_setup_wizard()`: Main orchestrator
  - Checks for existing .env and env vars
  - Asks if project is already set up
  - If not: collects credentials, creates DB, validates
  - If yes: verifies existing DB
  - Shows .env instructions
  - Exits with status 0 (success) or 1 (failure)

## Usage

### Option 1: Run the Setup Wizard (Interactive)
```python
from modules.sql_manager.SqlSetupHandler import run_setup_wizard

run_setup_wizard()
```

Or from command line:
```powershell
python -m modules.sql_manager.SqlSetupHandler.main
```

### Option 2: Use Individual Functions Programmatically
```python
from modules.sql_manager.SqlSetupHandler import (
    create_database_and_setup,
    check_database_schema,
    DEFAULT_SCHEMA
)

# Create DB
success = create_database_and_setup(
    host="localhost",
    user="root",
    password="pass",
    db_name="zyncdb_users",
    schema_sql=DEFAULT_SCHEMA
)

# Validate
if success:
    is_valid, missing = check_database_schema(
        host="localhost",
        user="root",
        password="pass",
        db_name="zyncdb_users"
    )
```

### Option 3: Import All in Flask App
```python
from modules.sql_manager.SqlSetupHandler import (
    run_setup_wizard,
    check_database_schema,
    create_database_and_setup,
    REQUIRED_TABLES,
    DEFAULT_SCHEMA
)

# Check on startup
valid, missing = check_database_schema(host, user, pwd, db)
if not valid:
    print(f"Missing tables: {missing}")
    # Handle error or run setup
```

## Comments & Documentation

Each file includes:
- Module docstring explaining purpose
- Function docstrings with:
  - Purpose/what it does
  - Args documentation
  - Returns documentation
  - Step-by-step process documentation (for complex functions)

## Next Steps

To use this in your Flask app startup:
1. Run `run_setup_wizard()` once to initialize DB
2. On subsequent startups, `check_database_schema()` to verify
3. Load DB credentials from `.env` file

Example Flask startup:
```python
from flask import Flask
from modules.sql_manager.SqlSetupHandler import check_database_schema
import os

app = Flask(__name__)

# On startup
@app.before_first_request
def check_db():
    valid, missing = check_database_schema(
        os.getenv("DB_HOST"),
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_NAME")
    )
    if not valid:
        raise Exception(f"Database schema incomplete: missing {missing}")
```
