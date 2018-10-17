import abc

from ..abstracts.workflow import Workflow
from ..exceptions import ExternalError
from ..traits.zenatonable import Zenatonable


class Version(Workflow, Zenatonable):

    def __init__(self, *args):
        if args:
            self.args = args

    @abc.abstractmethod
    def versions(self):
        raise NotImplementedError("Please override the `versions' method in your subclass")

    """Calls handle on the current implementation"""

    def handle(self):
        self.current_implementation().handle()

    """
    Get the current implementation class
    returns class
    """

    def current(self):
        return self.__get_versions()[-1]

    """
        Get the first implementation class
        returns class
    """

    def initial(self):
        return self.__get_versions()[0]

    """
    Returns an instance of the current implementation
    :returns .abstracts.workflow.Workflow
    """

    def current_implementation(self):
        if hasattr(self, 'args'):
            return self.current()(self.args)
        else:
            return self.current()()

    def __get_versions(self):
        if not type(self.versions()) == list:
            raise ExternalError
        if not len(self.versions()) > 0:
            raise ExternalError
        for version in self.versions():
            if not issubclass(version, Workflow):
                raise ExternalError
        return self.versions()
