# tasks/Task_B10.py
import pandas as pd
import os
import re
import json

DATA_DIR = "data/"

def filter_csv(file_name: str, column: str, value: str):
    file_path = os.path.join(DATA_DIR, file_name)
    print(file_path)
    print(column)
    print(value)
    
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    try:
        df = pd.read_csv(file_path)
        
        if column not in df.columns:
            return {"error": "Column not found"}
        
        filtered_df = df[df[column].astype(str) == value]
        result = filtered_df.to_dict(orient="records")
        
        # Write the result to a text file
        output_file = os.path.join(DATA_DIR, "filtered_output.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(result, indent=4))
        
        return result
    
    except Exception as e:
        return {"error": str(e)}

def extract_filter_csv(task: str):
    """
    For B10: Filter CSV file.
    Extracts:
      - CSV file: Look for "csv" followed by a filename.
      - Column: Look for "filter by" followed by a word.
      - Value: Look for "equals" or "equal" followed by a word.
    """
    csv_match = re.search(r"csv\s+([^\s]+)", task, re.IGNORECASE)
    csv_file = csv_match.group(1) if csv_match else "E2.csv"
    col_match = re.search(r"filter by\s+([^\s]+)", task, re.IGNORECASE)
    column = col_match.group(1) if col_match else "HomeTeam"
    val_match = re.search(r"equal[s]?\s+([^\s]+)", task, re.IGNORECASE)
    value = val_match.group(1) if val_match else "Burnley"
    print(csv_file,column, value)
    return csv_file, column, value
