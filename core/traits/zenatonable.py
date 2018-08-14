from core.engine import Engine
from core.query.builder import Builder


class Zenatonable:
    """
        Sends self as the single job to be executed
        to the engine and returns the result
    """

    def dispatch(self):
        return Engine().dispatch([self])

    """
        Sends self as the single job to be dispatched
        to the engine and returns the result
    """

    def execute(self):
        return Engine().execute([self])[0]

    """
        Search for workflows to interact with.
        For available methods, see core.query.builder.Builder
        :param String id ID for a given worflow
        :returns core.query.builder.Builder a query builder object
    """

    def where_id(self, workflow_id):
        return Builder(type(self)).where_id(workflow_id)
