#!/usr/bin/env python

"""Dialogflow API debugger.
Examples:
  python3 dev.py -h
  python3 dev.py -q "hello, how do I reset my password?"
  python3 dev.py "hello" "how do I reset my password?"
"""

import argparse
import os

from DialogFlowClient import DialogflowAClient

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("texts", nargs="+", type=str, default="", help="Text inputs.")

    args = parser.parse_args()

    df_config = {}
    df_config["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    df_config["DIALOGFLOW_PROJECT_ID"] = os.environ.get("DIALOGFLOW_PROJECT_ID")
    df_config["DIALOGFLOW_LANGUAGE_CODE"] = os.environ.get("DIALOGFLOW_LANGUAGE_CODE")

    if (args.texts):
        dialogFlowClient = DialogflowAClient(df_config)
        dialogFlowClient.detect_intent_texts(args.texts)
