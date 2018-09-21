from zenaton.abstracts.workflow import Workflow


def test_has_handle():
    assert hasattr(Workflow(), 'handle')
