import pytest

from zenaton.abstracts.event import Event


class MyEvent(Event):
    pass


@pytest.fixture
def my_event():
    return MyEvent()
