import os
import sys
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

def load_csv_to_snowflake():
    csv_file_path = "data/my_data.csv" # Or take from env var/arg
    table_name = "MY_NEW_TABLE"
    
    # 1. Read CSV
    try:
        df = pd.read_csv(csv_file_path)
        # Snowflake table names/columns are typically upper case, let's normalize headers
        df.columns = [c.upper() for c in df.columns]
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

    # 2. Connect to Snowflake
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
        
        # 3. Write Pandas DataFrame to Snowflake
        # auto_create_table=True will create the table if it doesn't exist
        success, nchunks, nrows, _ = write_pandas(
            conn, 
            df, 
            table_name=table_name,
            auto_create_table=True,
            quote_identifiers=False # To let Snowflake handle column names as case-insensitive usually
        )
        print(f"Successfully loaded {nrows} rows into {table_name}.")
        
    except Exception as err:
        print(f"Snowflake connection or load error: {err}", file=sys.stderr)
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    load_csv_to_snowflake()
