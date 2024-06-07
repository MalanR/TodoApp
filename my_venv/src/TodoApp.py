import uuid
import asyncio
import datetime
import json
import os
from my_venv.src.DateTimEencoder import DateTimeEncoder, as_datetime

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
# Todo Change todoApp
class TodoApp:
    # loading the existing tasks from the json file to the todolist

    @staticmethod
    # use new to start a new blank todo list from scratch.
    def new():
        return TodoApp()

    def __init__(self):
        self.todos = load_tasks()

    def print_todos(self):
        # printing all the tasks in todolist by iterating through all the tasks and printing the defined content
        # this will display when the users selects to see the list with option 5
        for task_id, task in self.todos.items():
            print(f"ID: {task_id}")
            print(f"Description: {task['description']}")
            print(f"Created_on: {task['created_on']}")
            print(f"Completed_on: {task['completed_on']}")
            print("--------------------------------------------------------------------")

    async def user_action(self):
        while True:
        # while loop for the user to see what their options are in the app.
        # created as a while loop so that this "menu" displays after each action the user makes.

            crud_operations = {
                1: self.create,
                2: self.delete,
                3: self.update,
                4: self.complete,
                5: self.print_todos,
                6: self.filter,
                7: lambda: print("Goodbye") or exit()
            }

            try:
                user_input = int(input(
                    "1)\033[92m Add Task\033[0m\n2)\033[92m Delete a task\033[0m\n3)\033[92m Update a task\033["
                    "0m\n4)\033[92m Complete a task\033[0m\n5)\033[92m View "
                    "all tasks\033[0m\n6)\033[92m Filter tasks\033[0m\n7)\033[93m Exit\033[0m\nChoose an option: "))

                # Checking for a match in the user input and the crud dictionary.
                if user_input in crud_operations:

                    # check if the user has entered option 1, if so we do not require the tasks ID.
                    if user_input == 1:

                        # get the task name/description from the user.
                        description = input("Enter task description: ")

                        # Await the create function to execute.
                        await crud_operations[user_input](description)

                    #     check if the user input is 2,3 or 4, these require an existing tasks ID
                    elif user_input in [2, 3, 4]:

                        # take in the tasks ID
                        task_id = input("Enter task ID: ")

                        # check if the input is 3
                        if user_input == 3:

                            # get the new task name/description from the user
                            task_description = input("Enter new task description: ")

                            # Await the update function to execute.
                            await crud_operations[user_input](task_id, task_description)
                        else:

                            # Await the corresponding function to execute based on the crud_operation dictionary and
                            # the user's input.
                            await crud_operations[user_input](task_id)

                    #         if the user input is 6, we need to print the filter options the users has.
                    elif user_input == 6:
                        print("\n1) Incomplete Tasks")
                        print("2) Completed Tasks")
                        print("3) Search by Text")

                        # take in the users choice.
                        search_choice = input('Please choose a search option: ')

                        # Await the filter function to execute.
                        await crud_operations[user_input](search_choice)
                    else:

                        # check if the selected function is a coroutine function, if it is, await the execution of
                        # the selected function, otherwise execute immediately.
                        if asyncio.iscoroutinefunction(crud_operations[user_input]):
                            await crud_operations[user_input]()
                        else:
                            crud_operations[user_input]()
                else:

                    # display a message if the user enters a number that is not within the defined range
                    print("\033[91mInvalid Entry\033[0m")
            except ValueError:

                # ValueError incase the user's input is not an integer.
                print("\033[91mYou did not enter an integer\033[0m")

    async def create(self, description):
        # generating an task ID for each task by using UUID.
        task_id = str(uuid.uuid4())

        #  create a new task dictionary.
        new_task = {
            "id": task_id,
            "description": description,
            "created_on": datetime.datetime.now().strftime("%d-%H:%M"),
            "completed_on": None
        }

        #  adding the new task to the todolist dictionary.
        self.todos[task_id] = new_task

        #  store the new task in the json file.
        store_tasks(self.todos)

        #  confirming that the task has been added and provide the ID as this will be
        # needed later on for updating, deleting and completing tasks.
        print(f"Task '{description}' added with ID {task_id}")
        return task_id, description

    async def delete(self, task_id):
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
    async def update(self, task_id, task_description):

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

    async def complete(self, task_id):

        # finding the task by its ID
        if task_id in self.todos:

            # finding the tasks completed at status and setting it to be equal to the current datetime.
            self.todos[task_id]['completed_on'] = datetime.datetime.now()

            # update json file
            store_tasks(self.todos)
            print(f"Task with ID {task_id} has been marked as complete")
        else:
            print("Invalid task ID")

    async def filter(self, user_input):
        # create a list to keep the filtered tasks in for when we return them to the user.
        filtered_tasks = []

        # taking input from the user.
        if user_input == '1':

            # iterating through all the tasks.
            for task_id, task in self.todos.items():

                # finding all the tasks with a completed at state of None.
                if task['completed_on'] is None:
                    # adding the found tasks to the filtered tasks list.
                    filtered_tasks.append(task)
        elif user_input == '2':
            for task_id, task in self.todos.items():

                # finding the tasks with a status that is not None.
                if task['completed_on'] is not None:
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
            print(f"Created_on: {task['created_on']}"),
            print(f"Completed_on: {task['completed_on']}"),
            print("--------------------------------------------------------------------")
        return filtered_tasks


# create a new instance of the TodoList by using the static factory method.
my_todo_list = TodoApp.new()

# run the user_action method to be able to interact with the todolist.
asyncio.run(my_todo_list.user_action())
