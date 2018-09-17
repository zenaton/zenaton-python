import abc

from .job import Job


class Workflow(Job):

    @abc.abstractmethod
    def handle(self):
        pass

    def id(self):
        return None
