import sqlite3
import os

def init_db():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the database file
    db_path = os.path.join(current_dir, "villa.db")
    
    # Path to the schema file
    schema_path = os.path.join(current_dir, "schema.sql")
    
    # Read the schema file
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    # Connect to the database and create tables
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.executescript(schema)
        conn.commit()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!") 