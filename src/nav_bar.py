

import flet as ft

from ui_base import UIBase


class NavBar(UIBase):

    def __init__(self, parent, organizer, tasks, calendar):
        super().__init__(parent)
        self.organizer = organizer
        self.tasks = tasks
        self.calendar = calendar
    
    def _switch_page(self, event):
        index = event.control.selected_index
        self.organizer.content.visible = (index == 0)
        self.tasks.content.visible = (index == 1)
        self.calendar.content.visible = (index == 2)
        if index != 2:
            self.calendar.back_to_calendar()
        if index != 0:
            self.organizer.goto_page(0)
        self.parent.page.update()

    def _get_content(self, page:ft.Page):

        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.TUNE,
                    selected_icon=ft.Icons.TUNE,
                    label="Organize",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.CONTENT_PASTE_OUTLINED,
                    selected_icon=ft.Icons.ASSIGNMENT,
                    label="Tasks",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.CALENDAR_TODAY_OUTLINED,
                    selected_icon=ft.Icons.CALENDAR_MONTH,
                    label="Calendar",
                ),
            ],
            selected_index=1,
            on_change=self._switch_page,
        )

        organize_content = self.organizer.get_content(page)
        tasks_content = self.tasks.get_content(page)
        calendar_content = self.calendar.get_content(page)
        
        organize_content.visible = False
        calendar_content.visible = False

        content = ft.Row(
            controls=[
                organize_content,
                tasks_content,
                calendar_content,
            ]
        )

        return content
