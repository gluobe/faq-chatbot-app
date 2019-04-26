from slacker import Slacker
from slackeventsapi import SlackEventAdapter
import os

servicedesk = Slacker(os.getenv('SLACK_ACCES_TOKEN'))
slack_signing_secret = os.getenv('SLACK_SECRET')
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")


def zend_bericht( message):
    servicedesk.chat.post_message('#general', message)


def get_secret():
    return slack_signing_secret
