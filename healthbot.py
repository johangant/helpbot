#!/usr/bin/env python

import zulip
import uuid
import os
import json

def detect_intent_knowledge(project_id, session_id, language_code,
                            knowledge_base_id, text_query):
    """Returns the result of detect intent with querying Knowledge Connector.

    Args:
    project_id: The GCP project linked with the agent you are going to query.
    session_id: Id of the session, using the same `session_id` between requests
              allows continuation of the conversation.
    language_code: Language of the queries.
    knowledge_base_id: The Knowledge base's id to query against.
    texts: A list of text queries to send.
    """
    from google.cloud import dialogflow_v2beta1 as dialogflow
    session_client = dialogflow.SessionsClient()

    session_path = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session_path))

    text_input = dialogflow.TextInput(text=text_query, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    knowledge_base_path = dialogflow.KnowledgeBasesClient \
        .knowledge_base_path(project_id, knowledge_base_id)

    query_params = dialogflow.QueryParameters(
        knowledge_base_names=[knowledge_base_path])

    request = dialogflow.DetectIntentRequest(
        session=session_path,
        query_input=query_input,
        query_params=query_params
    )
    response = session_client.detect_intent(request=request)

    # print('=' * 20)
    # print('Query text: {}'.format(response.query_result.query_text))
    # print('Detected intent: {} (confidence: {})\n'.format(
    #     response.query_result.intent.display_name,
    #     response.query_result.intent_detection_confidence))
    # print('Fulfillment text: {}\n'.format(
    #     response.query_result.fulfillment_text))
    # print('Knowledge results:')
    knowledge_answers = response.query_result.knowledge_answers
    # for answers in knowledge_answers.answers:
    #     print(' - Answer: {}'.format(answers.answer))
    #     print(' - Confidence: {}'.format(
    #         answers.match_confidence))
    return knowledge_answers

class ZulipBot(object):
    def __init__(self):
        self.client = zulip.Client()
        self.subscribe_all()
        print("SUCCESS: Zulip bot started, press Ctrl/Cmd + C to exit")

    def subscribe_all(self):
        json = self.client.get_streams()
        streams = [{"name": stream["name"]} for stream in json["streams"]]
        self.client.add_subscriptions(streams)

    def process(self, msg):
        content = msg["content"]
        sender_email = msg["sender_email"]
        type = msg["type"]
        stream_name = msg['display_recipient']
        stream_topic = msg['subject']

        if sender_email == ZULIP_EMAIL:
            return 

        df_response = detect_intent_knowledge(DIALOGFLOW_PROJECT_ID, SESSION_ID,
                            DIALOGFLOW_LANGUAGE_CODE, DIALOGFLOW_KB_ID,
                            content)
        first_answer = next(iter(df_response.answers))

        # First answer (For now).        
        message = {
            "type": type,
            "subject": msg["subject"],
            "to": sender_email,
            "content": first_answer.answer,
        }

        self.client.send_message(message)

def main():
    SERVICE_USER_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    DIALOGFLOW_PROJECT_ID = os.environ.get("DIALOGFLOW_PROJECT_ID")
    DIALOGFLOW_LANGUAGE_CODE = os.environ.get("DIALOGFLOW_LANGUAGE_CODE")
    DIALOGFLOW_KB_ID = os.environ.get("DIALOGFLOW_KB_ID")
    SESSION_ID = str(uuid.uuid4())

    # Set Zulip server details.
    ZULIP_SITE = os.environ.get("ZULIP_SITE")
    ZULIP_EMAIL = os.environ.get("ZULIP_EMAIL")
    ZULIP_API_KEY = os.environ.get("ZULIP_API_KEY")

    # Activate Zulip client
    bot = ZulipBot()
    bot.client.call_on_each_message(bot.process)    

    # DEBUG
    # df_response = detect_intent_knowledge(DIALOGFLOW_PROJECT_ID, SESSION_ID,
    #                         DIALOGFLOW_LANGUAGE_CODE, DIALOGFLOW_KB_ID,
    #                         "Hi, tell me about a better diet please")

    # first_answer = next(iter(df_response.answers))
    # print(first_answer.answer)

if __name__ == '__main__':    
    try:
        main()
    except KeyboardInterrupt:
        print("HealthBot stopping")
        sys.exit(0)