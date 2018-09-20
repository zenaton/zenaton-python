import pytest

from .fake_task import FakeTask0, FakeTask1, FakeTask2, FakeTask3

from zenaton.abstracts.workflow import Workflow
from zenaton.traits.zenatonable import Zenatonable


class FakeSequentialWorkflowClass(Workflow, Zenatonable):

    def handle(self):

        a = FakeTask0().execute()

        if a > 0:
            FakeTask1().execute()
        else:
            FakeTask2().execute()

        FakeTask3().execute()

    def id(self):
        return 'MySequentialId'


@pytest.fixture
def FakeSequentialWorkflow():
    return FakeSequentialWorkflowClass()
