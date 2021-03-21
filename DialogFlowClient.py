import json
import uuid
from google.cloud import dialogflow_v2beta1 as dialogflow

class DialogflowClient():

    def __init__(self, config):
        self.SERVICE_USER_FILE = config["GOOGLE_APPLICATION_CREDENTIALS"]
        self.DIALOGFLOW_PROJECT_ID = config["DIALOGFLOW_PROJECT_ID"]
        self.DIALOGFLOW_LANGUAGE_CODE = config["DIALOGFLOW_LANGUAGE_CODE"]
        self.session_client = dialogflow.SessionsClient()

        # Hard baked MVP dictionary of stream mappings to ids.
        self.streams = {
            "alcohol": "275267",
            "covid": "277736",
            "health_champions": "277849",
            "feedback": "275798",
            "finance": "275163",
            "help": "277855",
            "nutrition": "275295",
            "physical_activity": "275271",
            "stop_smoking": "275278",
            "stress": "275528",
        }

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

    def raw_query(self, text_query):
        text_query = text_query.strip()

        if (not text_query):
            return

        session = self.get_session()
        print('Session path: {}\n'.format(session["path"]))

        text_input = dialogflow.TextInput(text=text_query, language_code=self.DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.QueryInput(text=text_input)

        response = self.session_client.detect_intent(
            request={"session": session["path"], "query_input": query_input}
        )

        return response

    def detect_intent_texts(self, texts):
        """Returns the result of detect intent with texts as inputs.
        Using the same `session_id` between requests allows continuation
        of the conversation."""
        session = self.get_session()
        print('Session path: {}\n'.format(session["path"]))

        for text in texts:
            text_input = dialogflow.TextInput(text=text, language_code=self.DIALOGFLOW_LANGUAGE_CODE)
            query_input = dialogflow.QueryInput(text=text_input)

            response = self.session_client.detect_intent(
                request={"session": session["path"], "query_input": query_input}
            )

            print("=" * 20)
            print("Query text: {}".format(response.query_result.query_text))
            print(
                "Detected intent: {} (confidence: {})\n".format(
                    response.query_result.intent.display_name,
                    response.query_result.intent_detection_confidence,
                )
            )

            if (response.query_result.fulfillment_text):
                print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))

            # if (response.query_result.fulfillment_messages):
            #     for message in response.query_result.fulfillment_messages:
            #         m = dialogflow.

