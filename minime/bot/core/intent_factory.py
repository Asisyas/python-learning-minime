import minime.bot.core.intent as intnt
import json

class Intents_Collection_Factory:

    __intnts_cache = {}

    def create_intent_collection( self, intents_array ):
        return intnt.Intents_Collection( intents_array )

    def create_intent_collection_from_json_file(self, intents_json_file):
        cached = self.__intnts_cache.get( intents_json_file )

        if cached:
            return cached

        with open( intents_json_file ) as intents_data:
            intents = json.load(intents_data)
            intents = intents['intents']

        intents_coll = intnt.Intents_Collection( intents )

        self.__intnts_cache.update( { intents_json_file: intents_coll } )

        return intents_coll
