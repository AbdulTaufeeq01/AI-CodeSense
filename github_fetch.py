import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_python_files(owner, repo):
    # Get GitHub token from .env file
    token = os.getenv("GITHUB_TOKEN")
    headers = {}
    if token and token != "your_github_token_here":
        headers["Authorization"] = f"token {token}"
    
    url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    
    # Supported file extensions
    supported_extensions = ('.py', '.java', '.js', '.ts', '.cpp', '.c', '.go', '.rs')
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            print("Error: GitHub API rate limit exceeded.")
            print("To fix this:")
            print("  1. Get a token at: https://github.com/settings/tokens (select 'repo' scope)")
            print("  2. Edit .env file and replace 'your_github_token_here' with your token")
            print("  3. Run the script again")
        raise

    files = []
    for item in response.json():
        if item["name"].endswith(supported_extensions):
            try:
                code = requests.get(item["download_url"], headers=headers).text
                files.append(code)
            except Exception as e:
                print(f"Warning: Could not fetch {item['name']}: {e}")
    
    if not files:
        print(f"⚠️  Warning: No supported files found in {owner}/{repo}")
        print(f"   Supported extensions: {', '.join(supported_extensions)}")
    
    return files



