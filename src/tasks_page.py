

import flet as ft

from ui_base import UIBase
from task_manager import TaskManager


class Tasks(UIBase):

    def __init__(self, parent, task_manager: TaskManager):
        super().__init__(parent)
        self.task_manager = task_manager
        self.tast_column = None
    
    def _update_task_list(self):
        tasks = self.task_manager.get_top_priority_tasks()
        self.tast_column.controls.clear()
        if len(tasks) == 0:
            self.tast_column.controls.append(
                ft.Text("No upcoming tasks!", style=ft.TextThemeStyle.BODY_MEDIUM)
            )
        else:
            for task in tasks:
                card = self._task_to_card(task)
                self.tast_column.controls.append(card)

    def _task_to_card(self, task):
        card = ft.Card(
            width=400,
            content=ft.Container(
                padding=ft.padding.all(10),
                content=ft.Row(
                    controls=[
                        ft.Column(
                            expand=True,
                            controls=[
                                ft.Text(
                                    task.title,
                                    style=ft.TextThemeStyle.HEADLINE_SMALL,
                                    color=ft.Colors.PRIMARY,
                                ),
                                ft.Text(
                                    task.description,
                                    style=ft.TextThemeStyle.BODY_MEDIUM
                                ),
                                ft.Text(
                                    f"{task.due_date}",
                                    style=ft.TextThemeStyle.BODY_SMALL,
                                    text_align=ft.TextAlign.RIGHT,
                                    color=ft.Colors.SECONDARY,
                                ),
                            ]
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CIRCLE_OUTLINED,
                            icon_color=ft.Colors.PRIMARY,
                            icon_size=40,
                            tooltip="Done",
                            on_click=lambda e: 1,
                        )
                    ]
                )
            ),
            margin=ft.margin.all(5),
        )
        return card

    def _get_content(self, page:ft.Page):

        self.tast_column = ft.Column(
            spacing=20,
            expand=False
        )

        content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            controls=[
                ft.Text("Next Tasks", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                ft.Text("Here are your upcoming tasks:", style=ft.TextThemeStyle.BODY_MEDIUM),
                self.tast_column,
            ],
        )

        self._update_task_list()

        self.task_manager.on_tasks_updated(self._update_task_list)

        return content
