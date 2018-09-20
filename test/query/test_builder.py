import pytest

from zenaton.query.builder import Builder

@pytest.mark.usefixtures("FakeSequentialWorkflow")
def test_test(FakeSequentialWorkflow):
    assert hasattr(FakeSequentialWorkflow, 'handle')

