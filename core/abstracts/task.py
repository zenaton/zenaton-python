import abc

from .job import Job


class Task(Job):

    @abc.abstractmethod
    def handle(self):
        pass
