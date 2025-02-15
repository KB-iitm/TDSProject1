import subprocess

def format_with_prettier(file_path: str, version: str = "3.4.2"):
    """Format a file using Prettier with the specified version."""
    try:
        subprocess.run([f"npx", f"prettier@{version}", "--write", file_path], check=True, shell=True)
        print(f"Formatted {file_path} using Prettier {version}.")
    except subprocess.CalledProcessError as e:
        print(f"Error formatting file: {e}")

# Example usage
if __name__ == "__main__":
    format_with_prettier(r"C:\Users\kathb\TDS_Project\data\format.md")