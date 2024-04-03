import os
from dotenv import load_dotenv
from github import Github

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")
repo_owner = "RV-Connect"
repo_name = "RV_Connect"

# Authenticate with GitHub using your personal access token
g = Github(github_token)

# Get the Repository object
repo = g.get_repo(f"{repo_owner}/{repo_name}")

# Create a branch with a new commit
# You would replace this with your actual code changes
branch_name = "my-feature-branch"
branch = repo.get_branch("main")  # Assuming you're pushing changes to the main branch
new_commit = repo.create_git_commit("Commit message", "file.txt", "Content", branch.commit.sha, branch_name)

# Create a new branch with the new commit
ref = repo.create_git_ref(f"refs/heads/{branch_name}", new_commit.sha)

# Create a pull request
pull = repo.create_pull(title="My Pull Request", body="Description of my changes", base="main", head=branch_name)

# Merge the pull request
pull.merge()

print("Changes pushed successfully.")
