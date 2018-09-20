from zenaton.singleton import Singleton


class SingleClass(metaclass=Singleton):
    def __init__(self):
        self.foo = 0


def test_unicity():
    SingleClass().foo = 1
    assert SingleClass().foo == 1
