

import flet as ft

from ui_base import UIBase
from task_manager import TaskManager, Task


class TaskItem:
    def __init__(self, task: Task, tast_manager: TaskManager, page: ft.Page, parent):
        self.parent = parent
        self.task = task
        self.task_manager = tast_manager
        self.page = page
        self.delete_button = None
        self.confirm_delete_btn = None
        self.cancel_delete_btn = None
        self.date_picker_btn = None
        self.date_del_btn = None
        self.date_picker = None
        self.completet_at_text = None
        self.item = None
    
    def _delete_due_date(self, e):
        self.task.due_date = None
        self.date_picker_btn.text = "No Due Date"
        self.date_del_btn.visible = False
        self.page.update()
        self.task_manager.trigger_save()
    
    def _date_picker_changed(self, e):
        new_date = e.control.value
        self.task.due_date = new_date.date() if new_date else None
        due_date_text = f"Due: {self.task.due_date.strftime('%Y-%m-%d')}" if self.task.due_date else "No Due Date"
        self.date_picker_btn.text = due_date_text
        self.date_del_btn.visible = self.task.due_date is not None
        self.page.update()
        self.task_manager.trigger_save()
    
    def _delete_btn_click(self, e):
        self.delete_button.visible = False
        self.confirm_delete_btn.visible = True
        self.cancel_delete_btn.visible = True
        self.page.update()
    
    def _cancel_delete_click(self, e):
        self.delete_button.visible = True
        self.confirm_delete_btn.visible = False
        self.cancel_delete_btn.visible = False
        self.page.update()
    
    def _delete_confirmed(self, e):
        self.task_manager.remove_task(self.task)
        self.parent.controls.remove(self.item)
        self.page.update()
    
    def _toggle_task_completion(self, e):
        task = e.control.data
        if task.completed:
            self.task_manager.undo_task(task)
        else:
            self.task_manager.complete_task(task)
        btn = e.control
        btn.icon=ft.Icons.CHECK_CIRCLE if task.completed else ft.Icons.CIRCLE_OUTLINED
        btn.text="Done" if task.completed else "To Do"
        btn.icon_color=ft.Colors.GREEN if task.completed else ft.Colors.PRIMARY
        self.completet_at_text.value = f"Completed: {task.completed_at.strftime('%Y-%m-%d %H:%M')}" if task.completed and task.completed_at else ""
        self.page.update()
    
    def get_item(self):
        self.date_picker = ft.DatePicker(
            value=self.task.due_date,
            on_change=self._date_picker_changed
        )
        self.date_picker_btn = ft.TextButton(
            text=f"Due: {self.task.due_date.strftime('%Y-%m-%d')}" if self.task.due_date else "No Due Date",
            on_click=lambda e: self.page.open(self.date_picker)
        )
        self.date_del_btn = ft.IconButton(
            tooltip="Remove Due Date",
            icon=ft.Icons.DELETE,
            icon_color=ft.Colors.ERROR,
            on_click=self._delete_due_date,
            visible=self.task.due_date is not None
        )
        self.delete_button = ft.OutlinedButton(
            icon=ft.Icons.DELETE,
            text="Delete",
            icon_color=ft.Colors.ERROR,
            on_click=self._delete_btn_click
        )
        self.confirm_delete_btn = ft.OutlinedButton(
            icon=ft.Icons.DELETE,
            text="Yes Delete!",
            icon_color=ft.Colors.ERROR,
            data=self.task,
            on_click=self._delete_confirmed,
            visible=False
        )
        self.cancel_delete_btn = ft.OutlinedButton(
            icon=ft.Icons.CLOSE,
            text="Cancel",
            visible=False,
            on_click=self._cancel_delete_click
        )
        self.completet_at_text = ft.Text(
            f"Completed: {self.task.completed_at.strftime('%Y-%m-%d %H:%M')}" if self.task.completed and self.task.completed_at else "",
            style=ft.TextStyle(size=12, color=ft.Colors.ON_SURFACE_VARIANT)
        )
        self.item = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(self.task.title, style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)),
                            ft.Container(expand=True),
                            self.date_del_btn,
                            self.date_picker_btn
                        ]
                    ),
                    ft.Text(self.task.description, style=ft.TextStyle(size=14)),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            self.completet_at_text,
                            ft.Container(expand=True),
                            self.confirm_delete_btn,
                            self.cancel_delete_btn,
                            self.delete_button,
                            ft.OutlinedButton(
                                icon=ft.Icons.CHECK_CIRCLE if self.task.completed else ft.Icons.CIRCLE_OUTLINED,
                                text="Done" if self.task.completed else "To Do",
                                icon_color=ft.Colors.GREEN if self.task.completed else ft.Colors.PRIMARY,
                                data=self.task,
                                on_click=self._toggle_task_completion
                            )
                        ]
                    ),
                    ft.Divider()
                ]
            ),
            padding=ft.padding.all(10)
        )
        return self.item

