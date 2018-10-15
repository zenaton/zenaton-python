import pytest

from zenaton.services.serializer import Serializer


@pytest.fixture
def serializer():
    return Serializer()
