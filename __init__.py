import minime.bot.core.intent_factory as int_fac
import minime.bot.core.model_factory as mdl_factory
import minime.bot.actions.class_action_factory as af
import nltk
import numpy as np

from nltk.stem.lancaster import LancasterStemmer

import pickle


sentence_words = LancasterStemmer()
stemmer = LancasterStemmer()

data = pickle.load( open( "./brain_data/training_data", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

model_factory = mdl_factory.Model_Factory()
intents_coll_factory = int_fac.Intents_Collection_Factory()

intents = intents_coll_factory.create_intent_collection_from_json_file( "./config/intents.json" )

model = model_factory.create_model(train_x,train_y)
model.load('./brain_data/model.tflearn')


# create a data structure to hold user context
context = {}

ERROR_THRESHOLD = 0.6


def clean_up_sentence(sentence):
#    global stemmer
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))



def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)

    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents.get_intents():
                tmp_tag = i['tag']
                # find a tag matching the first result
                if tmp_tag == results[0][0]:
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']

                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', tmp_tag)
                        # a random response from the intent
                        return print(af.action_factory.run_action(tmp_tag, clean_up_sentence(sentence), i['responses']))

            results.pop(0)



while True:
    s = input()

    if s == 'exit':
        break

    print(classify(s))
    print(response(s))
    print("--------------")