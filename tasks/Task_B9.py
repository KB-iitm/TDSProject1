import sys
import os
import re
import markdown

DATA_DIR = "data/"

def convert_md_to_html(md_filename, html_filename):
    md_path = os.path.join(DATA_DIR, md_filename)
    html_path = os.path.join(DATA_DIR, html_filename)
    
    if not os.path.exists(md_path):
        print(f"Error: {md_path} does not exist.")
        return
    
    with open(md_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()
        html_content = markdown.markdown(md_content)
    
    with open(html_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)
    
    print(f"Conversion successful! HTML saved to {html_path}")

def extract_md_to_html(task: str):
    """
    For B9: Convert Markdown to HTML.
    Extracts:
      - Input file: Look for "markdown" followed by a filename.
      - Output file: Following "save to".
    """
    input_match = re.search(r"markdown\s+([^\s]+)", task, re.IGNORECASE)
    input_file = input_match.group(1) if input_match else "format.md"
    output_match = re.search(r"save to\s+([^\s]+)", task, re.IGNORECASE)
    output_file = output_match.group(1) if output_match else "md_to_html.html"
    return input_file, output_file

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python Task_B9.py <input_markdown.md> <output_html.html>")
    else:
        convert_md_to_html(sys.argv[1], sys.argv[2])
