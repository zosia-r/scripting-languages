import sqlite3
import sys
import os

def create_database(db_name, schema_file):
    if not os.path.exists(schema_file):
        print(f"Error: Schema file '{schema_file}' does not exist.")
        return

    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    connection = sqlite3.connect(f"{db_name}.sqlite3")
    cursor = connection.cursor()

    try:
        cursor.executescript(schema_sql)
        connection.commit()
        print(f"Data base '{db_name}.sqlite3' has been successfully created using schema file '{schema_file}'.")
    except sqlite3.Error as e:
        print(f"Sqlite error: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_database.py <db_name> <sql_schema_file>")
    else:
        db_name = sys.argv[1]
        schema_file = sys.argv[2]
        create_database(db_name, schema_file)