class Organizer(UIBase):

    def __init__(self, parent, task_manager: TaskManager):
        super().__init__(parent)
        self.task_manager = task_manager
        self.drawer = None

        self.new_task_content = None
        self.sort_tasks_content = None
        self.recently_completed_content = None
        self.all_tasks_content = None

        self.title_txb = None
        self.description_txb = None
        self.due_date_button = None
        self.new_due_date = None
        self.due_date_picker = None
        self.delete_due_date_btn = None
    
    def _nav_drawer_changed(self, e):
        selected_index = e.control.selected_index
        self.goto_page(selected_index)
    
    def goto_page(self, index: int):
        self.drawer.selected_index = index

        self.new_task_content.visible = (index == 0)
        self.sort_tasks_content.visible = (index == 1)
        self.recently_completed_content.visible = (index == 2)
        self.all_tasks_content.visible = (index == 3)

        self.parent.page.close(self.drawer)

        if index == 2:
            self._load_recently_completed()
        else:
            self._unload_recently_completed()

        if index == 3:
            self._load_all_tasks()
        else:
            self._unload_all_tasks()

        self.parent.page.update()

    def _load_all_tasks(self):
        self.all_tasks_content.controls.clear()
        tasks = self.task_manager.get_all_tasks()

        if not tasks:
            self.all_tasks_content.controls.append(
                ft.Text("No tasks available.", style=ft.TextStyle(size=16, color=ft.Colors.ON_SURFACE_VARIANT))
            )
            self.parent.page.update()

        for task in tasks:
            item_obj = TaskItem(task, self.task_manager, self.parent.page, self.all_tasks_content)
            item = item_obj.get_item()
            self.all_tasks_content.controls.append(item)
        
        self.parent.page.update()

    def _unload_all_tasks(self):
        self.all_tasks_content.controls.clear()
        self.parent.page.update()
    
    def _load_recently_completed(self):
        self.recently_completed_content.controls.clear()
        tasks = self.task_manager.get_last_completed()

        if not tasks:
            self.recently_completed_content.controls.append(
                ft.Text("No recently completed tasks.", style=ft.TextStyle(size=16, color=ft.Colors.ON_SURFACE_VARIANT))
            )
            self.parent.page.update()

        for task in tasks:
            item_obj = TaskItem(task, self.task_manager, self.parent.page, self.recently_completed_content)
            item = item_obj.get_item()
            self.recently_completed_content.controls.append(item)
        
        self.parent.page.update()
    
    def _unload_recently_completed(self):
        self.recently_completed_content.controls.clear()
        self.parent.page.update()
    
    def _open_due_date_picker(self, e):
        self.parent.page.open(self.due_date_picker)
    
    def _update_due_date_ui(self):
        if self.new_due_date != None:
            self.due_date_button.text = f"Due: {self.new_due_date.strftime('%Y-%m-%d')}"
            self.delete_due_date_btn.visible = True
        else:
            self.due_date_button.text = "Due: None"
            self.delete_due_date_btn.visible = False
        self.parent.page.update()
    
    def _on_delete_due_date(self, e):
        self.new_due_date = None
        self._update_due_date_ui()
    
    def _on_due_date_selected(self, e):
        self.new_due_date = e.control.value
        self._update_due_date_ui()
    
    def _on_add_task_clicked(self, e):
        title = self.title_txb.value.strip()
        description = self.description_txb.value

        if not title:
            error_snack = ft.SnackBar(
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.WARNING, color=ft.Colors.ON_ERROR_CONTAINER),
                        ft.Text(
                            value="Task title cannot be empty.",
                            style=ft.TextStyle(color=ft.Colors.ON_ERROR_CONTAINER)
                        )
                    ],
                    spacing=10
                ),
                bgcolor=ft.Colors.ERROR_CONTAINER
            )
            self.parent.page.open(error_snack)
            return

        new_task = Task(
            title=title,
            description=description
        )
        if self.new_due_date:
            new_task.due_date = self.new_due_date.date()
        self.task_manager.add_task(new_task)

        self.title_txb.value = ""
        self.description_txb.value = ""
        self.new_due_date = None
        self._update_due_date_ui()

        self.parent.page.open(ft.SnackBar(ft.Text("Task added successfully!")))

    def _get_content(self, page:ft.Page):

        self.drawer = ft.NavigationDrawer(
            on_change=self._nav_drawer_changed,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.ADD,
                    label="Add Task"
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.SWAP_VERT,
                    label="Sort Tasks"
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.CHECK,
                    label="Recently Completed"
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.CHECKLIST,
                    label="All Tasks"
                )
            ]
        )

        menu_btn = ft.IconButton(
            icon=ft.Icons.MENU,
            on_click=lambda e: page.open(self.drawer)
        )

        self.due_date_button = ft.OutlinedButton(
            text="Due: None",
            width=300,
            on_click=self._open_due_date_picker
        )

        self.due_date_picker = ft.DatePicker(
            on_change=self._on_due_date_selected
        )

        self.delete_due_date_btn = ft.OutlinedButton(
            text="Remove Due Date",
            icon=ft.Icons.DELETE,
            width=300,
            icon_color=ft.Colors.ERROR,
            on_click=self._on_delete_due_date,
            visible=False
        )

        self.title_txb = ft.TextField(label="Task Title", width=300, bgcolor=ft.Colors.PRIMARY_CONTAINER)
        self.description_txb = ft.TextField(label="Task Description", width=300, multiline=True, bgcolor=ft.Colors.PRIMARY_CONTAINER)

        self.new_task_content = ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("Add New Task", style=ft.TextStyle(size=20)),
                    self.title_txb,
                    self.description_txb,
                    self.due_date_button,
                    self.delete_due_date_btn,
                    ft.Divider(),
                    ft.ElevatedButton(text="Add Task", width=150, on_click=self._on_add_task_clicked)
                ]
            )
        )

        self.sort_tasks_content = ft.Container(
            visible=False
        )

        self.recently_completed_content = ft.Column(
            expand=True,
            visible=False
        )

        self.all_tasks_content = ft.Column(
            expand=True,
            visible=False
        )

        content = ft.Column(
            expand=True,
            controls=[
                menu_btn,
                self.new_task_content,
                self.sort_tasks_content,
                self.recently_completed_content,
                self.all_tasks_content
            ]
        )

        return content
