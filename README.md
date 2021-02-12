# HelpBot

A small bot that allows Zulip users to @mention it and receive feedback from a DialogFlow backend service.

# Requirements

* Python 3
* Pip 3
* virtualenv for Python 3
* Dialogflow Agent configured and set up.
* Dialogflow API enabled and service user credentials file downloaded locally.
* Zulip instance configured with 'Generic bot'

# Local work

**Environment variables**

* Copy the example environment variables file to a standard `.env` file: `cp .env.example .env` and populate it with your details. **NEVER COMMIT THIS FILE TO SOURCE CODE**.
* Create a new Python virtual environment: `python3 -m venv venv`
* Activate it: `source env/bin/activate`
* Install dependencies: `pip3 install -r requirements.txt`
* Load your environment variables: `source .env`
* Start the app: `python3 app.py`

Exit the virtual environment with `deactivate`