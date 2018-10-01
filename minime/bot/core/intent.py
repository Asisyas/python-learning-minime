class Intents_Collection:
    __intents = None

    def __init__(self, intents):
       self.__intents = intents

    def get_intents( self ):
        return self.__intents