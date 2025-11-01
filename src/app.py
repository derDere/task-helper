

import flet as ft
from front_page import FrontPage


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.front_page = FrontPage(self)

    def start(self):
        self.page.title = "Task Helper"
        self.page.add(self.front_page.get_content())
        self.page.update()
