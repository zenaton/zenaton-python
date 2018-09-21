from zenaton.abstracts.job import Job


def test_has_handle():
    assert hasattr(Job(), 'handle')
