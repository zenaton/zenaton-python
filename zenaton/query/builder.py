from ..abstracts.workflow import Workflow
from ..exceptions import ExternalError


class Builder:
    """Wrapper class around the client to interact with workflows by id"""

    def __init__(self, class_):
        from ..client import Client
        self.check_class(class_)
        self.class_ = class_
        self.client = Client()

    """
        Sets the id of the workflow we want to find
        :param String or None id the id
        :returns Builder the current builder
    """
    def where_id(self, id):
        self.id = id
        return self

    """
        Finds a workflow
        returns Workflow
    """
    def find(self):
        return self.client.find_workflow(self.class_, self.id)

    """
        Sends an event to a workflow
        :param abstracts.event.Event event the event to send
        :returns query.builder the current builder
    """
    def send_event(self, event):
        self.client.send_event(self.class_.__name__, self.id, event)

    """
        Kills a workflow
        :returns query.builder.Builder the current builder
    """
    def kill(self):
        self.client.kill_workflow(self.class_, self.id)
        return self

    """
        Pauses a workflow
        :returns query.builder.Builder the current builder
    """
    def pause(self):
        self.client.pause_workflow(self.class_, self.id)
        return self

    """
        Resumes a workflow
        :returns query.builder.Builder the current builder
    """
    def resume(self):
        self.client.resume_workflow(self.class_, self.id)
        return self

    """
        Checks if class_ is subclass of Workflow
        :param class class_
    """

    def check_class(self, class_):
        msg = '{} should be a subclass of .abstracts.workflow'.format(class_)
        if not issubclass(class_, Workflow):
            raise ExternalError(msg)
