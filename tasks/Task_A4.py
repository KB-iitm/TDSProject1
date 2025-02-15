import json
import re

def sort_contacts(input_file: str, output_file: str, sort_keys=None):
    """
    Sort contacts by specified keys.
    
    Parameters:
      - input_file: Path to the JSON file containing contacts.
      - output_file: Path to the JSON file where sorted contacts will be written.
      - sort_keys: List of keys to sort by. Defaults to ["last_name", "first_name"] if not provided.
    """
    if sort_keys is None:
        sort_keys = ["last_name", "first_name"]
    
    with open(input_file, "r", encoding="utf-8") as f:
        contacts = json.load(f)

    # Sort by the provided keys in order.
    contacts.sort(key=lambda x: tuple(x[k] for k in sort_keys))

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4)

def extract_sort_keys(task: str):
    """
    Extract sort keys from the task description.
    Looks for phrases like "by email", "by first name", "by last name", etc.
    Returns a list of keys to sort by.
    """
    task_lower = task.lower()
    sort_keys = []

    # Look for phrases following the word "by"
    # e.g., "sort contacts by email", "sort contacts by first name and last name", etc.
    pattern = r"by\s+([a-z\s,]+)"
    match = re.search(pattern, task_lower)
    if match:
        keys_str = match.group(1)
        # Split by comma or "and" to allow multiple sort keys
        # Remove extra spaces and filter out empty strings.
        possible_keys = re.split(r",|and", keys_str)
        for key in possible_keys:
            key = key.strip()
            if "email" in key:
                sort_keys.append("email")
            if "first" in key:
                sort_keys.append("first_name")
            if "last" in key:
                sort_keys.append("last_name")
    
    # If no keys were found, use the default order.
    if not sort_keys:
        sort_keys = ["last_name", "first_name"]
    
    return sort_keys

# Example usage:
if __name__ == "__main__":
    # Default sort (by last name then first name)
    sort_contacts(r"C:\Users\kathb\TDS_Project\data\contacts.json",
                  r"C:\Users\kathb\TDS_Project\data\contacts_sorted.json")

    # Custom sort, for example by email only:
    sort_contacts(r"C:\Users\kathb\TDS_Project\data\contacts.json",
                  r"C:\Users\kathb\TDS_Project\data\contacts_sorted_by_email.json",
                  sort_keys=["email"])
