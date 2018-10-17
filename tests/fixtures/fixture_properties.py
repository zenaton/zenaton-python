import pytest

from zenaton.services.properties import Properties


@pytest.fixture
def properties():
    return Properties()
