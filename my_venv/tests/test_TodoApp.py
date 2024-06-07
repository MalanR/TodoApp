from my_venv.src.TodoApp import TodoList
import asyncio
from unittest.mock import patch
import pytest


@pytest.fixture
def todo_list():
    """Fixture to provide a new TodoList instance for each test."""
    return TodoList()


# Test if add_task method adds a task correctly
def add_task(todo_list, param):
    pass


@pytest.mark.asyncio
def test_add_task(todo_list):
    """Tests adding a task to the TodoList."""
    assert len(todo_list.todos) == 0
    add_task(todo_list, "Task 1")
    assert len(todo_list.todos) == 1
    assert todo_list.todos[0]["description"] == "Task 1"
