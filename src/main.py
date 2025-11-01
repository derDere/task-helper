

import flet as ft
from app import App


def main(page: ft.Page):
    app = App(page)
    app.start()


if __name__ == "__main__":
    ft.app(main)
