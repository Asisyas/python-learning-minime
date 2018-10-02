class Git_Service:

    _services = {}

    def register_service(self, alias, git_obj):
        self._services.update({alias : git_obj})

    def get_service(self, name):
        return self._services.get(name)


