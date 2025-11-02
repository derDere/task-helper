

import flet as ft
import math
import random

from ui_base import UIBase
from task_manager import TaskManager, Task


def estimated_comparisons(n: int) -> int:
    """
    Returns the theoretical minimum number of comparisons
    needed to fully sort n items (O(n log₂ n) estimate).
    """
    if n <= 1:
        return 0
    return int(n * math.log2(n))


class TaskItem:
    def __init__(self, task: Task, tast_manager: TaskManager, page: ft.Page, parent):
        self.parent = parent
        self.task = task
        self.task_manager = tast_manager
        self.page = page
        self.edit_button = None
        self.delete_button = None
        self.confirm_delete_btn = None
        self.cancel_delete_btn = None
        self.date_picker_btn = None
        self.date_del_btn = None
        self.date_picker = None
        self.completet_at_text = None
        self.item = None
        self.title_txb = None
        self.description_txb = None
        self.edit_dialog = None
    
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
    
    def _edit_task_dialog(self, e):
        self.title_txb.value = self.task.title
        self.description_txb.value = self.task.description
        self.page.open(self.edit_dialog)

    def _save_task_edits(self, e):
        self.task.title = self.title_txb.value
        self.task.description = self.description_txb.value
        self.task_manager.trigger_save()
        self.item.content.controls[0].controls[1].value = self.task.title
        self.item.content.controls[1].value = self.task.description
        self.page.close(self.edit_dialog)
        self.page.update()
    
    def get_item(self):
        self.title_txb = ft.TextField(
            value=self.task.title,
            label="Title",
            width=300
        )
        self.description_txb = ft.TextField(
            value=self.task.description,
            label="Description",
            width=300,
            multiline=True,
            max_lines=5
        )
        self.edit_dialog = ft.AlertDialog(
            title=ft.Text("Edit Task"),
            content=ft.Column(
                controls=[
                    self.title_txb,
                    self.description_txb
                ]
            ),
            actions=[
                ft.TextButton(
                    text="Cancel",
                    on_click=lambda e: self.page.close(self.edit_dialog)
                ),
                ft.ElevatedButton(
                    text="Save",
                    on_click=self._save_task_edits
                )
            ]
        )
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
        self.edit_button = ft.IconButton(
            icon=ft.Icons.EDIT,
            on_click=self._edit_task_dialog
        )
        self.item = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            self.edit_button,
                            ft.Text(self.task.title, style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)),
                            ft.Text(f"ELO: {self.task.elo}", style=ft.TextStyle(size=14, color=ft.Colors.ON_SURFACE_VARIANT)),
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


