from .client import Client
from .traits.zenatonable import Zenatonable
from .abstracts.workflow import Workflow
from .abstracts.event import Event
from .abstracts.task import Task
from .parallel import Parallel

import sys
import trace


appId = 'COZLVYTWHQ'
appToken = 'hf1mIIyoKdfW8p71GUkHUwa7fLJYgrhXhhSAVR6XCofdaDuJ5p9QFkJq1uyo'
appEnv = 'dev'

client = Client(appId, appToken, appEnv)

class TaskA(Task, Zenatonable):

    def handle(self):
        print('Task A')
        return 'Task A'


class TaskB(Task, Zenatonable):

    def handle(self):
        print('Task B')
        return 'Task B'

class TaskC(Task, Zenatonable):

    def handle(self):
        print('Task C')
        return 'Task C'


class SequentialWorkflow(Workflow, Zenatonable):

    def handle(self):
        TaskA().execute()
        TaskB().execute()


class ParallelWorkflow(Workflow, Zenatonable):

    def handle(self):
        Parallel(TaskA(), TaskB()).execute()


class MyEvent(Event):
    pass


class EventWorkflow(Workflow, Zenatonable):

    def handle(self):
        TaskA.execute()
        TaskB.execute()

    def on_event(self, event):
        if issubclass(type(event), MyEvent):
            TaskC.execute()

    def id(self):
        return 'MyId'


# tracer = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix],trace=0,count=1)
# tracer.runfunc(SequentialWorkflow().dispatch)
# tracer.runfunc(EventWorkflow().dispatch)

EventWorkflow().where_id(workflow_id='MyId').send_event(MyEvent())
