import sys
import os
from PIL import Image

DATA_DIR = "data/"

def process_image(input_file, output_file, width=None, height=None, quality=85):
    """Resize and/or compress an image and save it."""
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    input_path = os.path.join(DATA_DIR, input_file)
    output_path = os.path.join(DATA_DIR, output_file)

    if not os.path.exists(input_path):
        print(f"❌ Error: File {input_file} not found in /data/")
        return
    
    try:
        with Image.open(input_path) as img:
            # Resize if width/height provided
            if width or height:
                width = width or img.width
                height = height or img.height
                img = img.resize((width, height), Image.LANCZOS)
            
            # Save compressed version (JPEG for best compression)
            img.save(output_path, quality=quality, optimize=True)
        
        print(f"✅ Image processed and saved to {output_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

def extract_image_params(task: str):
    """
    For B7: Process an image (compress/resize).
    Extracts:
      - Input file: Look for "image" followed by a filename.
      - Output file: Following "save to".
      - Width, height, quality: Look for these words followed by numbers.
    """
    input_match = re.search(r"image\s+([^\s]+)", task, re.IGNORECASE)
    input_file = input_match.group(1) if input_match else "credit_card.png"
    output_match = re.search(r"save to\s+([^\s]+)", task, re.IGNORECASE)
    output_file = output_match.group(1) if output_match else "output.jpg"
    width_match = re.search(r"width\s+(\d+)", task, re.IGNORECASE)
    width = int(width_match.group(1)) if width_match else 800
    height_match = re.search(r"height\s+(\d+)", task, re.IGNORECASE)
    height = int(height_match.group(1)) if height_match else 600
    quality_match = re.search(r"quality\s+(\d+)", task, re.IGNORECASE)
    quality = int(quality_match.group(1)) if quality_match else 80
    return input_file, output_file, width, height, quality

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python B7_image.py <input_image> <output_image> [width] [height] [quality]")
        print("Example: python B7_image.py 'input.jpg' 'output.jpg' 800 600 80")
    else:
        width = int(sys.argv[3]) if len(sys.argv) > 3 else None
        height = int(sys.argv[4]) if len(sys.argv) > 4 else None
        quality = int(sys.argv[5]) if len(sys.argv) > 5 else 85
        process_image(sys.argv[1], sys.argv[2], width, height, quality)
