import pytest


class DummyClass:
    pass


@pytest.fixture
def DummyObject():
    return DummyClass()
