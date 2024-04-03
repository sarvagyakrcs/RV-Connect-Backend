import os

# Replace with the path to your local repository on PythonAnywhere
repo_path = "/path/to/your/local/repo"

# Change the current working directory to the repository path
os.chdir(repo_path)

# Perform a git pull to update the local repository
os.system("git pull origin main")

print("Local repository updated with changes from GitHub.")
