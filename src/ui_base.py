

import flet as ft
from abc import abstractmethod


class UIBase:

    def __init__(self, parent):
        self.parent = parent
        self.content = None
    
    @abstractmethod
    def _get_content(self, page:ft.Page):
        pass

    def get_content(self, page:ft.Page):
        self.content = self._get_content(page)
        return self.content
