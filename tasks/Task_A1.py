def install_uv():
    """Install uv if it's not already installed."""
    try:
        subprocess.run(["uv", "--version"], check=True, stdout=subprocess.DEVNULL)
        print("uv is already installed.")
    except subprocess.CalledProcessError:
        print("Installing uv...")
        subprocess.run(["pip", "install", "uv"], check=True)

def run_datagen(user_email: str):
    """Download and run datagen.py with user email as an argument."""
    url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    script_path = r"C:\Users\kathb\TDS_Project\datagen.py"

    # Download the script
    response = requests.get(url)
    response.raise_for_status()

    # Save to a local file
    with open(script_path, "w") as f:
        f.write(response.text)

    # Run the script
    subprocess.run(["python", script_path, user_email], check=True)

# Example usage
if __name__ == "__main__":
    user_email = "23ds3000241@ds.study.iitm.ac.in"  # Replace this dynamically in your implementation
    install_uv()
    run_datagen(user_email)