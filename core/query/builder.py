from ..abstracts.workflow import Workflow
from ..exceptions import ExternalError


class Builder:
    """Wrapper class around the client to interact with workflows by id"""
    def __init__(self, klass):
        from ..client import Client
        self.check_klass(klass)
        self.klass = klass
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
        return self.client.find_workflow(self.klass, self.id)

    """
        Sends an event to a workflow
        :param abstracts.event.Event event the event to send
        :returns query.builder the current builder
    """
    def send_event(self, event):
        self.client.send_event(self.klass.__name__, self.id, event)

    """
        Kills a workflow
        :returns query.builder.Builder the current builder
    """
    def kill(self):
        self.client.kill_workflow(self.klass, self.id)
        return self

    """
        Pauses a workflow
        :returns query.builder.Builder the current builder
    """
    def pause(self):
        self.client.pause_workflow(self.klass, self.id)
        return self

    """
        Resumes a workflow
        :returns query.builder.Builder the current builder
    """
    def resume(self):
        self.client.resume_workflow(self.klass, self.id)
        return self

    """
        Checks if klass is subclass of Workflow
        :param class klass
    """
    def check_klass(self, klass):
        msg = '{} should be a subclass of .abstracts.workflow'.format(klass)
        if not issubclass(klass, Workflow):
            raise ExternalError(msg)
