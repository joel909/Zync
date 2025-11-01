# modules/sql_manager/SqlSetupHandler/schema.py
"""
Database schema definition for Zync project.
Contains all SQL CREATE TABLE statements (idempotent).
"""

# Required tables list for validation
REQUIRED_TABLES = ["users", "events", "registrations"]

# Default database schema with all table definitions
DEFAULT_SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        auth_key VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        core_event VARCHAR(255) NOT NULL,
        event_name VARCHAR(255) NOT NULL,
        description TEXT,
        ev_date DATETIME,
        venue VARCHAR(255),
        created_by_auth_key VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS registrations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        event_id INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        school VARCHAR(255),
        DOB DATE,
        grade VARCHAR(50),
        contact_details VARCHAR(255),
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
]
