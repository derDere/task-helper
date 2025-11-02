

from datetime import datetime, timedelta, date
import flet as ft

from ui_base import UIBase
from task_manager import TaskManager


class Calendar(UIBase):

    def __init__(self, parent, task_manager: TaskManager):
        super().__init__(parent)
        self.task_manager = task_manager
        self.calendar_content = None
        self.day_content = None
    
    def _day_content(self, day_date: datetime):
        date = day_date.strftime("%d.")
        tasks = self.task_manager.get_task_for_date(day_date.date())
        task_count = len(tasks)
        tast_done_count = len([t for t in tasks if t.completed])
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
                                f"{tast_done_count}/{task_count}",
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
                    border_radius=ft.border_radius.all(4),
                    data=day_date,
                    on_click=lambda e: self._show_day_tasks(e.control.data)
                )
                week_row.controls.append(day_item)
            self.calendar_content.controls.append(week_row)
    
    def back_to_calendar(self):
        self.day_content.visible = False
        self.calendar_content.visible = True
        self.parent.page.update()
    
    def _show_day_tasks(self, day_date: date|datetime):
        self.day_content.controls.clear()
        if isinstance(day_date, datetime):
            day_date = day_date.date()
        tasks = self.task_manager.get_task_for_date(day_date)
        if len(tasks) == 0:
            return

        top = ft.Row(
            expand=True,
            controls=[
                ft.Text(
                    day_date.strftime('%a: %d.%m.%Y'),
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.PRIMARY,
                    expand=True
                ),
                ft.FilledButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ARROW_BACK),
                            ft.Text("Back"),
                            ft.Icon(ft.Icons.CALENDAR_MONTH),
                        ]
                    ),
                    tooltip="Back to Calendar",
                    on_click=lambda e: self.back_to_calendar()
                )
            ]
        )

        self.day_content.controls.append(top)

        for task in tasks:
            task_item = ft.Container(
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=True,
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    task.title,
                                    size=16,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Text(
                                    task.description,
                                    size=14,
                                    color=ft.Colors.ON_SURFACE_VARIANT
                                )
                            ]
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CIRCLE_OUTLINED if not task.completed else ft.Icons.CHECK_CIRCLE,
                            icon_color=ft.Colors.PRIMARY if not task.completed else ft.Colors.GREEN,
                            icon_size=40,
                            tooltip="Completed" if task.completed else "Uncompleted",
                            data=task,
                            on_click=self._task_icon_click,
                        )
                    ]
                ),
                padding=ft.padding.all(10),
                margin=ft.margin.only(bottom=5),
                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                border_radius=ft.border_radius.all(4),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
            )
            self.day_content.controls.append(task_item)
        
        self.calendar_content.visible = False
        self.day_content.visible = True
        self.parent.page.update()
    
    def _task_icon_click(self, e):
        task = e.control.data
        if task.completed:
            self.task_manager.undo_task(task)
        else:
            self.task_manager.complete_task(task)
        e.control.icon = ft.Icons.CIRCLE_OUTLINED if not task.completed else ft.Icons.CHECK_CIRCLE
        e.control.icon_color = ft.Colors.PRIMARY if not task.completed else ft.Colors.GREEN
        e.control.tooltip = "Completed" if task.completed else "Uncompleted"
        self.parent.page.update()

    def _get_content(self, page:ft.Page):

        self.day_content = ft.Column(
            expand=True,
            spacing=20,
            visible=False
        )

        self.calendar_content = ft.Column(
            expand=True,
            spacing=2
        )
        
        self._generate_calendar()

        content = ft.Column(
            expand=True,
            controls=[
                self.calendar_content,
                self.day_content
            ]
        )

        self.task_manager.on_tasks_updated(self._generate_calendar)

        return content
