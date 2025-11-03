

from datetime import date, datetime
import json
import random


STORAGE_KEY = "stored_tasks"


def uuid4():
    return ''.join([hex(random.randint(0, 15))[2:] for _ in range(32)])


class Task:
    def __init__(self, title: str, description: str, due_date: date|None = None, completed: bool = False, elo: int = 1000):
        self.id = uuid4()
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed
        self.completed_at = None
        self.elo = elo
        self.new_elo = 1000 # not saved, used for temporary calculations

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed": self.completed,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "elo": self.elo,
        }

    @staticmethod
    def from_dict(data: dict):
        # Parse due_date from string to date object if it exists
        due_date = None
        if data.get("due_date"):
            try:
                due_date = datetime.fromisoformat(data["due_date"]).date()
            except (ValueError, TypeError):
                due_date = None
        
        # Parse completed_at from string to datetime object if it exists
        completed_at = None
        if data.get("completed_at"):
            try:
                completed_at = datetime.fromisoformat(data["completed_at"])
            except (ValueError, TypeError):
                completed_at = None
        
        task = Task(
            title=data["title"],
            description=data["description"],
            due_date=due_date,
            completed=data.get("completed", False),
            elo=data.get("elo", 1000),
        )
        task.id = data.get("id", uuid4())
        task.completed_at = completed_at
        return task


class TaskManager:
    def __init__(self, page):
        self.page = page
        self.tasks = self.load_tasks()
        self._make_uuids_unique()
        self.callbacks = []
    
    def on_tasks_updated(self, callback):
        self.callbacks.append(callback)

    def _raise_tasks_updated(self):
        for callback in self.callbacks:
            try:                
                callback()
            except Exception as e:
                print(f"Error in callback: {e}")
    
    def _make_uuids_unique(self):
        existing_ids = set()
        for task in self.tasks:
            while task.id in existing_ids:
                task.id = uuid4()
            existing_ids.add(task.id)

    def load_tasks(self):
        try:
            datas = self.page.client_storage.get(STORAGE_KEY)
            if datas:
                data = json.loads(datas)
                return [Task.from_dict(task_data) for task_data in data]
        except TypeError:
            pass
        return []

    def save_tasks(self):
        self._make_uuids_unique()
        data = json.dumps([task.to_dict() for task in self.tasks], indent=2)
        self.page.client_storage.set(STORAGE_KEY, data)
    
    def trigger_save(self):
        self.save_tasks()
        self._raise_tasks_updated()

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()
        self._raise_tasks_updated()

    def remove_task(self, task: Task):
        if task in self.tasks:
            self.tasks.remove(task)
        self.save_tasks()
        self._raise_tasks_updated()
    
    def complete_task(self, task: Task):
        task.completed = True
        task.completed_at = datetime.now()
        self.save_tasks()
        self._raise_tasks_updated()

    def undo_task(self, task: Task):
        task.completed = False
        task.completed_at = None
        self.save_tasks()
        self._raise_tasks_updated()

    def get_all_tasks(self):
        return sorted(self.tasks, key=lambda t: (t.completed, -t.elo))

    def get_task_for_date(self, target_date: date|datetime):
        if isinstance(target_date, datetime):
            target_date = target_date.date()
        return [task for task in self.tasks if task.due_date == target_date]

    def get_top_priority_tasks(self, n: int = 3):
        sorted_tasks = sorted(self.tasks, key=lambda t: (t.completed, -t.elo))
        return sorted_tasks[:n]

    def get_last_completed(self):
        completed_tasks = [task for task in self.tasks if task.completed and task.completed_at]
        return sorted(completed_tasks, key=lambda t: t.completed_at, reverse=True)