class TaskSortPage(UIBase):
    def __init__(self, parent, task_manager: TaskManager):
        super().__init__(parent)
        self.task_manager = task_manager
        self.start_btn = None
        self.top_tasks_container = None
        self.bottom_tasks_container = None
        self.sort_complete_text = None
        self.progess_bar = None
        self.priorities = {}
        self.K = 32  # Lernrate; kleiner = stabiler, größer = schneller
        self._max_rounds = 50      # maximale Vergleichsanzahl pro Session
        self._rounds_done = 0
    
    def _get_pair_key(self, task_a, task_b):
        tab = [task_a.id, task_b.id]
        tab.sort()
        return f"{tab[0]}_{tab[1]}"

    def _expected_score(self, rating_a, rating_b):
        """Berechnet erwarteten Sieganteil nach Elo-Formel."""
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def _update_elo(self, winner, loser):
        """Aktualisiert Elo-Werte basierend auf Sieg und Niederlage."""
        expected_winner = self._expected_score(winner.new_elo, loser.new_elo)
        expected_loser = self._expected_score(loser.new_elo, winner.new_elo)

        winner.new_elo += self.K * (1 - expected_winner)
        loser.new_elo += self.K * (0 - expected_loser)

    def _reset_elos(self):
        """Setzt alle Tasks auf Startwert zurück."""
        for t in self.task_manager.get_all_tasks():
            t.new_elo = 1000

    def _sort(self):
        """Startet oder setzt den Sortiervorgang fort."""
        tasks = [t for t in self.task_manager.get_all_tasks() if not t.completed]

        # Ende erreicht?
        if self._rounds_done >= self._max_rounds:
            self._apply_sorted_order_to_task_manager()
            self._sorting_completed()
            return

        # Wähle zwei Tasks für den nächsten Vergleich
        task_a, task_b = self._select_next_pair(tasks)
        if task_a is None or task_b is None:
            # Nichts mehr zu vergleichen
            self._apply_sorted_order_to_task_manager()
            self._sorting_completed()
            return

        pair_key = self._get_pair_key(task_a, task_b)

        if pair_key in self.priorities:
            # Ergebnis bekannt → automatisch Elo anwenden
            self._rounds_done += 1
            self._update_progress_bar()
            self._sort()
            return

        # Kein Ergebnis bekannt → User soll entscheiden
        self._pause_sorting_on(task_a, task_b)
    
    def _select_next_pair(self, tasks):
        """Wählt das nächste Paar für Vergleich.
           Priorisiert ähnliche Elo-Werte, vermeidet Wiederholungen.
        """
        untested = []
        for i, a in enumerate(tasks):
            for b in tasks[i + 1:]:
                pair_key = self._get_pair_key(a, b)
                if pair_key not in self.priorities:
                    untested.append((a, b))

        if not untested:
            return None, None

        # Wähle Paar mit minimalem Elo-Abstand, um "spannende" Vergleiche zu zeigen
        untested.sort(key=lambda p: abs(p[0].new_elo - p[1].new_elo))
        # zufällige Auswahl aus den ähnlichsten 20 %
        top_n = max(1, len(untested) // 5)
        return random.choice(untested[:top_n])
    
    def _apply_sorted_order_to_task_manager(self):
        for task in self.task_manager.get_all_tasks():
            # Assign the new Elo value calculated during sorting
            task.elo = round(task.new_elo)
        
        # Save the updated importance values
        self.task_manager.trigger_save()
    
    def _update_progress_bar(self):
        progress = self._rounds_done / self._max_rounds
        self.progess_bar.value = progress
        self.parent.page.update()
    
    def _start_sorting(self, e):
        self.progess_bar.visible = True
        self.start_btn.visible = False
        self.priorities = {}
        self.sort_complete_text.visible = False
        self.priorities = {}
        self._rounds_done = 0
        self._update_progress_bar()
        self._max_rounds = estimated_comparisons(len([t for t in self.task_manager.get_all_tasks() if not t.completed]))
        self._reset_elos()
        self.parent.page.update()
        self._sort()

    def _pause_sorting_on(self, task_a, task_b):
        self.top_tasks_container.data = (task_a, task_b)
        self.top_tasks_container.content = ft.Column(
            controls=[
                ft.Text(task_a.title, style=ft.TextStyle(size=16)),
                ft.Text(task_a.description, style=ft.TextStyle(size=14, color=ft.Colors.ON_SURFACE_VARIANT))
            ]
        )
        self.top_tasks_container.visible = True

        self.bottom_tasks_container.data = (task_a, task_b)
        self.bottom_tasks_container.content = ft.Column(
            controls=[
                ft.Text(task_b.title, style=ft.TextStyle(size=16)),
                ft.Text(task_b.description, style=ft.TextStyle(size=14, color=ft.Colors.ON_SURFACE_VARIANT))
            ]
        )
        self.bottom_tasks_container.visible = True

        self.parent.page.update()
    
    def _top_task_selected(self, e):
        task_a, task_b = self.top_tasks_container.data
        pair_key = self._get_pair_key(task_a, task_b)
        self.priorities[pair_key] = task_a.id
        self._update_elo(task_a, task_b)
        self._rounds_done += 1
        self._update_progress_bar()
        
        self.top_tasks_container.visible = False
        self.top_tasks_container.content = None
        self.bottom_tasks_container.visible = False
        self.bottom_tasks_container.content = None
        self.parent.page.update()
        self._sort()
    
    def _bottom_task_selected(self, e):
        task_a, task_b = self.bottom_tasks_container.data
        pair_key = self._get_pair_key(task_a, task_b)
        self.priorities[pair_key] = task_b.id
        self._update_elo(task_b, task_a)
        self._rounds_done += 1
        self._update_progress_bar()
        
        self.top_tasks_container.visible = False
        self.top_tasks_container.content = None
        self.bottom_tasks_container.visible = False
        self.bottom_tasks_container.content = None
        self.parent.page.update()
        self._sort()

    def stop_sorting(self):
        self.progess_bar.visible = False
        self.top_tasks_container.visible = False
        self.top_tasks_container.content = None
        self.bottom_tasks_container.visible = False
        self.bottom_tasks_container.content = None
        self.start_btn.visible = True
        self.sort_complete_text.visible = False
        self.priorities = {}
        self.parent.page.update()

    def _sorting_completed(self):
        self.progess_bar.visible = False
        self.top_tasks_container.visible = False
        self.top_tasks_container.content = None
        self.bottom_tasks_container.visible = False
        self.bottom_tasks_container.content = None
        self.sort_complete_text.visible = True
        self.start_btn.visible = True
        self.parent.page.update()
    
    def _get_content(self, page:ft.Page):

        self.start_btn = ft.ElevatedButton(
            text="Start Sorting Tasks",
            on_click=self._start_sorting
        )

        self.top_tasks_container = ft.Container(
            visible=False,
            on_click=self._top_task_selected,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            width=400,
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.Colors.SECONDARY),
            border_radius=ft.border_radius.all(4)
        )

        self.bottom_tasks_container = ft.Container(
            visible=False,
            on_click=self._bottom_task_selected,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            width=400,
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.Colors.SECONDARY),
            border_radius=ft.border_radius.all(4)
        )

        self.sort_complete_text = ft.Text(
            "Sorting Complete!",
            style=ft.TextStyle(size=16, color=ft.Colors.GREEN),
            visible=False
        )

        self.progess_bar = ft.ProgressBar(
            width=400,
            visible=False
        )

        content = ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("Sort Tasks by Importance", style=ft.TextStyle(size=20)),
                    self.start_btn,
                    self.progess_bar,
                    self.sort_complete_text,
                    self.top_tasks_container,
                    self.bottom_tasks_container
                ]
            )
        )

        return content


class Organizer(UIBase):

    def __init__(self, parent, task_manager: TaskManager):
        super().__init__(parent)
        self.task_manager = task_manager
        self.drawer = None
        self.task_sort_page = TaskSortPage(parent, task_manager)

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
        # if drawer is in page
        if self.drawer.open:
            self.drawer.selected_index = index
            self.parent.page.close(self.drawer)

        self.new_task_content.visible = (index == 0)
        self.sort_tasks_content.visible = (index == 1)
        self.recently_completed_content.visible = (index == 2)
        self.all_tasks_content.visible = (index == 3)

        if index == 2:
            self._load_recently_completed()
        else:
            self._unload_recently_completed()

        if index == 3:
            self._load_all_tasks()
        else:
            self._unload_all_tasks()
        
        if index != 1:
            self.task_sort_page.stop_sorting()

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

        self.sort_tasks_content = self.task_sort_page.get_content(page)
        self.sort_tasks_content.visible = False

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
