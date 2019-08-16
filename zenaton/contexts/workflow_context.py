class WorkflowContext():
    """
    Represents the current runtime context of a Workflow.

    Attributes
    ----------
    id : str
        The UUID identifying the current workflow
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
