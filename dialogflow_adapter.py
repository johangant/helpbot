import os 
import uuid
from google.cloud import dialogflow_v2beta1 as dialogflow

SERVICE_USER_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
DIALOGFLOW_PROJECT_ID = os.environ.get("DIALOGFLOW_PROJECT_ID")
DIALOGFLOW_LANGUAGE_CODE = os.environ.get("DIALOGFLOW_LANGUAGE_CODE")
DIALOGFLOW_KB_ID = os.environ.get("DIALOGFLOW_KB_ID")

def detect_intent_knowledge(text_query):
    """Returns the result of detect intent with querying Knowledge Connector."""    
    session_id = str(uuid.uuid4())

    session_client = dialogflow.SessionsClient()

    session_path = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)
    print('Session path: {}\n'.format(session_path))

    text_input = dialogflow.TextInput(text=text_query, language_code=DIALOGFLOW_LANGUAGE_CODE)

    query_input = dialogflow.QueryInput(text=text_input)

    knowledge_base_path = dialogflow.KnowledgeBasesClient \
        .knowledge_base_path(DIALOGFLOW_PROJECT_ID, DIALOGFLOW_KB_ID)

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