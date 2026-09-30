import os
import sys
import snowflake.connector

def run_query():
    try:
        conn = snowflake.connector.connect(
            user=os.environ["SNOWFLAKE_USER"],
            password=os.environ["SNOWFLAKE_PASSWORD"],
            account=os.environ["SNOWFLAKE_ACCOUNT"],
            warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
            database=os.environ.get("SNOWFLAKE_DATABASE"),
            schema=os.environ.get("SNOWFLAKE_SCHEMA"),
            role=os.environ.get("SNOWFLAKE_ROLE")
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_VERSION(), CURRENT_USER(), CURRENT_ROLE();")
        version, user, role = cursor.fetchone()
        
        print(" Connected to Snowflake successfully!")
        print(f"Snowflake Version: {version}")
        print(f"Authenticated User: {user}")
        print(f"Active Role:        {role}")
        
    except Exception as err:
        print(f" Failed to connect or execute query: {err}", file=sys.stderr)
        sys.exit(1)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    run_query()
