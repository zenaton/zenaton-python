import pytest

from .fixture_task import task0, task1, task2, task3
from .fixture_event import MyEvent

from zenaton.abstracts.workflow import Workflow
from zenaton.traits.zenatonable import Zenatonable
from zenaton.workflows.version import Version


class SequentialWorkflow(Workflow, Zenatonable):

    def __init__(self):
        self.id_ = 'MyTestWorkflowId'

    def handle(self):

        a = task0.execute()

        if a > 0:
            task1.execute()
        else:
            task2.execute()

        task3.execute()

    def id(self):
        return self.id_

    def set_id(self, id_):
        self.id_ = id_

    def on_event(self, event):
        if issubclass(MyEvent, type(event)):
            return True
        else:
            return False



@pytest.fixture
def sequential_workflow():
    return SequentialWorkflow()


class VersionWorkflow(Version):

    def versions(self):
        return [SequentialWorkflow, ]


@pytest.fixture
def version_workflow():
    return VersionWorkflow()
