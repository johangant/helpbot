#!/usr/bin/env python
import os

from ZulipBot import ZulipBot
from DialogFlowClient import DialogflowAClient

def run():
    # Get key config for our classes.
    zulip_config, df_config = {}, {}

    zulip_config["ZULIP_SITE"] = os.environ.get("ZULIP_SITE")
    zulip_config["ZULIP_EMAIL"] = os.environ.get("ZULIP_EMAIL")
    zulip_config["ZULIP_API_KEY"] = os.environ.get("ZULIP_API_KEY")

    df_config["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    df_config["DIALOGFLOW_PROJECT_ID"] = os.environ.get("DIALOGFLOW_PROJECT_ID")
    df_config["DIALOGFLOW_LANGUAGE_CODE"] = os.environ.get("DIALOGFLOW_LANGUAGE_CODE")

    # Start up instances of DialogflowClient and ZulipBot client classes.
    dialogFlowClient = DialogflowAClient(df_config)

    bot = ZulipBot(zulip_config, dialogFlowClient)
    # Tell our bot to trigger a function on every message from the API.
    bot.client.call_on_each_message(bot.process)
