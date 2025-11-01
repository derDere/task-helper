

import flet as ft

from ui_base import UIBase
from task_manager import TaskManager


class Tasks(UIBase):

    def __init__(self, parent, task_manager: TaskManager):
        super().__init__(parent)
        self.task_manager = task_manager

    def _get_content(self, page:ft.Page):
        content = ft.Column(
            controls=[
                ft.Text("This is the Tasks Page"),
            ]
        )

        return content
