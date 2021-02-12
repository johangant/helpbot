import os
import zulip
import dialogflow_adapter as df 

# # Set Zulip server details.
ZULIP_SITE = os.environ.get("ZULIP_SITE")
ZULIP_EMAIL = os.environ.get("ZULIP_EMAIL")
ZULIP_API_KEY = os.environ.get("ZULIP_API_KEY")

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
        content = msg["content"].strip()
        sender_email = msg["sender_email"]
        type = msg["type"]
        stream_name = msg['display_recipient']
        stream_topic = msg['subject']

        if sender_email == ZULIP_EMAIL:
            return 

        response = ""
        
        if (content.lower() == "help"):
            response = "You rang??"
        else:
            df_response = df.detect_intent_knowledge(content)
            first_answer = next(iter(df_response.answers))
            response = first_answer.answer

        # First answer (For now).        
        message = {
            "type": type,
            "subject": msg["subject"],
            "to": sender_email,
            "content": response,
        }

        self.client.send_message(message)