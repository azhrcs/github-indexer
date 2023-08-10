import os
import time
import requests
from datetime import datetime, timedelta

YOUR_DISCORD_WEBHOOK_URL = os.getenv("WEBHOOK_URL")
TARGET_USERNAME = os.getenv("TARGET_USERNAME")

def get_repositories(user):
    url = f"https://api.github.com/users/{user}/repos"
    headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {repo['name']: repo['created_at'] for repo in response.json()}
    except requests.RequestException as e:
        print(f"Error: {e}")
        return {}

def less_than_a_day_old(timestamp):
    created_at = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    return datetime.now() - created_at < timedelta(days=1)

def notify_discord(deleted_repos):
    for repo, timestamp in deleted_repos.items():
        data = {
            'content': f"Repository {repo} that was created at {timestamp} has been deleted."
        }
        result = requests.post(YOUR_DISCORD_WEBHOOK_URL, json=data)
        message = 'Notification sent to Discord.' if result.status_code == 200 else f'Failed to send notification to Discord, status code: {result.status_code}'
        print(message)

def main():
    user = TARGET_USERNAME
    previous_repositories = get_repositories(user)

    while True:
        time.sleep(24 * 60 * 60)  # wait for a day

        current_repositories = get_repositories(user)
        deleted_repos = {
            repo: timestamp for repo, timestamp in previous_repositories.items()
            if repo not in current_repositories and less_than_a_day_old(timestamp)
        }

        if deleted_repos:
            notify_discord(deleted_repos)

        previous_repositories = current_repositories

if __name__ == "__main__":
    main()
