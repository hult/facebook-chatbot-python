# coding: utf-8

import random
import warnings
import re
import os
from flask import Flask, request
import nltk
import nltk.model.ngram

import messenger

app = Flask(__name__)

FACEBOOK_TOKEN = os.environ['FACEBOOK_TOKEN']
content_model = None

def create_content_model(text):
    tokens = nltk.word_tokenize(text)
    print "tokenized"
    m = nltk.model.ngram.NgramModel(3, tokens)
    print "modelized"
    return m

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

        # Pick a random word from the incoming message
        input_tokens = nltk.word_tokenize(message)
        keyword = random.choice(input_tokens)

        # Use keyword and input length to seed a response
        input_length = len(input_tokens)
        num_response_words = int(random.gauss(input_length, input_length / 2)) + 1
        print "Basing response on keyword %s and length %d" % (keyword, num_response_words)
        content = content_model.generate(num_response_words, (keyword,))
        response = format_response(content)

        # Send the response back
        print "Outgoing to %s: %s" % (sender, response)
        messenger.send_message(FACEBOOK_TOKEN, sender, response)

    return "ok"

def format_response(content):
    def to_unicode(x):
        if isinstance(x, str):
            return x.decode('utf-8')
        return x

    s = u' '.join([to_unicode(c) for c in content])
    s = re.sub(r' ([\?,\.:!])', r'\1', s)  # Remove spaces before separators
    return s

if __name__ == '__main__':
    # Suppress nltk warnings about not enough data
    warnings.filterwarnings('ignore', '.*returning an arbitrary sample.*',)

    if os.path.exists("corpus.txt"):
        content_model = create_content_model(open("corpus.txt").read())

    app.run(port=3000, debug=True)
