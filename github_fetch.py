import requests
import os

def fetch_python_files(owner, repo):
    # Get GitHub token from environment variable
    token = os.getenv("GITHUB_TOKEN")
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            print("Error: GitHub API rate limit exceeded.")
            print("To increase limits, set your GitHub token as an environment variable:")
            print("  $env:GITHUB_TOKEN = 'your_github_token'")
            print("Get a token at: https://github.com/settings/tokens")
        raise

    files = []
    for item in response.json():
        if item["name"].endswith(".py"):
            try:
                code = requests.get(item["download_url"], headers=headers).text
                files.append(code)
            except Exception as e:
                print(f"Warning: Could not fetch {item['name']}: {e}")
    
    return files


