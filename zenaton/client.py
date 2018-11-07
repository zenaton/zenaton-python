import json
import os
import urllib

from .abstracts.workflow import Workflow
from .exceptions import InvalidArgumentError
from .services.http_service import HttpService
from .services.properties import Properties
from .services.serializer import Serializer
from .singleton import Singleton
from .workflows.version import Version


class Client(metaclass=Singleton):
    ZENATON_API_URL = 'https://api.zenaton.com/v1'  # Zenaton api url
    ZENATON_WORKER_URL = 'http://localhost'  # Default worker url
    DEFAULT_WORKER_PORT = 4001  # Default worker port
    WORKER_API_VERSION = 'v_newton'  # Default worker api version

    MAX_ID_SIZE = 256  # Limit on length of custom ids

    APP_ENV = 'app_env'  # Parameter name for the application environment
    APP_ID = 'app_id'  # Parameter name for the application ID
    API_TOKEN = 'api_token'  # Parameter name for the API token

    ATTR_ID = 'custom_id'  # Parameter name for custom ids
    ATTR_NAME = 'name'  # Parameter name for workflow names
    ATTR_CANONICAL = 'canonical_name' # Parameter name for version name
    ATTR_DATA = 'data'  # Parameter name for json payload
    ATTR_PROG = 'programming_language'  # Parameter name for the language
    ATTR_MODE = 'mode'  # Parameter name for the worker update mode
    ATTR_MAX_PROCESSING_TIME = 'max_processing_time' # Pararameter name for the max processing time

    PROG = 'Python'  # The current programming language

    EVENT_INPUT = 'event_input'  # Parameter name for event data
    EVENT_NAME = 'event_name'  # Parameter name for event name

    WORKFLOW_KILL = 'kill'  # Worker update mode to stop a worker
    WORKFLOW_PAUSE = 'pause'  # Worker udpate mode to pause a worker
    WORKFLOW_RUN = 'run'  # Worker update mode to resume a worker

    def __init__(self, app_id, api_token, app_env):
        self.app_id = app_id
        self.api_token = api_token
        self.app_env = app_env
        self.http = HttpService()
        self.serializer = Serializer()
        self.properties = Properties()

    """
        Gets the url for the workers
        :param String resource the endpoint for the worker
        :param String params url encoded parameters to include in request
        :returns String the workers url with parameters
    """
    def worker_url(self, resource='', params=''):
        base_url = os.environ.get('ZENATON_WORKER_URL') or self.ZENATON_WORKER_URL
        port = os.environ.get('ZENATON_WORKER_PORT') or self.DEFAULT_WORKER_PORT
        url = '{}:{}/api/{}/{}?'.format(base_url, port, self.WORKER_API_VERSION, resource)
        return self.add_app_env(url, params)

    """
        Gets the url for zenaton api
        :param String resource the endpoint for the api
        :param String params url encoded parameters to include in request
        :returns String the api url with parameters
    """
    def website_url(self, resource='', params=''):
        api_url = os.environ.get('ZENATON_API_URL') or self.ZENATON_API_URL
        url = '{}/{}?{}={}&'.format(api_url, resource, self.API_TOKEN, self.api_token)
        return self.add_app_env(url, params)

    def send_event_url(self):
        return self.worker_url('events')

    """
        Start the specified workflow
        :params .abstracts.workflow.Workflow flow
    """
    def start_workflow(self, flow):
        return self.http.post(self.instance_worker_url(),
                              data=json.dumps({
                                  self.ATTR_PROG: self.PROG,
                                  self.ATTR_CANONICAL: self.canonical_name(flow),
                                  self.ATTR_NAME: self.class_name(flow),
                                  self.ATTR_DATA: self.serializer.encode(self.properties.from_(flow)),
                                  self.ATTR_ID: self.parse_custom_id_from(flow)
                       }))

    def start_task(self, task):
        return self.http.post(self.worker_url('tasks'),
                              data=json.dumps({
                                  self.ATTR_PROG: self.PROG,
                                  self.ATTR_NAME: self.class_name(task),
                                  self.ATTR_DATA: self.serializer.encode(self.properties.from_(task)),
                                  self.ATTR_MAX_PROCESSING_TIME: task.max_processing_time() if hasattr(task, 'max_processing_time') else None
                       }))

    def update_instance(self, workflow, custom_id, mode):
        params = '{}={}'.format(self.ATTR_ID, custom_id)
        url = self.instance_worker_url(params)
        options = json.dumps({
            self.ATTR_PROG: self.PROG,
            self.ATTR_NAME: workflow.__name__,
            self.ATTR_MODE: mode
        })
        return self.http.put(url, options)

    """
        Sends an event to a workflow
        :param String workflow_name  the class name of the workflow
        :param String custom_id the custom ID of the workflow (if any)
        :param .abstracts.Event event the event to send
        :returns None
    """
    def send_event(self, workflow_name, custom_id, event):
        body = json.dumps({
            self.ATTR_PROG: self.PROG,
            self.ATTR_NAME: workflow_name,
            self.ATTR_ID: custom_id,
            self.EVENT_NAME: type(event).__name__,
            self.EVENT_INPUT: self.serializer.encode(self.properties.from_(event)),
        })
        return self.http.post(self.send_event_url(), body)

    """
        Finds a workflow
        :param String workflow_name the class name of the workflow
        :param String custom_id the custom ID of the workflow (if any)
        :return .abstracts.workflow.Workflow
    """

    def find_workflow(self, workflow, custom_id):

        params = '{}={}&{}={}&{}={}'.format(
            self.ATTR_ID,
            custom_id,
            self.ATTR_NAME,
            workflow.__name__,
            self.ATTR_PROG,
            self.PROG)
        response = self.http.get(self.instance_website_url(params))

        if response.get('data', None) is not None:
            data = response['data']
            return self.properties.object_from(
                workflow,
                self.serializer.decode(data['properties']),
                Workflow
            )
        else:
            return None

    """
        Stops a workflow
        :param String workflow_name the class name of the workflow
        :param String custom_id the custom ID of the workflow, if any
        :returns None
    """
    def kill_workflow(self, workflow_name, custom_id):
        return self.update_instance(workflow_name, custom_id, self.WORKFLOW_KILL)

    """
        Pauses a workflow
        :param String workflow_name the class name of the workflow
        :param String custom_id the custom ID of the workflow, if any
        :returns None
    """
    def pause_workflow(self, workflow_name, custom_id):
        return self.update_instance(workflow_name, custom_id, self.WORKFLOW_PAUSE)

    """
        Resumes a workflow
        :param String workflow_name the class name of the workflow
        :param String custom_id the custom ID of the workflow, if any
        :returns None
    """
    def resume_workflow(self, workflow_name, custom_id):
        return self.update_instance(workflow_name, custom_id, self.WORKFLOW_RUN)

    def instance_website_url(self, params=''):
        return self.website_url('instances', params)

    def instance_worker_url(self, params=''):
        return self.worker_url('instances', params)

    def add_app_env(self, url, params):
        app_env = '{}={}&'.format(self.APP_ENV, self.app_env) if self.app_env else ''
        app_id = '{}={}&'.format(self.APP_ID, self.app_id) if self.app_id else ''
        return '{}{}{}{}'.format(url, app_env, app_id, urllib.parse.quote_plus(params, safe='=&'))

    def parse_custom_id_from(self, flow):
        custom_id = flow.id()
        if custom_id is not None:
            if not isinstance(custom_id, str) and not isinstance(custom_id, int):
                raise InvalidArgumentError('Provided ID must be a string or an integer')
            custom_id = str(custom_id)
            if len(custom_id) > self.MAX_ID_SIZE:
                raise InvalidArgumentError('Provided Id must not exceed {} bytes'.format(self.MAX_ID_SIZE))
        return custom_id

    def canonical_name(self, flow):
        return type(flow).__name__ if issubclass(type(flow), Version) else None

    def class_name(self, flow):
        if issubclass(type(flow), Version):
            return type(flow.current_implementation()).__name__
        return type(flow).__name__
