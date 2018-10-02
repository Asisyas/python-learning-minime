class Session:

    __user = None
    __context = None
    __data = None
    __id = None
    __tag = None

    def __init__(self, id, user):
        self.__data = {}
        self.__user = user
        self.__id = id

    @property
    def id(self):
        return self.__id

    @property
    def tag(self):
        return self.__tag

    @tag.setter
    def tag(self, tag):
        self.__tag = tag

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, context):
        self.__context = context

    @property
    def user(self):
        return self.__user

    def get_param(self, key):
        return self.__data.get(key)

    def set_param(self, key, value):
        self.__data.update({key: value})
