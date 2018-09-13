from .engine import Engine


class Parallel:
    """
        Build a collection of jobs to be executed in parallel
        :params: [.abstracts.job.Job] items
    """

    def __init__(self, *items):
        self.items = items

    # Execute synchronous jobs
    def execute(self):
        return Engine().execute(self.items)

    # Dispatches synchronous jobs
    def dispatch(self):
        return Engine().dispatch(self.items)
