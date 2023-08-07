# github indexer
A simple python script to clone new git repos from a selected person and notify you if they are deleted within the day of creation.
## How to use
To run you will have to create a file named .env and put in this
```
GITHUB_TOKEN="your token"
WEBHOOK_URL="your webhook url"
TARGET_USERNAME=user```

Then simply run

```sudo python3 main.py```