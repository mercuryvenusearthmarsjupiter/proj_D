import os
import re
from github import Github, BadCredentialsException, GithubException
import git

# Get environment variables
repo_name = os.getenv('ORG_REPO')
branch = os.getenv('branch')
since = os.getenv('since')
workspace_path = os.getenv('WORKSPACE')
print("in main : ",repo_name, branch, workspace_path)
github_token = os.getenv('GITHUB_TOKEN')
# Initialize GitHub client
g = Github(github_token)
print("g   :",g)
repo = g.get_repo(repo_name)
print("repo   :", repo)
prohibited_file = os.path.join(workspace_path, 'abandoned_files.txt')

# Function to extract PR number from the commit message
def extract_pr_number(commit_message):
    match = re.search(r"#(\d+)", commit_message)
    if match:
        return match.group(1)
    return None

# Loop through merged commits in the last week
for commit in repo.iter_commits(branch, since):  # 'master' is the branch name
    if commit.merge:  # Check if the commit is a merge commit
        pr_number = extract_pr_number(commit.message)
        if pr_number:
            # Get the files changed in the merge commit
            changed_files = commit.stats.files
            for file_path in changed_files:
                print(f"PR #{pr_number} - {file_path}")
