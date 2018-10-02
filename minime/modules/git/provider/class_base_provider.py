class Base_Provider:
    _name = None

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def get_branches(self):
        pass

    def get_tags(self):
        pass