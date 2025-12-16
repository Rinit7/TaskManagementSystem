import csv
import os
from datetime import datetime
from uuid import uuid4

FILE_NAME = "tasks.csv"


# ------------------ Task Class ------------------

class Task:
    def __init__(self, user, title, description, priority, due_date=None,
                 completed=False, task_id=None, created_at=None):
        self.user = user
        self.id = task_id or str(uuid4())[:8]
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_list(self):
        return [
            self.user,
            self.id,
            self.title,
            self.description,
            self.priority,
            self.due_date,
            self.completed,
            self.created_at
        ]


# ------------------ Task Manager Class ------------------

class TaskManager:
    def __init__(self, filename):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.filename):
            return

        with open(self.filename, newline="", mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                task = Task(
                    user=row[0],
                    task_id=row[1],
                    title=row[2],
                    description=row[3],
                    priority=row[4],
                    due_date=row[5] if row[5] else None,
                    completed=row[6] == "True",
                    created_at=row[7]
                )
                self.tasks.append(task)

    def save_tasks(self):
        with open(self.filename, newline="", mode="w") as file:
            writer = csv.writer(file)
            writer.writerow([
                "user", "id", "title", "description",
                "priority", "due_date", "completed", "created_at"
            ])
            for task in self.tasks:
                writer.writerow(task.to_list())

    def add_task(self, user):
        title = input("Title: ")
        description = input("Description: ")
        priority = input("Priority (low/medium/high): ").lower()
        due_date = input("Due Date (YYYY-MM-DD, optional): ")

        task = Task(user, title, description, priority, due_date or None)
        self.tasks.append(task)
        print("✅ Task added.")

    def get_user_tasks(self, user):
        return [task for task in self.tasks if task.user == user]

    def find_task(self, task_id, user):
        for task in self.tasks:
            if task.id == task_id and task.user == user:
                return task
        return None

    def view_tasks(self, user):
        tasks = self.get_user_tasks(user)
        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            status = "✔ Completed" if task.completed else "✘ Incomplete"
            print("-" * 40)
            print(f"ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Priority: {task.priority}")
            print(f"Due Date: {task.due_date}")
            print(f"Status: {status}")
            print(f"Created At: {task.created_at}")

    def edit_task(self, user):
        task_id = input("Task ID: ")
        task = self.find_task(task_id, user)

        if not task:
            print("❌ Task not found.")
            return

        task.title = input(f"Title ({task.title}): ") or task.title
        task.description = input(f"Description ({task.description}): ") or task.description
        task.priority = input(f"Priority ({task.priority}): ") or task.priority
        task.due_date = input(f"Due Date ({task.due_date}): ") or task.due_date

        print("✅ Task updated.")

    def delete_task(self, user):
        task_id = input("Task ID: ")
        task = self.find_task(task_id, user)

        if task:
            self.tasks.remove(task)
            print("🗑 Task deleted.")
        else:
            print("❌ Task not found.")

    def toggle_complete(self, user):
        task_id = input("Task ID: ")
        task = self.find_task(task_id, user)

        if task:
            task.completed = not task.completed
            print("✅ Task status updated.")
        else:
            print("❌ Task not found.")

    def sort_tasks(self, user):
        tasks = self.get_user_tasks(user)

        print("""
1. Priority
2. Due Date
3. Creation Date
4. Completion Status
""")
        choice = input("Choose option: ")

        if choice == "1":
            order = {"low": 1, "medium": 2, "high": 3}
            tasks.sort(key=lambda x: order.get(x.priority, 0))
        elif choice == "2":
            tasks.sort(key=lambda x: x.due_date or "9999-12-31")
        elif choice == "3":
            tasks.sort(key=lambda x: x.created_at)
        elif choice == "4":
            tasks.sort(key=lambda x: x.completed)

        self.view_tasks(user)


# ------------------ Main Program ------------------

def main():
    manager = TaskManager(FILE_NAME)
    user = input("Enter username: ")

    while True:
        print(f"""
===== Task Manager ({user}) =====
1. Add Task
2. View Tasks
3. Edit Task
4. Delete Task
5. Mark Complete/Incomplete
6. Sort Tasks
7. Save & Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            manager.add_task(user)
        elif choice == "2":
            manager.view_tasks(user)
        elif choice == "3":
            manager.edit_task(user)
        elif choice == "4":
            manager.delete_task(user)
        elif choice == "5":
            manager.toggle_complete(user)
        elif choice == "6":
            manager.sort_tasks(user)
        elif choice == "7":
            manager.save_tasks()
            print("💾 Tasks saved. Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
