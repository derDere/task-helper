

from abc import abstractmethod


class UIBase:

    def __init__(self, parent):
        self.parent = parent
        self.content = None
    
    @abstractmethod
    def _get_content(self):
        pass

    def get_content(self):
        self.content = self._get_content()
        return self.content
