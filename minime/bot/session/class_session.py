class Session:

    __user = None
    __context = None
    __data = None

    def __init__(self, user):
        self.__data = {}
        self.__user = user

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
