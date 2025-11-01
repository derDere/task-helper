

import flet as ft

from ui_base import UIBase


class Calendar(UIBase):

    def __init__(self, parent):
        super().__init__(parent)

    def _get_content(self, page:ft.Page):
        content = ft.Column(
            controls=[
                ft.Text("This is the Calendar Page"),
            ]
        )

        return content
