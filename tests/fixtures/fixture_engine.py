import pytest

from zenaton.engine import Engine
from zenaton.client import Client


@pytest.fixture
def engine():
    Client()
    return Engine()
