import abc

from .job import Job
from ..contexts.task_context import TaskContext


class Task(Job):

    @abc.abstractmethod
    def handle(self):
        pass

    """
        (Optional) Implement this method for automatic retrial of task in case of failures.

        :params error Error
        :raises Exception when the return type is not falsy or is not positive integer.
        :return [int, false, None] the amount of seconds to wait
        before automatically retrying this task. Falsy values will avoid
        retrial. Other values will raise.
    """
    def on_error_retry_delay(self, error):
        None

    """
        :return TaskContext
    """
    def get_context(self):
        return self._context or TaskContext()

    """
        Sets a new context if none has been set yet.
        This is called from the zenaton agent and will raise if called twice.

        :params context TaskContext
        :raises Exception when the context was already set.
    """
    def set_context(self, context):
        if hasattr(self, '_context') and self._context != None:
            raise Exception('Context is already set and cannot be mutated.')

        self._context = context
