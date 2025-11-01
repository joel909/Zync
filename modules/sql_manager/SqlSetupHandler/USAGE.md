# SqlSetupHandler Usage Examples

## Quick Start

### Option 1: Run the Setup Wizard (Interactive)

```python
from modules.sql_manager.SqlSetupHandler import SqlSetupHandler

handler = SqlSetupHandler()
handler.run_setup_wizard()
```

Or from command line:
```powershell
python -m modules.sql_manager.SqlSetupHandler
```

### Option 2: Create Database Programmatically

```python
from modules.sql_manager.SqlSetupHandler import SqlSetupHandler

handler = SqlSetupHandler()

# Create database and setup schema
success = handler.create_database_and_setup(
    host="localhost",
    user="root",
    password="your_password",
    db_name="zyncdb_users",
    schema_sql=handler.DEFAULT_SCHEMA
)

if success:
    print("Database created successfully!")
else:
    print("Failed to create database")
```

### Option 3: Validate Database Schema

```python
from modules.sql_manager.SqlSetupHandler import SqlSetupHandler

handler = SqlSetupHandler()

# Check if database schema is valid
is_valid, missing_tables = handler.check_database_schema(
    host="localhost",
    user="root",
    password="your_password",
    db_name="zyncdb_users"
)

if is_valid:
    print("Database schema is valid!")
else:
    print(f"Missing tables: {missing_tables}")
```

### Option 4: Use in Flask Startup

```python
from flask import Flask
from modules.sql_manager.SqlSetupHandler import SqlSetupHandler
import os

app = Flask(__name__)

# Check database on startup
@app.before_request
def check_database():
    handler = SqlSetupHandler()
    is_valid, missing = handler.check_database_schema(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db_name=os.getenv("DB_NAME", "zyncdb_users")
    )
    
    if not is_valid:
        raise Exception(f"Database schema incomplete: missing {missing}")

if __name__ == "__main__":
    app.run()
```

## Class Methods

### `__init__()`
Initializes the handler and checks environment status.

### `run_setup_wizard()`
Main interactive setup wizard. Handles:
- Checking for existing .env and env vars
- Asking if project is already set up
- Creating database if needed
- Validating schema
- Showing .env instructions

### `create_database_and_setup(host, user, password, db_name, schema_sql=None, port=3306, charset="utf8mb4")`
Creates database and executes schema SQL statements.

**Returns:** `bool` (True on success, False on failure)

### `check_database_schema(host, user, password, db_name, port=3306)`
Validates database schema and checks for required tables.

**Returns:** `Tuple[bool, List[str]]` (success, list of missing tables)

### `prompt_user(question)`
Prompts user with yes/no question.

**Returns:** `str` (lowercase response)

### `get_raw_password(prompt="Enter password: ")`
Gets password input from user.

**Returns:** `str` (password)

### `create_env_instructions(host, user, password, db_name)`
Displays .env file creation instructions.

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    auth_key VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Events Table
```sql
CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    core_event VARCHAR(255) NOT NULL,
    event_name VARCHAR(255) NOT NULL,
    description TEXT,
    ev_date DATETIME,
    venue VARCHAR(255),
    created_by_auth_key VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Registrations Table
```sql
CREATE TABLE registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    school VARCHAR(255),
    DOB DATE,
    grade VARCHAR(50),
    contact_details VARCHAR(255),
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
