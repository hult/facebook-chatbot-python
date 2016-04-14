import random
import re
import nltk

class Bot(object):
    def __init__(self, text):
        tokens = nltk.word_tokenize(text)
        print "tokenized"
        self._model = nltk.model.ngram.NgramModel(3, tokens)
        print "modelized"

    def respond_to(self, message):
        # Pick a random word from the incoming message
        input_tokens = nltk.word_tokenize(message)
        keyword = random.choice(input_tokens)

        # Use keyword and input length to seed a response
        input_length = len(input_tokens)
        num_response_words = int(random.gauss(input_length, input_length / 2)) + 1
        print "Basing response on keyword %s and length %d" % (keyword, num_response_words)
        content = self._model.generate(num_response_words, (keyword,))
        return self._format_response(content)

    def _format_response(self, content):
        def to_unicode(x):
            if isinstance(x, str):
                return x.decode('utf-8')
            return x

        s = u' '.join([to_unicode(c) for c in content])
        s = re.sub(r' ([\?,\.:!])', r'\1', s)  # Remove spaces before separators
        return s
