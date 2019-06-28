import pytest


class CustomClass(object):
    def __init__(self, value):
        self.value = value


@pytest.mark.usefixtures("properties")
def test_from_args(properties):
    props = properties.from_(CustomClass(5))
    assert props == {'value': 5}


@pytest.mark.usefixtures("properties")
def test_from_args(properties):
    with pytest.raises(TypeError, match=r'Could not get properties from 5: .*'):
        properties.from_(5)
