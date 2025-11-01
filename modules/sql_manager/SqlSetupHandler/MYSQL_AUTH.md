# MySQL Authentication: Raw Password Support

## Problem
Error: `Authentication plugin 'caching_sha2_password' is not supported`

This occurs with MySQL 8.0+ which uses the `caching_sha2_password` authentication plugin by default, which requires SSL or special handling.

## Solution
We use `auth_plugin='mysql_native_password'` which supports raw passwords without SSL.

## MySQL Version Support

### Raw Password Support by Version
- **MySQL 5.7 and earlier**: ✅ Supports raw passwords natively
- **MySQL 8.0+**: ⚠️ Uses `caching_sha2_password` by default (requires SSL or plugin override)

### Our Fix
We added `auth_plugin='mysql_native_password'` to connection parameters:

```python
mysql.connector.connect(
    host=host,
    user=user,
    password=password,  # Raw password
    auth_plugin='mysql_native_password'  # ✅ Supports raw passwords
)
```

## How to Enter Raw Password

When the setup wizard asks: **"Enter DB_PASSWORD:"**

Just type your password **as plain text** (no special characters needed):

```
Enter DB_PASSWORD: my_password_123
```

The system will:
1. Take your raw password as-is
2. Use `mysql_native_password` plugin for authentication
3. Connect securely to MySQL

## Files Updated

1. **database.py**: `create_database_and_setup()` now uses `auth_plugin='mysql_native_password'`
2. **validators.py**: `check_database_schema()` now uses `auth_plugin='mysql_native_password'`

## Testing Connection

Try running the setup again:

```powershell
python app.py
```

When prompted:
```
Enter DB_HOST (default: 169.254.196.213): 169.254.196.213
Enter DB_USER (default: zync): zync
Enter DB_PASSWORD: 123
Enter DB_NAME (default: zyncdb_users): zyncdb_users
```

Just enter your raw password directly - no quotes or encoding needed!

## Alternative: Change MySQL User Authentication

If you want to permanently use raw passwords on MySQL 8.0+, you can change the authentication method:

```sql
-- Connect as root
mysql -u root -p

-- Change user authentication plugin
ALTER USER 'zync'@'%' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
```

Then the default connection will work without specifying the plugin.

## Troubleshooting

If you still get authentication errors:

1. **Verify credentials**: Make sure host, user, password are correct
2. **Check MySQL server**: Ensure MySQL is running and accessible
3. **Check user permissions**: Verify the user has CREATE DATABASE privilege
4. **Try connecting manually**:
   ```powershell
   mysql -h 169.254.196.213 -u zync -p123
   ```

## References

- MySQL Connector/Python: `auth_plugin` parameter
- MySQL 8.0 Authentication Methods: https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-tutorial-python-connection.html
