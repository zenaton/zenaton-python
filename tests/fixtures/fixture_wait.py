import pytest

from zenaton.tasks.wait import Wait
from .fixture_event import MyEvent


@pytest.fixture
def wait():
    wait = Wait()
    wait.set_timezone('Europe/Paris')
    return wait


@pytest.fixture
def wait_event():
    return Wait(MyEvent)
