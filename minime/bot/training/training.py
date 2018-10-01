import minime.bot.core.intent_factory as intnt_factory
import minime.bot.core.model_factory as mdl_factory

import nltk
# things we need for Tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random
import pickle
from nltk.stem.lancaster import LancasterStemmer


class Training_Engine:
    __intents_collection = None
    __words = []
    __classes = []
    __documents = []
    __ignore_words = ['?']

    __save_model_pickle_file = './brain_data/training_data'
    __save_model_file = './brain_data/model.tflearn'

    __intents_collection_factory = None
    __stemmer = None
    __mdl_factory = None

    def __init__(self):
        nltk.download('punkt')
        int_fact = intnt_factory.Intents_Collection_Factory()

        self.__intents_collection = int_fact.create_intent_collection_from_json_file("config/intents.json")
        self.__stemmer = LancasterStemmer()
        self.__mdl_factory = mdl_factory.Model_Factory()

    def run(self):

        intents = self.__intents_collection.get_intents()

        for intent in intents:
            for pattern in intent['patterns']:
                w = nltk.word_tokenize(pattern)
                self.__words.extend(w)
                self.__documents.append((w, intent['tag']))
                if intent['tag'] not in self.__classes:
                    self.__classes.append(intent['tag'])

        self.__words = [self.__stemmer.stem(w.lower()) for w in self.__words if w not in self.__ignore_words]
        self.__words = sorted(list(set(self.__words)))
        self.__classes = sorted(list(set(self.__classes)))

        training = []
        output = []
        output_empty = [0] * len(self.__classes)

        for doc in self.__documents:
            bag = []
            pattern_words = doc[0]
            pattern_words = [self.__stemmer.stem(word.lower()) for word in pattern_words]
            for w in self.__words:
                bag.append(1) if w in pattern_words else bag.append(0)

            # output is a '0' for each tag and '1' for current tag
            output_row = list(output_empty)
            output_row[self.__classes.index(doc[1])] = 1

            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training)

        train_x = list(training[:, 0])
        train_y = list(training[:, 1])

        tf.reset_default_graph()

        model = self.__mdl_factory.create_model(train_x, train_y)
        model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)

        self._dump_model(model, train_x, train_y)

    def _dump_model(self, model, train_x, train_y):
        model.save(self.__save_model_file)

        pickle.dump({'words': self.__words, 'classes': self.__classes, 'train_x': train_x, 'train_y': train_y},
                    open(self.__save_model_pickle_file, "wb"))
