# modules/sql_manager/SqlSetupHandler/database.py
"""
Database setup and operations.
Handles creating database, executing schema, and validating connections.
"""

import mysql.connector
from mysql.connector import Error
from typing import Iterable, Union


def create_database_and_setup(
    host: str,
    user: str,
    password: str,
    db_name: str,
    schema_sql: Union[None, str, Iterable[str]] = None,
    port: int = 3306,
    charset: str = "utf8mb4",
) -> bool:
    """
    Create database and execute schema SQL statements.
    
    This function:
    1. Connects to MySQL server
    2. Creates the database if it doesn't exist
    3. Executes all provided SQL schema statements
    4. Commits and closes connections
    
    Supports MySQL 8.0+ with caching_sha2_password authentication.
    
    Args:
        host: MySQL server hostname/IP
        user: MySQL username
        password: MySQL password (raw password, no special encoding needed)
        db_name: Name of database to create
        schema_sql: None, string, or list of SQL statements
        port: MySQL port (default 3306)
        charset: Character set for database (default utf8mb4)
    
    Returns:
        bool: True on success, False on failure
    """
    # Normalize schema_sql into a list of statements
    if schema_sql is None:
        schema_statements = []
    elif isinstance(schema_sql, str):
        schema_statements = [schema_sql]
    else:
        schema_statements = list(schema_sql)

    try:
        # 1) Connect to the server (no database specified)
        # Use auth_plugin parameter to handle MySQL 8.0+ caching_sha2_password
        print(f"\n[*] Connecting to MySQL server at {host}:{port}...")
        admin_conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            autocommit=True,
            auth_plugin='mysql_native_password'  # Supports raw passwords
        )
        admin_cursor = admin_conn.cursor()
        
        # Create database
        create_db_stmt = f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET '{charset}'"
        print(f"[*] Creating database '{db_name}'...")
        admin_cursor.execute(create_db_stmt)
        admin_cursor.close()
        admin_conn.close()
        print(f"[✓] Database '{db_name}' created/exists.")

        # 2) Connect to the database and execute schema statements
        print(f"[*] Connecting to database '{db_name}'...")
        db_conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port,
            auth_plugin='mysql_native_password'  # Supports raw passwords
        )
        db_cursor = db_conn.cursor()

        print(f"[*] Creating tables...")
        for stmt in schema_statements:
            # Skip empty statements
            if not str(stmt).strip():
                continue
            db_cursor.execute(stmt)

        db_conn.commit()
        db_cursor.close()
        db_conn.close()
        print(f"[✓] Schema created/updated successfully.")
        return True

    except Error as e:
        print(f"[✗] Database setup failed: {e}")
        return False
