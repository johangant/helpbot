# See readme.md for instructions on running this code.

from dotenv import load_dotenv
load_dotenv()

import logging
import os
import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument

from typing import Any, Dict

help_message = '''DialogFlow bot
This bot will interact with dialogflow bots.
Simply send this bot a message, and it will respond depending on the configured bot's behaviour.
'''

def get_bot_result(message_content: str, config: Dict[str, str], sender_id: str) -> str:
    if message_content.strip() == '' or message_content.strip() == 'help':
        return config['bot_info']

    SERVICE_USER_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
    DIALOGFLOW_LANGUAGE_CODE = os.getenv("DIALOGFLOW_LANGUAGE_CODE")
    SESSION_ID = os.getenv("SESSION_ID")

    text_to_be_analyzed = message_content.strip()

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        logging.exception(str(e))
        return 'Error. {}.'.format(str(e))

    print("Query text:", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    print("Fulfillment text:", response.query_result.fulfillment_text)
        

class DialogFlowHandler:
    '''
    This plugin allows users to easily add their own
    DialogFlow bots to zulip
    '''

    def initialize(self, bot_handler: Any) -> None:
        self.config_info = bot_handler.get_config_info('dialogflow')

    def usage(self) -> str:
        return '''
            This plugin will allow users to easily add their own
            DialogFlow bots to zulip
            '''

    def handle_message(self, message: Dict[str, str], bot_handler: Any) -> None:
        result = get_bot_result(message['content'], self.config_info, message['sender_email'])
        bot_handler.send_reply(message, result)


handler_class = DialogFlowHandler
