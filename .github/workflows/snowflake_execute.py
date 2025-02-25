import snowflake.connector
import os
import sys

def execute_sql_file(cursor, file_path):
    with open(file_path, 'r') as file:
        sql_script = file.read()
        cursor.execute(sql_script)
        print(f"Executed: {file_path}")

def main(branch):
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=os.environ['SNOWFLAKE_USER'],
        password=os.environ['SNOWFLAKE_PASSWORD'],
        account=os.environ['SNOWFLAKE_ACCOUNT'],
        database=os.environ['SNOWFLAKE_DATABASE'],
        warehouse=os.environ['SNOWFLAKE_WAREHOUSE'],
        role=os.environ['SNOWFLAKE_ROLE']
    )
    cursor = conn.cursor()

    # Branch-based deployment
    try:
        if branch == "dev":
            execute_sql_file(cursor, "models/latest_2_year_listings.sql")
            execute_sql_file(cursor, "models/older_than_2_year_listings.sql")
        elif branch == "release":
            execute_sql_file(cursor, "models/latest_2_year_listings.sql")
            execute_sql_file(cursor, "models/older_than_2_year_listings.sql")
        elif branch == "prod":
            execute_sql_file(cursor, "models/latest_2_year_listings_table.sql")
            execute_sql_file(cursor, "models/older_than_2_year_listings_table.sql")

        print("All SQL scripts executed successfully!")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    branch = sys.argv[1]
    main(branch)
