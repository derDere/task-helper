

import flet as ft

from task_manager import TaskManager, Task
from organize_page import Organizer
from tasks_page import Tasks
from calendar_page import Calendar
from nav_bar import NavBar


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.task_manager = TaskManager()
        self.organize_page = Organizer(self, self.task_manager)
        self.tasks_page = Tasks(self, self.task_manager)
        self.calendar_page = Calendar(self, self.task_manager)
        self.nav_bar = NavBar(self, self.organize_page, self.tasks_page, self.calendar_page)

        #self.task_manager.add_task(Task("Test Task", "This is a test task", "2024-12-31", False, 1))

    def start(self):

        self.page.title = "Task Helper"

        self.page.window.center()

        self.page.scroll=ft.ScrollMode.AUTO

        #self.page.window.alignment = ft.alignment.center

        #self.page.theme_mode = ft.ThemeMode.LIGHT

        self.page.theme = ft.Theme(
            color_scheme_seed=ft.Colors.PURPLE,
        )

        self.page.add(self.nav_bar.get_content(self.page))
        self.page.update()
