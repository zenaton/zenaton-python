from zenaton.abstracts.task import Task


def test_has_handle():
    assert hasattr(Task(), 'handle')
