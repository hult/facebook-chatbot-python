# facebook-chatbot-python
A simple python chatbot for Facebook Messenger.

The bot reads incoming Facebook Messenger messages, and responds by generating random text from a corpus. The length of the response is randomly selected around the length of the incoming message, and a random word from the incoming message is selected as the starting word of the response.

## Installing dependencies

Use of virtualenv is highly recommended, especially since the old version of `nltk` used requires an old version of `setuptools`.

    $ pip install -r requirements.txt

## Setting up a Facebook app for Facebook messenger

* You're going to need a publicly routed https address. I used [ngrok](https://ngrok.com/) to create a tunnel to my local development machine.
* The server will need to be started for you to verify the webhook. See "Starting the server" below.
* Follow the instructions provided in the [Facebook quickstart tutorial](https://developers.facebook.com/docs/messenger-platform/quickstart) for creating a page and an app.
* Set the `VERIFY_TOKEN` and `FACEBOOK_TOKEN` environment variables to the values you get from following the tutorial.

## Building a corpus

Before you start the server, there has to be a file called `corpus.txt` in the root directory. This can be any text, but I found it interesting to use all of my sent emails as the corpus.

If you have your emails in mbox format (you can get them from Gmail using [Google Takeout](https://takeout.google.com/settings/takeout)), you can use the provided `mail_corpus.py` to build a corpus.

    $ python mail_corpus.py emails.mbox youremail1@example.com youremail2@example.com ...

This will grab the text from all emails from the specified addresses (it tries to not include text responded to, signatures and so on), and create a corpus from it.

## Starting the server

Is just a matter of

    $ python server.py

## TODO

* A big corpus takes a loooong time to load
* Tests
* Send structured messages
* Handle postbacks
