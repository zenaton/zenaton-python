import inspect

from ..abstracts.event import Event
from ..abstracts.task import Task
from ..exceptions import ExternalError
from ..traits.with_timestamp import WithTimestamp
from ..traits.zenatonable import Zenatonable


class Wait(Task, Zenatonable, WithTimestamp):

    def __init__(self, event=None):
        super(Wait, self).__init__()
        if not self.valid_param(event):
            raise ExternalError(self.error)
        if event:
            self.event = event.__name__

    @property
    def error(self):
        return '{}: Invalid parameter - argument must be a zenaton.abstracts.event.Event subclass'.format(
            self.__class__.__name__)

    def handle(self):
        pass

    def valid_param(self, event):
        return not event or isinstance(event, str) or self.event_class(event)

    def event_class(self, event):
        return inspect.isclass(event) and issubclass(event, Event)
