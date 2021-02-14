import uuid
from google.cloud import dialogflow_v2beta1 as dialogflow

class DialogflowAClient():

    def __init__(self, config):
        self.SERVICE_USER_FILE = config["GOOGLE_APPLICATION_CREDENTIALS"]
        self.DIALOGFLOW_PROJECT_ID = config["DIALOGFLOW_PROJECT_ID"]
        self.DIALOGFLOW_LANGUAGE_CODE = config["DIALOGFLOW_LANGUAGE_CODE"]
        self.DIALOGFLOW_KB_ID = config["DIALOGFLOW_KB_ID"]
        self.session_client = dialogflow.SessionsClient()

    def get_session(self):
        session = {}
        session["id"] = str(uuid.uuid4())
        session["path"] = self.session_client.session_path(self.DIALOGFLOW_PROJECT_ID, session["id"])

        return session

    def handle_query(self, text_query):
        """Returns the result of detect intent with texts as inputs.
        Using the same `session_id` between requests allows continuation
        of the conversation."""

        text_query = text_query.strip()

        if (not text_query):
            return

        session = self.get_session()
        # print('Session path: {}\n'.format(session["path"]))

        text_input = dialogflow.TextInput(text=text_query, language_code=self.DIALOGFLOW_LANGUAGE_CODE)
        # print(text_input)
        query_input = dialogflow.QueryInput(text=text_input)
        # print(query_input)

        response = self.session_client.detect_intent(
            request={"session": session["path"], "query_input": query_input}
        )

        if (response.query_result.intent):
            return response.query_result.fulfillment_text