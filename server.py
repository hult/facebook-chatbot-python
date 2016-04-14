# coding: utf-8

import warnings
import os
from flask import Flask, request

import chatbot
import messenger

app = Flask(__name__)

FACEBOOK_TOKEN = os.environ['FACEBOOK_TOKEN']
bot = None

@app.route('/', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == os.environ['VERIFY_TOKEN']:
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def webhook():
    payload = request.get_data()
    for sender, message in messenger.messaging_events(payload):
        print "Incoming from %s: %s" % (sender, message)

        response = bot.respond_to(message)

        print "Outgoing to %s: %s" % (sender, response)
        messenger.send_message(FACEBOOK_TOKEN, sender, response)

    return "ok"

if __name__ == '__main__':
    # Suppress nltk warnings about not enough data
    warnings.filterwarnings('ignore', '.*returning an arbitrary sample.*',)

    if os.path.exists("corpus.txt"):
        bot = chatbot.Bot(open("corpus.txt").read())

    app.run(port=3000, debug=True)
