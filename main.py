import os
import json
import requests
from datetime import datetime, timedelta
from smtplib import SMTP
import subprocess

# Fetch your token from environment variables for safety
user = os.getenv("TARGET")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
SCRAPER_EMAIL= os.getenv("SCRAPER_EMAIL")
MY_EMAIL = os.getenv("MY_EMAIL")
SCRAPER_EMAIL_PASS = os.getenv("SCRAPER_EMAIL_PASS")
EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER")
headers = {'Authorization': f'token {GITHUB_TOKEN}'}

BASE_PATH = "/'github indexer'/repos"  # Change this to the path where you want to store the repositories

print(os.getenv('GITHUB_TOKEN'))

def get_repositories(user):
    url = f"https://api.github.com/users/{user}/repos"
    response = requests.get(url, headers=headers)
    
    content = response.json()
    
    if response.status_code != 200:  # Check if the API response indicates an error
        print(f"Error {response.status_code}: {content.get('message')}")
        return {}

    elif isinstance(content, list):  # Ensure content is a list
        return {repo['name']: repo['created_at'] for repo in content}
    else:
        print(f"Unexpected content: {content}")
        return {}


def read_tracked_repositories():
    with open('tracked_repositories.json', 'r') as f:
        return json.load(f)

def write_repositories_to_file(repositories):
    with open('tracked_repositories.json', 'w') as f:
        json.dump(repositories, f)

def send_email(subject, body):
    from email.message import EmailMessage
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SCRAPER_EMAIL
    msg['To'] = MY_EMAIL

    # establish SMTP connection and send email
    with SMTP(EMAIL_PROVIDER) as s:
        s.login(SCRAPER_EMAIL, SCRAPER_EMAIL_PASS)
        s.send_message(msg)

def clone_repository(user, repo_name):
    repo_url = f"https://github.com/{user}/{repo_name}.git"
    clone_path = os.path.join(BASE_PATH, repo_name)
    subprocess.run(["git", "clone", repo_url, clone_path])

def main():
    current_repositories = get_repositories(user)
    
    try:
        tracked_repositories = read_tracked_repositories()
    except FileNotFoundError:
        tracked_repositories = {}
    
    for repo, _ in current_repositories.items():
        if repo not in tracked_repositories:
            clone_repository(user, repo)

    recently_deleted_repos = []
    for repo, created_at in tracked_repositories.items():
        if repo not in current_repositories:
            creation_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
            if datetime.now() - creation_date <= timedelta(days=1):  # check if the repository was created within the last day
                recently_deleted_repos.append(repo)
                
    if recently_deleted_repos:
        send_email("Recently deleted repositories!", f"The following repositories have been deleted within a day of their creation: {', '.join(recently_deleted_repos)}")
    
    # Update the tracked repositories with the current list
    write_repositories_to_file(current_repositories)

if __name__ == "__main__":
    main()
