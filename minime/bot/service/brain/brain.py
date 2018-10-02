import minime.bot.core.intent_factory as int_fac
import minime.bot.core.model_factory as mdl_factory
import minime.bot.actions.class_action_factory as af
import nltk
import numpy as np

from nltk.stem.lancaster import LancasterStemmer

import pickle


class Bot_Brain:
    ERROR_THRESHOLD = 0.6

    stemmer = None
    sentence_words = None
    model = None
    intents = None
    words = None
    classes = None

    def __init__(self):
        self.sentence_words = LancasterStemmer()
        self.stemmer = LancasterStemmer()

        data = pickle.load(open("./brain_data/training_data", "rb"))
        self.words = data['words']
        self.classes = data['classes']

        train_x = data['train_x']
        train_y = data['train_y']

        model_factory = mdl_factory.Model_Factory()
        intents_coll_factory = int_fac.Intents_Collection_Factory()

        self.intents = intents_coll_factory.create_intent_collection_from_json_file("./config/intents.json")

        self.model = model_factory.create_model(train_x, train_y)
        self.model.load('./brain_data/model.tflearn')

    def clean_up_sentence(self, sentence):
        #    global stemmer
        # tokenize the pattern
        sentence_words = nltk.word_tokenize(sentence)
        # stem each word
        sentence_words = [self.stemmer.stem(word.lower()) for word in sentence_words]

        return sentence_words

    def bow(self, sentence, words, show_details=False):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words
        bag = [0] * len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)

        return (np.array(bag))

    def classify(self, sentence):
        # generate probabilities from the model
        results = self.model.predict([self.bow(sentence, self.words)])[0]
        # filter out predictions below a threshold
        results = [[i, r] for i, r in enumerate(results) if r > self.ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append((self.classes[r[0]], r[1]))
        # return tuple of intent and probability
        return return_list

    def response(self, sentence, session):
        results = self.classify(sentence)

        context_prev = session.context
        session_tag = session.tag

        curr_context = None
        curr_tag = None
        curr_answers = None

        if session_tag is not None:
            return self._response(session,
                session_tag,
                context_prev,
                self.clean_up_sentence(sentence),
                [])


        # if we have a classification then find the matching intent tag
        if results:
            # loop as long as there are matches to process
            while results:
                for i in self.intents.get_intents():
                    tmp_tag = i['tag']
                    # find a tag matching the first result
                    if tmp_tag == results[0][0]:
                        # set context for this intent if necessary
                        if 'context_set' in i:
                            curr_context = i['context_set']

                        # check if this intent is contextual and applies to this user's conversation
                        if not 'context_filter' in i or \
                                (context_prev and
                                 'context_filter' in i
                                 and i['context_filter'] == context_prev):
                            # a random response from the intent
                            return self._response(session, tmp_tag, curr_context,
                                                  self.clean_up_sentence(sentence), i['responses'],
                                                  sentence
                                                  )

                results.pop(0)


    def _response(self, session, tag, context, tokens, answers, sentense):
        return af.action_factory.run_action(session, tag, context, tokens, answers, sentense)