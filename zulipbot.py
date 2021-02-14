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
            response = self.help_message()
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

    def help_message(self):
        message = "Hello, here are a few things you can ask me to help with.\
                \n* Ask me about healthy eating. Eg: Where can I find out about healthy diets and eating?\
                \n* Someone to support you with your action plan. Eg: Who can I chat with to help me with my action plan?\
                \nI'm learning all the time and I'm currently in my early stages so please be kind. If you have ideas about\
                what else you might like me to help with, or the quality of my answers, please pop a message into\
                [the feedback stream](https://nichs.zulipchat.com/#narrow/stream/275798-Feedback/topic/Comments/near/224995780)"

        return message