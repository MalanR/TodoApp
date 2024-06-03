import uuid
import asyncio
import datetime
import json
import os
from DateTimEencoder import DateTimeEncoder, as_datetime

print('--------------------------------------------------')
print('               TODO LIST                          ')
print('--------------------------------------------------')
print("\n")
print("1) Add a Task")
print("2) Remove a Task")
print("3) Update a Task")
print("4) Complete a Task")
print("5) View all Tasks")
print("6) Search Tasks")
print("7) Exit")

# file handeling
task_file = 'tasks.json'


def store_tasks(tasks):
    with open(task_file, 'w') as file:
        json.dump(tasks, file, cls=DateTimeEncoder)


def load_tasks():
    if os.path.exists(task_file):
        try:
            with open(task_file, 'r') as file:
                content = file.read()
                if content.strip():
                    return json.loads(content, object_hook=as_datetime)
        except json.JSONDecodeError:
            print("Error reading the task file")
            return {}
    return {}


# This is the main class, it stores an empty array, our tasks being added will be appended to this empty array.
class TodoList:
    def __init__(self):
        self.todos = load_tasks()

    def print_todos(self):
        for task_id, task in self.todos.items():
            print(f"ID: {task_id}")
            print(f"Description: {task['description']}")
            print(f"Created at: {task['created_at']}")
            print(f"Completed at: {task['completed_at']}")
            print("--------------------------------------------------------------------")

    # start building the async functions based on user input

    async def user_action(todo_list):
        user_choice = {
            '1': todo_list.add_task,
            '2': todo_list.delete_task,
            '3': todo_list.update_task,
            '4': todo_list.complete_task,
            '5': todo_list.print_todos,
            # '6': todo_list.search_task,
            '7': lambda: print('Goodbey')
        }

        while True:
            choice = str(input('Please enter your choice:'))
            action = user_choice.get(choice)
            if action:
                if choice == '5':
                    todo_list.print_todos()
                else:
                    task_id = str(input('Please enter task ID: '))
                    await action(task_id)
                if choice == '7':
                    break
            else:
                print('Invalid entry')

    # function for adding tasks
    async def add_task(self, description):
        task_id = str(uuid.uuid4())
        new_task = {
            "id": task_id,
            "description": description,
            "created_at": datetime.datetime.now(),
            "completed_at": None
        }
        self.todos[task_id] = new_task
        store_tasks(self.todos)
        print(f"Task '{description}' added with ID {task_id}")
        return (task_id, description)

    # function for deleting tasks
    async def delete_task(self, task_id):
        if task_id in self.todos:
            del self.todos[task_id]
            store_tasks(self.todos)
            print(f"Task with ID {task_id} has been deleted. ")
        else:
            print(f"Task with ID {task_id} not found. ")

    # function for updating tasks
    async def update_task(self, task_id, task_description):
        if task_id in self.todos:
            self.todos[task_id]['description'] = task_description
            store_tasks(self.todos)
            print(f"Task with ID {task_id} has been updated with {task_description}. ")
        else:
            print(f"Task with ID {task_id} not found. ")

    # function for marking tasks as complete
    async def complete_task(self, task_id):
        if task_id in self.todos:
            self.todos[task_id]['completed_at'] = datetime.datetime.now()
            store_tasks(self.todos)
            print(f"Task with ID {task_id} has been marked as complete")
        else:
            print("Invalid task ID")

    async def filters(self, task_id):



my_todo_list = TodoList()
asyncio.run(my_todo_list.user_action())
