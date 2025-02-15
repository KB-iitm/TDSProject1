import sqlite3

def calculate_gold_ticket_sales(db_path: str, output_file: str, ticket_type: str = "Gold"):
    """
    Calculate total sales for a specified ticket type (default is "Gold")
    and save the result to a file.
    
    Parameters:
    - db_path: Path to the SQLite database.
    - output_file: Path to the output file.
    - ticket_type: Ticket type to filter by (e.g., "Gold", "Silver", "Bronze").
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query total sales for the specified ticket type using parameterized SQL.
    cursor.execute("""
        SELECT SUM(units * price) FROM tickets WHERE type = ?;
    """, (ticket_type,))
    
    total_sales = cursor.fetchone()[0] or 0  # Handle NULL case
    
    # Close the connection
    conn.close()
    
    # Write the result to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(total_sales))

    print(f"Total sales for '{ticket_type}' tickets saved to {output_file}")

# Example usage:
if __name__ == "__main__":
    # Standard: Gold tickets
    calculate_gold_ticket_sales("data/ticket-sales.db", "data/ticket-sales-gold.txt")
    
    # Dynamic: Silver tickets
    calculate_gold_ticket_sales("data/ticket-sales.db", "data/ticket-sales-silver.txt", ticket_type="Silver")
    
    # Dynamic: Bronze tickets
    calculate_gold_ticket_sales("data/ticket-sales.db", "data/ticket-sales-bronze.txt", ticket_type="Bronze")
