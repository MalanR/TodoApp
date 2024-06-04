import uuid
import asyncio
import datetime
import json
import os
from DateTimEencoder import DateTimeEncoder, as_datetime

# initial greeting on first run of the program.
print('________________________________________________________')
print('|                  TODO LIST                           |')
print('________________________________________________________')

# file handling
# this is the file where all the tasks will be stored and accessed from.
task_file = 'tasks.json'


# function for writing to the pre-defined json file
def store_tasks(tasks):
    with open(task_file, 'w') as file:
        json.dump(tasks, file, cls=DateTimeEncoder)


# check if the json file exists, if found we try to open the file and read the content
# making sure that the datetime read as datetime after checking for content.
# if there is an error with reading the file we want to know that there was an at this point.
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


# Defining the TodoList class and initializing it by loading existing tasks
class TodoList:
    # loading the existing tasks from the json file to the todolist

    @staticmethod
    def new():
        return TodoList()

    def __init__(self):
        self.todos = load_tasks()

    def print_todos(self):
        # printing all the tasks in todolist by iterating through all the tasks and printing the defined content
        # this will display when the users selects to see the list with option 5
        for task_id, task in self.todos.items():
            print(f"ID: {task_id}")
            print(f"Description: {task['description']}")
            print(f"Created at: {task['created_at']}")
            print(f"Completed at: {task['completed_at']}")
            print("--------------------------------------------------------------------")

    async def user_action(self):
        # while loop for the user to see what their options are in the app.
        # created as a while loop so that this "menu" displays after each action the user makes.
        while True:
            print("\n1) Add a Task")
            print("2) Remove a Task")
            print("3) Update a Task")
            print("4) Complete a Task")
            print("5) View all Tasks")
            print("6) Search Tasks")
            print("7) Exit")

            # prompting the user to enter their choice of action
            choice = input('Please enter your choice: ')

            # very basic if and elif statements to handel the users actions and return the correct method.
            if choice == '1':
                description = input('Please enter a task description: ')
                await self.add_task(description)
            elif choice == '2':
                task_id = input('Enter the task ID to remove: ')
                await self.delete_task(task_id)
            elif choice == '3':
                task_id = input('Enter the task ID to update: ')
                updated_description = input('Enter the updated task description: ')
                await self.update_task(task_id, updated_description)
            elif choice == '4':
                task_id = input('Enter the task ID to complete: ')
                await self.complete_task(task_id)
            elif choice == '5':
                self.print_todos()
            elif choice == '6':
                user_search = input("1) Incomplete Tasks\n2) Completed Tasks\n3) Search a word from a task\nEnter "
                                    "your choice: ")
                await self.search_task(user_search)
            elif choice == '7':
                print("Goodbye")
                break
            else:
                print('Invalid entry')

    async def add_task(self, description):
        # generating an task ID for each task by using UUID.
        task_id = str(uuid.uuid4())

        #  create a new task dictionary.
        new_task = {
            "id": task_id,
            "description": description,
            "created_at": datetime.datetime.now(),
            "completed_at": None
        }

        #  adding the new task to the todolist dictionary.
        self.todos[task_id] = new_task

        #  store the new task in the json file.
        store_tasks(self.todos)

        #  confirming that the task has been added and provide the ID as this will be
        # needed later on for updating, deleting and completing tasks.
        print(f"Task '{description}' added with ID {task_id}")
        return task_id, description

    async def delete_task(self, task_id):
        # one the task with the provided ID was found we simply delete it from the json file.
        if task_id in self.todos:
            del self.todos[task_id]

            # update the json file
            store_tasks(self.todos)
            print(f"Task with ID {task_id} has been deleted. ")
        else:

            # if the task id was not find i prompt the user that id was not find
            print(f"Task with ID {task_id} not found. ")

    #  update the description of a task after finding the task ID
    async def update_task(self, task_id, task_description):

        # finding the task by its ID
        if task_id in self.todos:

            # finding the tasks description and setting it to be equal to the description entered
            # by the user.
            self.todos[task_id]['description'] = task_description

            # update the json file
            store_tasks(self.todos)
            print(f"Task with ID {task_id} has been updated with {task_description}. ")
        else:
            print(f"Task with ID {task_id} not found. ")

    async def complete_task(self, task_id):

        # finding the task by its ID
        if task_id in self.todos:

            # finding the tasks completed at status and setting it to be equal to the current datetime.
            self.todos[task_id]['completed_at'] = datetime.datetime.now()

            # update json file
            store_tasks(self.todos)
            print(f"Task with ID {task_id} has been marked as complete")
        else:
            print("Invalid task ID")

    async def search_task(self, user_input):
        # create a list to keep the filtered tasks in for when we return them to the user.
        filtered_tasks = []

        # taking input from the user.
        if user_input == '1':

            # iterating through all the tasks.
            for task_id, task in self.todos.items():

                # finding all the tasks with a completed at state of None.
                if task['completed_at'] is None:
                    # adding the found tasks to the filtered tasks list.
                    filtered_tasks.append(task)
        elif user_input == '2':
            for task_id, task in self.todos.items():

                # finding the tasks with a status that is not None.
                if task['completed_at'] is not None:
                    # adding the found tasks to the filtered tasks list.
                    filtered_tasks.append(task)
        elif user_input == '3':

            # take input from the user and converting it to lowercase
            partial_text = str(input("Search for a word in any task: ")).lower()

            # iterate through all tasks
            for task_id, task in self.todos.items():

                # check if the user entered text is in the description of any of the tasks
                if partial_text in task['description'].lower():
                    # if a task/tasks was found it gets added to the filtered tasks list.
                    filtered_tasks.append(task)
        else:

            # if the user entry was not any of the numbered options.
            print("Invalid entry.")

        # printing all the tasks that have been added to the filtered tasks list.
        for task in filtered_tasks:
            print(" ")
            print(f"ID: {task['id']}"),
            print(f"Description: {task['description']}"),
            print(f"Created at: {task['created_at']}"),
            print(f"Completed at: {task['completed_at']}"),
            print("--------------------------------------------------------------------")
        return filtered_tasks


# create a new instance of the TodoList by using the static factory method.
my_todo_list = TodoList.new()

# run the user_action method to be able to interact with the todolist.
asyncio.run(my_todo_list.user_action())
