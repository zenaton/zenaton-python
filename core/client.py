import os

from core.exceptions import InvalidArgumentError
from core.services.http_service import HttpService
from core.workflows.version import Version


# from core.services.serializer import Serializer
# from core.services.properties import Properties

class Client:

    ZENATON_API_URL = 'https://zenaton.com/api/v1' # Zenaton api url
    ZENATON_WORKER_URL = 'http://localhost' # Default worker url
    DEFAULT_WORKER_PORT = 4001 # Default worker port
    WORKER_API_VERSION = 'v_newton' # Default worker api version

    MAX_ID_SIZE = 256 # Limit on length of custom ids

    APP_ENV = 'app_env' # Parameter name for the application environment
    APP_ID = 'app_id' # Parameter name for the application ID
    API_TOKEN = 'api_token' # Parameter name for the API token

    ATTR_ID = 'custom_id' # Parameter name for custom ids
    ATTR_NAME = 'name' # Parameter name for workflow names
    ATTR_CANONICAL = 'canonical_name' # Parameter name for version name
    ATTR_DATA = 'data' # Parameter name for json payload
    ATTR_PROG = 'programming_language' # Parameter name for the language
    ATTR_MODE = 'mode' # Parameter name for the worker update mode

    PROG = 'Python'  # The current programming language

    EVENT_INPUT = 'event_input' # Parameter name for event data
    EVENT_NAME = 'event_name' # Parameter name for event name

    WORKFLOW_KILL = 'kill' # Worker update mode to stop a worker
    WORKFLOW_PAUSE = 'pause' # Worker udpate mode to pause a worker
    WORKFLOW_RUN = 'run' # Worker update mode to resume a worker

    def __init__(self, appId, apiToken, appEnv):
        self.appId = appId
        self.apiToken = apiToken
        self.appEnv = appEnv
        self.http = HttpService()
        # self.serializer = Serializer()
        # self.properties = Properties()


    """
        Gets the url for the workers
        :param String resource the endpoint for the worker
        :param String params url encoded parameters to include in request
        :returns String the workers url with parameters
    """
    def worker_url(self, resource='', params=''):
        base_url = os.environ('ZENATON_WORKER_URL') or self.ZENATON_WORKER_URL
        port = os.environ('ZENATON_WORKER_PORT') or self.DEFAULT_WORKER_PORT
        url = '{}:{}/api/{}/{}?'.format(base_url, port, self.WORKER_API_VERSION, resource)
        return self.add_app_env(url, params)

    """
        Gets the url for zenaton api
        :param String resource the endpoint for the api
        :param String params url encoded parameters to include in request
        :returns String the api url with parameters
    """
    def website_url(self, resource='', params=''):
        api_url = os.environ('ZENATON_API_URL') or self.ZENATON_API_URL
        url = '{}/{}?{}={}&'.format(api_url, resource, self.API_TOKEN, params)
        return self.add_app_env(url, params)

    """
        Start the specified workflow
        :params core.abstracts.workflow.Workflow flow
    """

    def start_workflow(self, flow):
        self.http.post(self.instance_worker_url(),
                       data={
                           self.ATTR_PROG: self.PROG,
                           self.ATTR_CANONICAL: self.canonical_name(flow),
                           self.ATTR_NAME: self.class_name(flow),
                           self.ATTR_DATA: {},
                           self.ATTR_ID: self.parse_custom_id_from(flow)
                       }
                       )

    """
        Stops a workflow
        :param String workflow_name the class name of the workflow
        :param String custom_id the custom ID of the workflow, if any
        :returns None
    """

    def kill_workflow(self, workflow_name, custom_id)
        self.update_instance(workflow_name, custom_id, self.WORKFLOW_KILL)

    def instance_website_url(self, params):
        return self.website_url('instances', params)

    def instance_worker_url(self, params):
        return self.worker_url('instances', params)

    def add_app_env(self, url, params):
        app_env = '{} : {}'.format(self.APP_ENV, self.appEnv) if self.app_env else ''
        app_id = '{} : {}'.format(self.APP_ENV, self.app_id) if self.app_id else ''
        return '{}{}{}{}'.format(url, app_env, app_id, params)

    def parse_custom_id_from(self, flow):
        custom_id = flow.id
        if custom_id:
            if not isinstance(custom_id, str) and not isinstance(custom_id, int):
                raise InvalidArgumentError('Provided ID must be a string or an integer')
            custom_id = str(custom_id)
            if len(custom_id) > self.MAX_ID_SIZE:
                raise InvalidArgumentError('Provided Id must not exceed {} bytes'.format_map(self.MAX_ID_SIZE))
        return custom_id

    def canonical_name(self, flow):
        return type(flow).__name__ if issubclass(type(flow), Version)
