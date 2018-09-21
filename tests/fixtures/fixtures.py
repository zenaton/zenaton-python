import pytest


class DummyClass:
    pass


@pytest.fixture
def dummy_object():
    return DummyClass()
