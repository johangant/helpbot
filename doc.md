# HealthBot

This bot allows Zulip users to mention `@HealthBot` in private or public streams and receive responses from a DialogFlow backend.

## Setup

Add environment variables for:

```
SERVICE_USER_FILE
DIALOGFLOW_PROJECT_ID
DIALOGFLOW_LANGUAGE_CODE
DIALOGFLOW_KB_ID
ZULIP_SITE
ZULIP_EMAIL
ZULIP_API_KEY
```

## Usage

Start the bot: `python healthbot.py`

Mention the bot in order to say things to it: `@HealthBot I'd like to find out more about eating well`

## LICENSE

MIT.