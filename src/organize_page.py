

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


class TaskSortPage(UIBase):
    def __init__(self, parent, task_manager: TaskManager):
        super().__init__(parent)
        self.task_manager = task_manager
        self.start_btn = None
        self.top_tasks_container = None
        self.bottom_tasks_container = None
        self.sort_complete_text = None
        self.priorities = {}
    
    def _get_priority_key(self, task_a, task_b):
        tab = [task_a.id, task_b.id]
        tab.sort()
        return f"{tab[0]}_{tab[1]}"
    
    def _find_priority_recursively(self, task_a, task_b, visited=None, depth=0):
        # die genaue Priorität zwischen task_a und task_b ist in der Kombination eventuell noch nicht definiert
        # aber kann möglicherise ermittelt werden in dem man die beziehungen zu anderen Tasks untersucht
        # zum Beispiel wenn task_a > task_c und task_c > task_b dann ist task_a > task_b
        # diese funktion soll das rekursiv versuchen zu ermitteln und falls ja einen key, value tupple zurückgeben
        # oder none wenn nicht möglich
        
        # Prevent excessive recursion depth
        MAX_DEPTH = 30
        if depth > MAX_DEPTH:
            print(f"[RECURSIVE] Max recursion depth {MAX_DEPTH} reached, stopping")
            return None
        
        print(f"[RECURSIVE] Depth {depth}: Checking priority between '{task_a.title}' and '{task_b.title}'")
        
        if visited is None:
            visited = set()
            print(f"[RECURSIVE] Starting new recursive search, visited set initialized")
        
        # Avoid infinite loops - use normalized key
        pair_key = self._get_priority_key(task_a, task_b)
        print(f"[RECURSIVE] Pair key: {pair_key}")
        
        if pair_key in visited:
            print(f"[RECURSIVE] Already visited {pair_key}, avoiding infinite loop")
            return None
        visited.add(pair_key)
        print(f"[RECURSIVE] Added {pair_key} to visited set, size now: {len(visited)}")
        
        # Check direct relationship
        if pair_key in self.priorities:
            print(f"[RECURSIVE] Found direct relationship: {pair_key} -> {self.priorities[pair_key]}")
            return (pair_key, self.priorities[pair_key])
        
        # Only check direct transitive relationships (no deep recursion)
        # This prevents infinite loops while still finding simple A>C>B relationships
        all_tasks = [t for t in self.task_manager.get_all_tasks() if not t.completed]
        print(f"[RECURSIVE] Checking {len(all_tasks)} incomplete tasks for direct transitive relationships")
        
        for i, intermediate_task in enumerate(all_tasks):
            if intermediate_task.id == task_a.id or intermediate_task.id == task_b.id:
                continue
            
            # Check if task_a > intermediate_task and intermediate_task > task_b
            key_a_to_c = self._get_priority_key(task_a, intermediate_task)
            key_c_to_b = self._get_priority_key(intermediate_task, task_b)
            
            if (key_a_to_c in self.priorities and self.priorities[key_a_to_c] == task_a.id and
                key_c_to_b in self.priorities and self.priorities[key_c_to_b] == intermediate_task.id):
                print(f"[RECURSIVE] Found transitive relationship: {task_a.title} > {intermediate_task.title} > {task_b.title}")
                return (pair_key, task_a.id)
            
            # Check if task_b > intermediate_task and intermediate_task > task_a
            key_b_to_c = self._get_priority_key(task_b, intermediate_task)
            key_c_to_a = self._get_priority_key(intermediate_task, task_a)
            
            if (key_b_to_c in self.priorities and self.priorities[key_b_to_c] == task_b.id and
                key_c_to_a in self.priorities and self.priorities[key_c_to_a] == intermediate_task.id):
                print(f"[RECURSIVE] Found reverse transitive relationship: {task_b.title} > {intermediate_task.title} > {task_a.title}")
                return (pair_key, task_b.id)
        
        print(f"[RECURSIVE] No priority relationship found between '{task_a.title}' and '{task_b.title}'")
        return None

    def _sort(self):
        # basically bubble sort but to compare we will find f"{task_a.id}_{task_b.id}" in priorities to find the better tast.id
        # if not found we will call _pause_sorting_on(task_a, task_b) and stop the sorting until user provides input
        # after the input the _sort will be called again

        if not self._validate_sorting_priority():
            print("Priority relationships contain cycles, cannot sort.")
            self.parent.page.open(ft.SnackBar(
                ft.Text("Priority relationships contain cycles. Please adjust your choices."),
                bgcolor=ft.Colors.ERROR_CONTAINER
            ))
            self.stop_sorting()
            return

        changed = True
        while changed:
            changed = False
            tasks = [t for t in self.task_manager.get_all_tasks() if not t.completed]
            for i in range(len(tasks) - 1):
                task_a = tasks[i]
                task_b = tasks[i + 1]
                pair_key = self._get_priority_key(task_a, task_b)
                better_task_id = None

                print("Checking priority between:", task_a.title, "and", task_b.title)
                
                if pair_key in self.priorities:
                    print("Found direct priority:", self.priorities[pair_key])
                    better_task_id = self.priorities[pair_key]
                elif len(self.priorities) > 0:
                    # Try to find priority recursively
                    print("No direct priority found, trying recursive search...")
                    recursive_result = self._find_priority_recursively(task_a, task_b)
                    print("Recursive search result:", recursive_result)
                    if recursive_result:
                        print("Found recursive priority:", recursive_result)
                        # Cache the found relationship
                        self.priorities[recursive_result[0]] = recursive_result[1]
                        better_task_id = recursive_result[1]
                
                if better_task_id:
                    print("Better task determined:", better_task_id)
                    if better_task_id == task_b.id:
                        print("Swapping tasks:", task_a.title, "<->", task_b.title)
                        # swap
                        tasks[i], tasks[i + 1] = tasks[i + 1], tasks[i]
                        changed = True
                else:
                    print("No priority found, pausing sorting for user input.")
                    self._pause_sorting_on(task_a, task_b)
                    return  # exit sorting until user input
        
        # Apply new priorities to the task manager
        self._apply_sorted_order_to_task_manager()
        self._sorting_completed()
    
    def _validate_sorting_priority(self):
        # make sure that the priorities dont contain any loops that would make sorting impossible
        # for example task_a > task_b, task_b > task_c, task_c > task_a
        
        all_tasks = self.task_manager.get_all_tasks()
        task_ids = [task.id for task in all_tasks]
        
        # Build adjacency graph from priorities
        graph = {task_id: [] for task_id in task_ids}
        
        for pair_key, better_task_id in self.priorities.items():
            task_a_id, task_b_id = pair_key.split('_', 1)
            if better_task_id == task_a_id:
                # task_a > task_b, so add edge from task_a to task_b
                if task_a_id in graph and task_b_id in task_ids:
                    graph[task_a_id].append(task_b_id)
            elif better_task_id == task_b_id:
                # task_b > task_a, so add edge from task_b to task_a
                if task_b_id in graph and task_a_id in task_ids:
                    graph[task_b_id].append(task_a_id)
        
        # Detect cycles using DFS
        visited = set()
        rec_stack = set()
        
        def has_cycle_dfs(node):
            if node in rec_stack:
                return True  # Back edge found - cycle detected
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if has_cycle_dfs(neighbor):
                    return True
            
            rec_stack.remove(node)
            return False
        
        # Check all nodes for cycles
        for task_id in task_ids:
            if task_id not in visited:
                if has_cycle_dfs(task_id):
                    return False  # Cycle detected
        
        return True  # No cycles found
    
    def _apply_sorted_order_to_task_manager(self):
        # Apply the sorted order to the task manager's importance values
        # Tasks are already sorted in the correct order by the bubble sort
        tasks = self.task_manager.get_all_tasks()
        
        # Set importance values in descending order (highest priority = highest importance)
        # The first task in the sorted list gets the highest importance
        for index, task in enumerate(tasks):
            # Assign importance in reverse order: first task gets highest value
            new_importance = len(tasks) - index
            task.importance = new_importance
        
        # Save the updated importance values
        self.task_manager.trigger_save()
    
    def _start_sorting(self, e):
        self.start_btn.visible = False
        self.priorities = {}
        self.sort_complete_text.visible = False
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
        pair_key = self._get_priority_key(task_a, task_b)
        self.priorities[pair_key] = task_a.id
        
        # Validate priorities for cycles
        if not self._validate_sorting_priority():
            # Remove the problematic priority and show error
            del self.priorities[pair_key]
            self.parent.page.open(ft.SnackBar(
                ft.Text("This choice would create a cycle in priorities. Please choose differently."),
                bgcolor=ft.Colors.ERROR_CONTAINER
            ))
            return
        
        self.top_tasks_container.visible = False
        self.top_tasks_container.content = None
        self.bottom_tasks_container.visible = False
        self.bottom_tasks_container.content = None
        self.parent.page.update()
        self._sort()
    
    def _bottom_task_selected(self, e):
        task_a, task_b = self.bottom_tasks_container.data
        pair_key = self._get_priority_key(task_a, task_b)
        self.priorities[pair_key] = task_b.id
        
        # Validate priorities for cycles
        if not self._validate_sorting_priority():
            # Remove the problematic priority and show error
            del self.priorities[pair_key]
            self.parent.page.open(ft.SnackBar(
                ft.Text("This choice would create a cycle in priorities. Please choose differently."),
                bgcolor=ft.Colors.ERROR_CONTAINER
            ))
            return
        
        self.top_tasks_container.visible = False
        self.top_tasks_container.content = None
        self.bottom_tasks_container.visible = False
        self.bottom_tasks_container.content = None
        self.parent.page.update()
        self._sort()

    def stop_sorting(self):
        self.top_tasks_container.visible = False
        self.top_tasks_container.content = None
        self.bottom_tasks_container.visible = False
        self.bottom_tasks_container.content = None
        self.start_btn.visible = True
        self.sort_complete_text.visible = False
        self.priorities = {}
        self.parent.page.update()

    def _sorting_completed(self):
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
