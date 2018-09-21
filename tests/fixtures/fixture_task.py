import time

import pytest

from zenaton.abstracts.task import Task
from zenaton.traits.zenatonable import Zenatonable


class Task0(Task, Zenatonable):

    def handle(self):
        print('Task 0 starts')
        time.sleep(3)
        print('Task 0 ends')
        return 0


@pytest.fixture
def task0():
    return Task0()


class Task1(Task, Zenatonable):

    def handle(self):
        print('Task 1 starts')
        time.sleep(5)
        print('Task 1 ends')
        return 1


@pytest.fixture
def task1():
    return Task1()


class Task2(Task, Zenatonable):

    def handle(self):
        print('Task 2 starts')
        time.sleep(7)
        print('Task 2 ends')
        return 2


@pytest.fixture
def task2():
    return Task2()


class Task3(Task, Zenatonable):

    def handle(self):
        print('Task 3 starts')
        time.sleep(9)
        print('Task 3 ends')
        return 3


@pytest.fixture
def task3():
    return Task3()
