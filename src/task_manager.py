

import json


class Task:
    def __init__(self, title: str, description: str, due_date: str, completed: bool = False, importance: int = 1):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed
        self.importance = importance

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed,
        }

    @staticmethod
    def from_dict(data: dict):
        return Task(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            completed=data.get("completed", False),
        )


class TaskManager:
    def __init__(self, storage_file: str = "tasks.json"):
        self.storage_file = storage_file
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.storage_file, "r") as f:
                data = json.load(f)
                return [Task.from_dict(task_data) for task_data in data]
        except FileNotFoundError:
            return []

    def save_tasks(self):
        with open(self.storage_file, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task: Task):
        self.tasks.remove(task)
        self.save_tasks()

    def get_all_tasks(self):
        return self.tasks

    def get_task_for_date(self, date: str):
        return [task for task in self.tasks if task.due_date == date]

    def get_top_priority_tasks(self, n: int = 3):
        sorted_tasks = sorted(self.tasks, key=lambda t: (t.completed, -t.importance))
        return sorted_tasks[:n]
