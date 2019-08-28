class TaskContext():
    """
    Represents the current runtime context of a Task.

    The information provided by the context can be useful to alter the
    behaviour of the task.

    For example, you can use the attempt index to know if a task has been
    automatically retried or not and how many times, and decide to do
    something when you did not expect the task to be retried more than X
    times.

    You can also use the attempt number in the `on_error_retry_delay` method
    of a task in order to implement complex retry strategies.

    Attributes
    ----------
    id : str
        The UUID identifying the current task.

    retry_index : int
        The number of times this task has been automatically retried.
        This counter is reset if you issue a manual retry from your dashboard
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.retry_index = kwargs.get('retry_index', None)
