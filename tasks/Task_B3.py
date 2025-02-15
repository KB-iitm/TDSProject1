import sys
import requests
import os

DATA_DIR = "data/"

def fetch_api_data(api_url, save_as):
    """Fetch data from an API and save it inside /data/."""
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    file_path = os.path.join(DATA_DIR, os.path.basename(save_as))  # Ensures saving only inside /data/
    
    response = requests.get(api_url)
    if response.status_code == 200:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Data saved to {file_path}")
    else:
        print(f"❌ Failed to fetch data: {response.status_code}")

def extract_api_data(task: str):
    """
    For B3: Fetch API data.
    Extracts:
      - URL: The first occurrence of an HTTP/HTTPS URL.
      - Output file: Following a phrase like "save to" (e.g., "save to example_data.txt").
    """
    url_match = re.search(r"(https?://[^\s]+)", task)
    url = url_match.group(0) if url_match else "https://en.wikipedia.org/wiki/Koala"
    output_match = re.search(r"save to\s+([^\s]+)", task, re.IGNORECASE)
    output_file = output_match.group(1) if output_match else "api_data.txt"
    return url, output_file

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python B3_fetch_api.py <API_URL> <FILENAME>")
        print("Example: python B3_fetch_api.py 'https://jsonplaceholder.typicode.com/posts' 'api_data.txt'")
    else:
        fetch_api_data(sys.argv[1], sys.argv[2])
