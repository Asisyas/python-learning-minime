import random

import minime.bot.actions.environment.class_action as env


class Action_Factory:

    __a_providers = {}

    def register_coll(self, providers):
        for provider in providers:
            self.register(provider)

    def register(self, action_provider):
        tag = action_provider.get_tag()

        self.__a_providers.update({ tag: action_provider })

    def run_action(self, session, tag, context, tokens, answers, sentense):
       ap = self.__a_providers.get(tag)
       if ap is None:
           return random.choice(answers)

       return ap.run(
           tokens = tokens,
           answers = answers,
           session = session,
           tag = tag,
           context = context,
           sentense = sentense
       )


action_factory = Action_Factory()

action_factory.register_coll([
    env.Action_Environment()
])