

import flet as ft
from organize_page import Organizer
from tasks_page import Tasks
from calendar_page import Calendar
from nav_bar import NavBar


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.organize_page = Organizer(self)
        self.tasks_page = Tasks(self)
        self.calendar_page = Calendar(self)
        self.nav_bar = NavBar(self, self.organize_page, self.tasks_page, self.calendar_page)

    def start(self):

        self.page.title = "Task Helper"

        self.page.window.center()

        #self.page.window.alignment = ft.alignment.center

        #self.page.theme_mode = ft.ThemeMode.LIGHT

        self.page.theme = ft.Theme(
            color_scheme_seed=ft.Colors.PURPLE,
        )

        self.page.add(self.nav_bar.get_content(self.page))
        self.page.update()
