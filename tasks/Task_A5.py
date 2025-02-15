import os
from pathlib import Path

def extract_recent_logs(logs_dir: str, output_file: str):
    """Write the first line of the 10 most recent .log files to a new file."""
    log_files = list(Path(logs_dir).glob("*.log"))
    log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)  # Sort by modified time

    with open(output_file, "w", encoding="utf-8") as out:
        for log_file in log_files[:10]:  # Get top 10 logs
            with open(log_file, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                out.write(first_line + "\n")

# Example usage
if __name__ == "__main__":
    extract_recent_logs(r"C:\Users\kathb\TDS_Project\data\logs",
                    r"C:\Users\kathb\TDS_Project\data\logs-recent.txt")