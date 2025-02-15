import sys
import os
import requests
from bs4 import BeautifulSoup

DATA_DIR = "data/"

# Restricted domains to prevent scraping sensitive sites
BLOCKED_DOMAINS = ["bank", "login", "secure", "paypal", "stripe"]

def scrape_website(url, save_as):
    """Scrapes a webpage and extracts visible text content."""
    
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Security: Block scraping sensitive domains
    if any(blocked in url.lower() for blocked in BLOCKED_DOMAINS):
        print("❌ Error: Scraping restricted domains is not allowed.")
        return
    
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ Error: Failed to fetch page (Status: {response.status_code})")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts, styles, and hidden elements
        for element in soup(["script", "style", "noscript"]):
            element.extract()

        extracted_text = soup.get_text(separator="\n", strip=True)

        file_path = os.path.join(DATA_DIR, save_as)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        
        print(f"✅ Data saved to {file_path}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def extract_scrape(task: str):
    """
    For B6: Scrape a website.
    Extracts:
      - URL: First HTTP/HTTPS URL.
      - Output file: Following "save to".
    """
    url_match = re.search(r"(https?://[^\s]+)", task)
    url = url_match.group(0) if url_match else "https://news.ycombinator.com/"
    output_match = re.search(r"save to\s+([^\s]+)", task, re.IGNORECASE)
    output_file = output_match.group(1) if output_match else "hackernews.txt"
    return url, output_file

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python B6_scrape.py <URL> <OUTPUT_FILE>")
        print("Example: python B6_scrape.py 'https://news.ycombinator.com/' 'hackernews.txt'")
    else:
        scrape_website(sys.argv[1], sys.argv[2])
