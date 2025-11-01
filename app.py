import os
from modules.sql_manager.SqlSetupHandler import SqlSetupHandler

# Flag to track if setup has already been done
_SETUP_COMPLETE = False

# Only run setup when this script is executed directly (not when imported)
# Also skip setup on Flask reloads (check WERKZEUG_RUN_MAIN environment variable)
if __name__ == '__main__':
    # WERKZEUG_RUN_MAIN is set by Flask when reloading, so we skip setup on reloads
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        # Step 1: Run database setup first (only once on initial run)
        print("\n" + "=" * 70)
        print("INITIALIZING DATABASE SETUP")
        print("=" * 70)

        db_handler = SqlSetupHandler()
        db_setup_success = db_handler.setup()

        if not db_setup_success:
            print("\n[✗] Database setup failed. Cannot start Flask app.")
            print("    Please fix the errors above and try again.")
            exit(1)
            

        print("\n[✓] Database setup successful!")

        # Step 2: Import Flask app AFTER database setup (NOW it's safe)
        print("\n" + "=" * 70)
        print("STARTING FLASK APPLICATION")
        print("=" * 70 + "\n")

    from flask_app_setup import create_app

    app = create_app()

    # Step 3: Run the Flask app
    app.run(debug=True, host="0.0.0.0", port=80)
