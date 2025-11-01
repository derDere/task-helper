

import flet as ft

from ui_base import UIBase


class Tasks(UIBase):

    def __init__(self, parent):
        super().__init__(parent)

    def _get_content(self, page:ft.Page):
        content = ft.Column(
            controls=[
                ft.Text("This is the Tasks Page"),
            ]
        )

        return content
