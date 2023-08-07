# Github indexer

This Python script is designed to track a specific GitHub user's repositories and send a Discord notification if any repositories are deleted within a day of their creation.

Requirements
- Python 3.6 or newer
- A GitHub Personal Access Token with "public_repo" scope. More info about creating a token can be found in the [GitHub Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- A Discord Webhook URL for sending notifications to a Discord channel. More info about creating a webhook can be found in the [Discord documentation](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

## Setup

1. Clone the repository to your local machine:
```
git clone https://github.com/azhrcs/github-indexer.git```

2. Navigate to the github indexer directory
```
cd 'github indexer'```

3. Set your GitHub token and Discord Webhook URL as environment variables:

For Unix systems (Linux/MacOS):
```
export TARGET_USERNAME=target_user
export GITHUB_TOKEN=your_github_token
export DISCORD_WEBHOOK_URL=your_discord_webhook_url
```
For Windows Command Prompt:
```
set TARGET_USERNAME=target_user
set GITHUB_TOKEN=your_github_token
set DISCORD_WEBHOOK_URL=your_discord_webhook_url
```
For Windows PowerShell:
```
$env:TARGET_USERNAME="target_user"
$env:GITHUB_TOKEN="your_github_token"
$env:DISCORD_WEBHOOK_URL="your_discord_webhook_url"
```

4. run the script
```
python3 main.py```
