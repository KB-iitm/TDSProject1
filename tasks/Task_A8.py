import pytesseract
from PIL import Image
import re

# Set the Tesseract path explicitly
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_credit_card_number(input_image: str, output_file: str, task_description: str):
    """
    Extract credit card information from an image based on the task description.
    
    Standard behavior: Extract only the credit card number.
    
    If the task description asks for "all the credit card info" or "everything", 
    return all extracted OCR text.
    
    If the task description asks for the "name", then attempt to extract the name 
    from the image text (assuming a pattern like 'Name: John Doe').
    """
    # Perform OCR on the image
    image = Image.open(input_image)
    extracted_text = pytesseract.image_to_string(image)
    print("Full OCR Text:\n", extracted_text)
    
    # Determine mode based on task description
    task_lower = task_description.lower()
    if "all" in task_lower or "everything" in task_lower or "credit card info" in task_lower:
        # Return all extracted text
        result = extracted_text.strip()
    elif "name" in task_lower:
        # Split the text into lines and strip whitespace
        lines = [line.strip() for line in extracted_text.splitlines() if line.strip()]
        # Heuristic: choose the last line if it contains alphabetic characters and is mostly uppercase.
        possible_names = [line for line in lines if re.fullmatch(r"[A-Z\s]+", line)]
        if possible_names:
            result = possible_names[-1]
        else:
            result = "Name not found"
    else:
        # Default: Extract credit card number
        patterns = [
            r"\b\d{4} \d{4} \d{4} \d{4}\b",  # XXXX XXXX XXXX XXXX
            r"\b\d{8} \d{4} \d{4}\b",        # XXXXXXXX XXXX XXXX
            r"\b\d{4} \d{8} \d{4}\b",        # XXXX XXXXXXXX XXXX
            r"\b\d{4} \d{4} \d{8}\b",        # XXXX XXXX XXXXXXXX
            r"\b\d{16}\b",                  # XXXXXXXXXXXXXXXX
            r"\b\d{4} \d{12}\b",            # XXXX XXXXXXXXXXXX
            r"\b\d{12} \d{4}\b"             # XXXXXXXXXXXX XXXX
        ]
        card_number = None
        for pattern in patterns:
            match = re.search(pattern, extracted_text)
            if match:
                card_number = match.group().replace(" ", "")  # Remove spaces
                break
        result = card_number if card_number else "Credit card number not found"

    # Save the result
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)
    
    print(f"Extracted result saved to {output_file}: {result}")

# Example usage:
if __name__ == "__main__":
    # Standard behavior: Extract credit card number
    extract_credit_card_number(
        input_image=r"C:\Users\kathb\TDS_Project\data\credit_card.png",
        output_file=r"C:\Users\kathb\TDS_Project\data\credit_card.txt",
        task_description="extract credit card number"
    )
    
    # Dynamic behavior: Extract all credit card info
    extract_credit_card_number(
        input_image=r"C:\Users\kathb\TDS_Project\data\credit_card.png",
        output_file=r"C:\Users\kathb\TDS_Project\data\credit_card_all.txt",
        task_description="give me all the credit card info"
    )
    
    # Dynamic behavior: Extract the name from the credit card (if present)
    extract_credit_card_number(
        input_image=r"C:\Users\kathb\TDS_Project\data\credit_card.png",
        output_file=r"C:\Users\kathb\TDS_Project\data\credit_card_name.txt",
        task_description="extract the credit card name"
    )
