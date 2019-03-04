from slacker import Slacker
from slackeventsapi import SlackEventAdapter

chucknorris_api = 'http://api.icndb.com/jokes/random/'
clank = Slacker('xoxb-555682767666-559725976260-2Y2Ho96wBukzlTohnjXrz0vK')
slack_signing_secret = "c6746653654493e16297fd7c04913564"
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")


def zend_bericht( message):
    clank.chat.post_message('#general', message)


def get_secret():
    return slack_signing_secret
