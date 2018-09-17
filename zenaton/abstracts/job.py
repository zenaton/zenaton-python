import abc


class Job:

    @abc.abstractmethod
    def handle(self):
        pass
