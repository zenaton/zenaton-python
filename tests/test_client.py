import pytest


@pytest.mark.usefixtures("FakeClient")
def test_test(FakeClient):
    assert hasattr(FakeClient, 'start_workflow')
