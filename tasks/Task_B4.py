import sys
import os
import subprocess

DATA_DIR = "data/"

def clone_and_commit(repo_url, commit_message):
    """Clone a Git repo into /data/, modify a file, commit, and push."""

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    repo_path = os.path.join(DATA_DIR, repo_name)

    if os.path.exists(repo_path):
        print(f"📂 Repository already exists at {repo_path}, pulling latest changes...")
        subprocess.run(["git", "-C", repo_path, "pull"], check=True)
    else:
        print(f"🔄 Cloning repository from {repo_url}...")
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)

    # Modify a file in the repo
    log_file = os.path.join(repo_path, "automation_log.txt")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"Automated commit: {commit_message}\n")

    # Commit and push changes
    subprocess.run(["git", "-C", repo_path, "add", "automation_log.txt"], check=True)
    subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "-C", repo_path, "push"], check=True)

    print(f"✅ Changes committed and pushed: {commit_message}")

def extract_clone_and_commit(task: str):
    """
    For B4: Clone a git repo and commit.
    Extracts:
      - Repo URL: Looks for an HTTP/HTTPS URL ending with .git.
      - Commit message: Looks for a quoted string following "commit" (if provided).
    """
    repo_match = re.search(r"(https?://[^\s]+\.git)", task)
    repo_url = repo_match.group(0) if repo_match else "https://github.com/KB-iitm/email-json.git"
    commit_match = re.search(r'commit(?: with message)?\s+"([^"]+)"', task, re.IGNORECASE)
    commit_message = commit_match.group(1) if commit_match else "Data was committed"
    return repo_url, commit_message


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python B4_clone_commit.py <GIT_REPO_URL> <COMMIT_MESSAGE>")
        print("Example: python B4_clone_commit.py 'https://github.com/user/repo.git' 'Updated automation log'")
    else:
        clone_and_commit(sys.argv[1], sys.argv[2])
