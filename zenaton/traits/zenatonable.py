from ..engine import Engine
from ..query.builder import Builder
from zenaton.exceptions import InvalidArgumentError


class Zenatonable:
    """
        Sends self as the single job to be dispatched
        to the engine and returns the result
    """
    def dispatch(self):
        return Engine().dispatch([self])

    """
        Sends self as the single job to be scheduled
        to the engine and returns the result
    """
    def schedule(self, cron):
        if not isinstance(cron, str) or cron == "":
            raise InvalidArgumentError("Param passed to 'schedule' function must be a non empty cron string")

        return Engine().schedule([self], cron)

    """
        Sends self as the single job to be executed
        to the engine and returns the result
    """
    def execute(self):
        return Engine().execute([self])[0]

    """
        Search for workflows to interact with.
        For available methods, see .query.builder.Builder
        :param String id ID for a given worflow
        :returns .query.builder.Builder a query builder object
    """

    @classmethod
    def where_id(cls, workflow_id):
        return Builder(cls).where_id(workflow_id)
