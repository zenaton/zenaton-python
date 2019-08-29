import abc

from .job import Job

from ..contexts.workflow_context import WorkflowContext

class Workflow(Job):

    @abc.abstractmethod
    def handle(self):
        pass

    def id(self):
        return None

    
    """
        :return TaskContext
    """
    def get_context(self):
        return self._context or WorkflowContext()

    """
        Sets a new context if none has been set yet.
        This is called from the zenaton agent and will raise if called twice.

        :context WorkflowContext
        :raises Exception when the context was already set.
    """
    def set_context(self, context):
        if hasattr(self, '_context') and self._context != None:
            raise Exception('Context is already set and cannot be mutated.')

        self._context = context
