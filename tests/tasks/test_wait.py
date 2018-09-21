import pytest

from zenaton.tasks.wait import Wait
from zenaton.exceptions import ExternalError
from ..fixtures.fixture_event import MyEvent


def test_init():
    with pytest.raises(ExternalError):
        Wait(1)


@pytest.mark.usefixtures("wait")
def test_has_handle(wait):
    assert hasattr(wait, 'handle')


@pytest.mark.usefixtures("wait", "wait_event", "my_event")
def test_valid_param(wait, my_event):
    assert not wait.valid_param(1)
    assert wait.valid_param(None)
    assert wait.valid_param("foo")
    assert wait.valid_param(MyEvent)


@pytest.mark.usefixtures("wait", "my_event")
def test_event_class(wait, my_event):
    assert not wait.event_class("foo")
    assert wait.event_class(MyEvent)
