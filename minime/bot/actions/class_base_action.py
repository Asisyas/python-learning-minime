from abc import ABCMeta, abstractmethod

class Base_Action:
    @abstractmethod
    def get_tag(self):
        pass

    def run(self, **kwargs):
        print("RUN ACTION [" + self.get_tag() + "]")