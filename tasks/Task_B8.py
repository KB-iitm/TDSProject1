import sys
import os
import re
import whisper

DATA_DIR = "data/"

def transcribe_audio(mp3_path, output_txt):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    model = whisper.load_model("base")  # Use 'tiny' for faster results
    result = model.transcribe(mp3_path)

    output_path = os.path.join(DATA_DIR, output_txt)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"Transcription saved to {output_path}")

def extract_audio_params(task: str):
    """
    For B8: Transcribe audio.
    Extracts:
      - Input file: Look for "audio" followed by a filename.
      - Output file: Following "save to".
    """
    input_match = re.search(r"audio\s+([^\s]+)", task, re.IGNORECASE)
    input_file = input_match.group(1) if input_match else "data/audio.mp3"
    output_match = re.search(r"save to\s+([^\s]+)", task, re.IGNORECASE)
    output_file = output_match.group(1) if output_match else "output.txt"
    return input_file, output_file

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python B8_transcribe.py <input.mp3> <output.txt>")
    else:
        transcribe_audio(sys.argv[1], sys.argv[2])
