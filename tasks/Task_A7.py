import openai

def extract_email_sender(input_file: str, output_file: str):
    """Extract sender email using an LLM."""
    with open(input_file, "r", encoding="utf-8") as f:
        email_content = f.read()

    client = openai.OpenAI()  # Create an OpenAI client

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Extract the sender's email address from the given email content."},
            {"role": "user", "content": email_content}
        ]
    )

    sender_email = response.choices[0].message.content.strip()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(sender_email)

# Example usage
if __name__ == "__main__":
    extract_email_sender(r"C:\Users\kathb\TDS_Project\data\email.txt",
                     r"C:\Users\kathb\TDS_Project\data\email-sender.txt")