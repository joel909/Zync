# modules/sql_manager/SqlSetupHandler/validators.py
"""
Database schema validation.
Checks if database exists and contains required tables.
"""

import mysql.connector
from mysql.connector import Error
from typing import Tuple
from .schema import REQUIRED_TABLES


def check_database_schema(
    host: str,
    user: str,
    password: str,
    db_name: str,
    port: int = 3306
) -> Tuple[bool, list]:
    """
    Validate database schema and check for required tables.
    
    This function:
    1. Connects to the specified database
    2. Retrieves list of existing tables
    3. Compares against REQUIRED_TABLES
    4. Reports missing tables if any
    
    Supports MySQL 8.0+ with caching_sha2_password authentication.
    
    Args:
        host: MySQL server hostname/IP
        user: MySQL username
        password: MySQL password (raw password)
        db_name: Database name to check
        port: MySQL port (default 3306)
    
    Returns:
        Tuple[bool, list]: (success: True if all tables exist, missing_tables: list of missing table names)
    """
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port,
            auth_plugin='mysql_native_password'  # Supports raw passwords
        )
        cursor = conn.cursor()

        # Get list of existing tables
        cursor.execute("SHOW TABLES;")
        existing_tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        conn.close()

        # Check for required tables
        missing_tables = [t for t in REQUIRED_TABLES if t not in existing_tables]

        if not missing_tables:
            print(f"\n[✓] Database schema check passed!")
            print(f"    Found all required tables: {', '.join(REQUIRED_TABLES)}")
            return True, []
        else:
            print(f"\n[✗] Database schema check failed!")
            print(f"    Missing tables: {', '.join(missing_tables)}")
            return False, missing_tables

    except Error as e:
        print(f"\n[✗] Could not connect to database: {e}")
        return False, REQUIRED_TABLES
