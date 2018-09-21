import pytest

from zenaton.tasks.wait import Wait
from .fixture_event import MyEvent


@pytest.fixture
def wait():
    return Wait()


@pytest.fixture
def wait_event():
    return Wait(MyEvent)
