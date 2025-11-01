

import flet as ft

from ui_base import UIBase


class FrontPage(UIBase):

    def _get_content(self) -> ft.Control:
        return ft.Text("Hello, this is the Front Page!")
