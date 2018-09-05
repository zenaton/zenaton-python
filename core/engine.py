from .abstracts.task import Task
from .abstracts.workflow import Workflow
from .exceptions import InvalidArgumentError
from .singleton import Singleton


class Engine(metaclass=Singleton):
    """
        Zenaton Engine is a singleton class that stores a reference to the current
        client and processor. It then handles job processing either locally or
        through the processor with Zenaton workers
        To access the instance, call `Zenaton::Engine.instance`
    """

    def __init__(self):
        from .client import Client
        self.client = Client()
        self.processor = None

    """
        Executes jobs synchronously
        @param jobs [Array<Zenaton::Interfaces::Job>]
        @return [Array<String>, nil] the results if executed locally, or nil
    """
    def execute(self, jobs):
        map(self.check_argument, jobs)
        if len(jobs) == 0 or self.processor is None:
            return [job.handle() for job in jobs]
        return self.processor.process(jobs, True)

    """
        Executes jobs asynchronously
        @param jobs [Array<Zenaton::Interfaces::Job>]
        @return nil
    """
    def dispatch(self, jobs):
        map(self.check_argument, jobs)
        if len(jobs) == 0 or self.processor is None:
            [self.local_dispatch(job) for job in jobs]
        if self.processor and len(jobs) > 0:
            self.processor.process(jobs, False)

    def local_dispatch(self, job):
        # if True:
        if issubclass(job.__class__, Workflow):
            self.client.start_workflow(job)
        else:
            job.handle()

    def check_argument(self, job):
        if not self.valid_job(job):
            raise InvalidArgumentError('You can only execute or dispatch Zenaton Task or Worflow')

    """
        Checks if the job is a valid job i.e. it is either a Task or a Workflow
    """
    def valid_job(self, job):
        return issubclass(job.__class__, Task) or issubclass(job.__class__, Workflow)
