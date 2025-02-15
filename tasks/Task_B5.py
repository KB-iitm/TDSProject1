import sys
import os
import sqlite3
import duckdb
import pandas as pd

DATA_DIR = "data/"

def run_sql_query(db_name, query):
    """Executes an SQL query on SQLite or DuckDB and returns the result."""
    
    db_path = os.path.join(DATA_DIR, db_name)

    # Ensure the database exists inside /data/ (B1 security rule)
    if not db_path.startswith(DATA_DIR) or not os.path.exists(db_path):
        print(f"❌ Error: Database {db_name} does not exist in {DATA_DIR}")
        return

    # Restrict DELETE, DROP, and other destructive queries (B2 security rule)
    restricted_keywords = ["DELETE", "DROP", "ALTER", "TRUNCATE"]
    if any(kw in query.upper() for kw in restricted_keywords):
        print("❌ Error: Destructive queries (DELETE, DROP, etc.) are not allowed.")
        return

    try:
        if db_name.endswith((".sqlite", ".db")):
            print("🔹 Using SQLite")
            conn = sqlite3.connect(db_path)
        elif db_name.endswith(".duckdb"):
            print("🔹 Using DuckDB")
            conn = duckdb.connect(db_path)
        else:
            print("❌ Unsupported database format.")
            return
        
        df = pd.read_sql_query(query, conn)  # Fetch results as DataFrame
        conn.close()
        
        # Convert to JSON
        result_json = df.to_json(orient="records", indent=2)
        print(result_json)
    
    except Exception as e:
        print(f"❌ Error executing query: {e}")

def extract_sql_query(task: str):
    """
    For B5: Run a SQL query.
    Extracts:
      - Database file: Look for "database" or "db" followed by a word.
      - Query: Look for "query:" and take the rest of the line.
    """
    db_match = re.search(r"(?:database|db)\s+([^\s]+)", task, re.IGNORECASE)
    db_file = db_match.group(1) if db_match else "ticket-sales.db"
    query_match = re.search(r"query\s*:\s*(.*)", task, re.IGNORECASE)
    query = query_match.group(1).strip() if query_match else "SELECT * FROM tickets LIMIT 5"
    return db_file, query

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python B5_run_sql.py <DATABASE_FILE> '<SQL_QUERY>'")
        print("Example: python B5_run_sql.py my_database.sqlite 'SELECT * FROM users LIMIT 5'")
    else:
        run_sql_query(sys.argv[1], sys.argv[2])
