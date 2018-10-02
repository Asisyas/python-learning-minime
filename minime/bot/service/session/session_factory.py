import uuid
import minime.bot.service.session.class_session as s

class Session_Factory:
    __sess = {}

    def create(self, user = None):
         guid = uuid.uuid4()
         sess = s.Session(guid,user)

         self.__sess.update({guid: sess})

         return sess

    def get_session_by_id(self, session_id):
        return self.__sess.get(session_id)


_session_factory = None

def get_default():
    if _session_factory is not None:
        return _session_factory

    __session_factory = Session_Factory()

    return  __session_factory
