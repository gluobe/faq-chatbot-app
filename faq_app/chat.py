from slackeventsapi import SlackEventAdapter
import slack
import help
import os
from flask import Flask
print(os.getenv('DB_HOST'))
print(os.getenv('DB_USER'))
print(os.getenv('DB_PASSWORD'))
print(os.getenv('DB_NAME'))
print(os.getenv('CONFLUENCE_URL'))
print(os.getenv('CONFLUENCE_USER'))
print(os.getenv('CONFLUENCE_PW'))

try:
    app = Flask(__name__)


    @app.route("/health")
    def hello():
        return "The connection is healthy!!!!!"


    slack_events_adapter = SlackEventAdapter(slack.get_secret(), "/slack/events", app)

    # Deze functie reageerd als in de chat gepost is, men gaan de texr ophallen en antwoorden indien nodig
    @slack_events_adapter.on("message")
    def handle_message(event_data):
        message = event_data["event"]
        channel = message["channel"]
        isGevonden = help.check_for_word(message.get('text'))
        if message.get("subtype") is None and isGevonden:
            slack.zend_bericht(channel, help.get_bericht())
        elif message.get("subtype") is None and ("chuck" in message.get('text') and "norris" in message.get('text')):
            slack.zend_bericht(slack.get_cn_joke())


    @slack_events_adapter.on("error")
    def error_handler(err):
        print("ERROR: " + str(err))


    # starten van de Flask server op port 3000 met de default /events
    if __name__ == "__main__":
        app.run(port=3000, host="0.0.0.0")
except app.error_handler_spec as error:
    print("x")
