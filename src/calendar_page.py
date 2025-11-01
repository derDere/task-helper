

from datetime import datetime, timedelta
import flet as ft

from ui_base import UIBase
from task_manager import TaskManager


class Calendar(UIBase):

    def __init__(self, parent, task_manager: TaskManager):
        super().__init__(parent)
        self.task_manager = task_manager
        self.calendar_content = None
    
    def _day_content(self, day_date: datetime):
        date = day_date.strftime("%d.")
        task_count = len(self.task_manager.get_task_for_date(day_date.date()))
        return ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    spacing=5,
                    controls=[
                        ft.Text(
                            date,
                            size=14,
                            text_align=ft.TextAlign.LEFT,
                        ),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    expand=True,
                    spacing=5,
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                str(task_count),
                                size=12,
                                color=ft.Colors.ON_PRIMARY_CONTAINER,
                            ),
                            padding=ft.padding.symmetric(horizontal=10, vertical=5),
                            bgcolor=ft.Colors.PRIMARY_CONTAINER,
                            border_radius=ft.border_radius.all(20),
                            visible=(task_count > 0)
                        )
                    ]
                ),
            ]
        )
    
    def _generate_calendar(self):
        self.calendar_content.controls.clear()
        last_monday = datetime.now() - timedelta(days=datetime.now().weekday())

        week_day_row = ft.Row(
            expand=True,
            spacing=2
        )
        for i in range(7):
            day_date = last_monday + timedelta(days=i)
            day_name = day_date.strftime("%a")
            item = ft.Container(
                content = ft.Text(day_name, size=16, weight=ft.FontWeight.BOLD),
                padding=ft.padding.all(5),
                alignment=ft.alignment.center,
                expand=True,
                bgcolor=ft.Colors.PRIMARY_CONTAINER,
                border_radius=ft.border_radius.all(4)
            )
            week_day_row.controls.append(item)
        
        self.calendar_content.controls.append(week_day_row)

        for week in range(6):
            week_row = ft.Row(
                expand=True,
                spacing=2
            )
            for day in range(7):
                day_date = last_monday + timedelta(days=week*7 + day)
                is_current_month = (day_date.month == datetime.now().month)
                is_today = (day_date.date() == datetime.now().date())
                border = ft.border.all(1, ft.Colors.OUTLINE_VARIANT)
                if is_today:
                    border = ft.border.all(2, ft.Colors.PRIMARY)
                bg = ft.Colors.SURFACE_CONTAINER_HIGHEST if is_current_month else ft.Colors.SURFACE
                day_item = ft.Container(
                    content = self._day_content(day_date),
                    padding=ft.padding.all(10),
                    alignment=ft.alignment.top_center,
                    border=border,
                    expand=True,
                    height=80,
                    bgcolor=bg,
                    border_radius=ft.border_radius.all(4)
                )
                week_row.controls.append(day_item)
            self.calendar_content.controls.append(week_row)

    def _get_content(self, page:ft.Page):

        self.calendar_content = ft.Column(
            expand=True,
            spacing=2
        )
        
        self._generate_calendar()

        return self.calendar_content
