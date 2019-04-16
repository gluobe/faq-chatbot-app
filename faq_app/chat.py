from slackeventsapi import SlackEventAdapter
import slack
import help

# testcomment

slack_events_adapter = SlackEventAdapter(slack.get_secret(), "/slack/events")


# Deze functie reageerd als in de chat gepost is, men gaan de texr ophallen en antwoorden indien nodig
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    isGevonden = help.check_for_word(message.get('text'))
    if message.get("subtype") is None and isGevonden:
        slack.zend_bericht(help.get_bericht())
    elif message.get("subtype") is None and ("chuck" in message.get('text') and "norris" in message.get('text')):
        slack.zend_bericht(slack.get_cn_joke())


@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


# starten van de Flask server op port 3000 met de default /events
slack_events_adapter.start(port=3000, host="0.0.0.0")
