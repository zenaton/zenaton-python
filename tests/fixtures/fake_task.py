import time

import pytest

from zenaton.abstracts.task import Task
from zenaton.traits.zenatonable import Zenatonable


class FakeTask0Class(Task, Zenatonable):

    def handle(self):
        print('FakeTask 0 starts')
        time.sleep(3)
        print('FakeTask 0 ends')
        return 0


@pytest.fixture
def FakeTask0():
    return FakeTask0Class()


class FakeTask1Class(Task, Zenatonable):

    def handle(self):
        print('FakeTask 1 starts')
        time.sleep(5)
        print('FakeTask 1 ends')
        return 1


@pytest.fixture
def FakeTask1():
    return FakeTask1Class()


class FakeTask2Class(Task, Zenatonable):

    def handle(self):
        print('FakeTask 2 starts')
        time.sleep(7)
        print('FakeTask 2 ends')
        return 2


@pytest.fixture
def FakeTask2():
    return FakeTask2Class()


class FakeTask3Class(Task, Zenatonable):

    def handle(self):
        print('FakeTask 3 starts')
        time.sleep(9)
        print('FakeTask 3 ends')
        return 3


@pytest.fixture
def FakeTask3():
    return FakeTask3Class()
