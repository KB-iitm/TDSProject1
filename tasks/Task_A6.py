import json
import re
from pathlib import Path

def generate_md_index(docs_dir: str, output_file: str):
    """Create an index of Markdown files mapping 'parent - filename' to first H1 title."""
    index = {}

    for md_file in Path(docs_dir).rglob("*.md"):
        relative_path = md_file.relative_to(docs_dir)  # Get relative path
        parts = relative_path.parts  # Split path into components
        if len(parts) > 1:
            index_name = f"{parts[-2]} - {md_file.name}"  # Format as 'parent - filename'
        else:
            index_name = md_file.name  # Keep filename if no parent dir

        with open(md_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("# "):
                    index[index_name] = line.strip("# ").strip()
                    break

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)

# Example usage
if __name__ == "__main__":
    generate_md_index(r"C:\Users\kathb\TDS_Project\data\docs",
                  r"C:\Users\kathb\TDS_Project\data\docs\index.json")

