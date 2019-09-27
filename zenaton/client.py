from contextlib import contextmanager
import json
import os
import urllib
import uuid

from .abstracts.workflow import Workflow
from .exceptions import InvalidArgumentError, ExternalError
from .services.http_service import HttpService
from .services.graphql_service import GraphQLService
from .services.properties import Properties
from .services.serializer import Serializer
from .singleton import Singleton
from .workflows.version import Version


class Client(metaclass=Singleton):
    ZENATON_API_URL = 'https://api.zenaton.com/v1'  # Zenaton api url
    ZENATON_WORKER_URL = 'http://localhost'  # Default worker url
    ZENATON_GATEWAY_URL = "https://gateway.zenaton.com/api"; # Zenaton gateway url
    DEFAULT_WORKER_PORT = 4001  # Default worker port
    WORKER_API_VERSION = 'v_newton'  # Default worker api version

    MAX_ID_SIZE = 256  # Limit on length of custom ids

    APP_ENV = 'app_env'  # Parameter name for the application environment
    APP_ID = 'app_id'  # Parameter name for the application ID
    API_TOKEN = 'api_token'  # Parameter name for the API token

    PROG = 'PYTHON'  # The current programming language

    def __init__(self, app_id='', api_token='', app_env=''):
        self.app_id = app_id
        self.api_token = api_token
        self.app_env = app_env
        self.graphql = GraphQLService()
        self.serializer = Serializer()
        self.properties = Properties()

    def __lazy_init__(self, app_id, api_token, app_env):
        self.app_id = self.app_id or app_id
        self.api_token = self.api_token or api_token
        self.app_env = self.app_env or app_env

    """
        Gets the gateway url (GraphQL API)
        :returns String the gateway url
    """
    def gateway_url(self):
        url = os.environ.get('ZENATON_GATEWAY_URL') or self.ZENATON_GATEWAY_URL
        return url

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
        if not self.api_token:
            raise ValueError('Client not initialized to access website: missing an API token.')
        url = '{}/{}?{}={}&'.format(api_url, resource, self.API_TOKEN, self.api_token)
        return self.add_app_env(url, params)

    """
        Start the specified workflow
        :params .abstracts.workflow.Workflow flow
    """
    def start_workflow(self, flow):
        query = self.graphql.DISPATCH_WORKFLOW
        variables = {
            'input': {
                'intent_id': self.uuid(),
                'environment_name': self.app_env,
                'programming_language': self.PROG,
                'custom_id': self.parse_custom_id_from(flow),
                'name': self.class_name(flow),
                'canonical_name': self.canonical_name(flow),
                'data': self.serializer.encode(self.properties.from_(flow))
            }
        }
        return self.gateway_request(query, variables=variables, data_response_key="dispatchWorkflow")

    def start_task(self, task):
        query = self.graphql.DISPATCH_TASK
        variables = {
            'input': {
                'intent_id': self.uuid(),
                'environment_name': self.app_env,
                'programming_language': self.PROG,
                'max_processing_time': task.max_processing_time() if hasattr(task, 'max_processing_time') else None,
                'name': self.class_name(task),
                'data': self.serializer.encode(self.properties.from_(task))
            }
        }
        return self.gateway_request(query, variables=variables, data_response_key="dispatchTask")

    def start_scheduled_workflow(self, flow, cron):
        query = self.graphql.CREATE_WORKFLOW_SCHEDULE
        variables = {
            'input': {
                'intent_id': self.uuid(),
                'environment_name': self.app_env,
                'cron': cron,
                'customId': self.parse_custom_id_from(flow),
                'workflowName': self.class_name(flow),
                'canonicalName': self.canonical_name(flow) or self.class_name(flow),
                'programmingLanguage': self.PROG,
                'properties': self.serializer.encode(self.properties.from_(flow))
            }
        }
        return self.gateway_request(query, variables=variables, data_response_key="createWorkflowSchedule")

    def start_scheduled_task(self, task, cron):
        query = self.graphql.CREATE_TASK_SCHEDULE
        variables = {
            'input': {
                'intent_id': self.uuid(),
                'environment_name': self.app_env,
                'cron': cron,
                'task_name': self.class_name(task),
                'programming_language': self.PROG,
                'properties': self.serializer.encode(self.properties.from_(task))
            }
        }
        return self.gateway_request(query, variables=variables, data_response_key="createTaskSchedule")

    """
        Sends an event to a workflow
        :param String workflow_name  the class name of the workflow
        :param String custom_id the custom ID of the workflow (if any)
        :param .abstracts.Event event the event to send
        :returns None
    """
    def send_event(self, workflow_name, custom_id, event):
        query = self.graphql.SEND_EVENT
        variables = {
            'input': {
                'intent_id': self.uuid(),
                'custom_id': custom_id,
                'environment_name': self.app_env,
                'programming_language': self.PROG,
                'name': type(event).__name__,
                'input': self.serializer.encode(self.properties.from_(event)),
                'workflow_name': workflow_name,
                'data': self.serializer.encode(event)
            }
        }
        return self.gateway_request(query, variables=variables, data_response_key="sendEventToWorkflowByNameAndCustomId")

    """
        Finds a workflow
        :param String workflow_name the class name of the workflow
        :param String custom_id the custom ID of the workflow (if any)
        :return .abstracts.workflow.Workflow
    """

    def find_workflow(self, workflow, custom_id):
        query = self.graphql.FIND_WORKFLOW
        variables = {
            'custom_id': custom_id,
            'environment_name': self.app_env,
            'programming_language': self.PROG,
            'name': workflow.__name__
        }
        res = self.gateway_request(query, variables=variables, data_response_key="findWorkflow", throw_on_error=False)
        errors = self.get_graphql_errors(res)
        if errors:
            if self.contains_not_found_error(errors):
                return None
            else:
                raise ExternalError(errors)

        return self.properties.object_from(
                workflow,
                self.serializer.decode(res['properties']),
                Workflow
            )

    """
        Stops a workflow
        :param .abstracts.workflow.Workflow workflow
        :param String custom_id the custom ID of the workflow, if any
        :returns None
    """
    def kill_workflow(self, workflow, custom_id):
        query = self.graphql.KILL_WORKFLOW
        variables = {
            'input': {
                'intent_id': self.uuid(),
                'environment_name': self.app_env,
                'programming_language': self.PROG,
                'custom_id': custom_id,
                'name': workflow.__name__
            }
        }
        return self.gateway_request(query, variables=variables, data_response_key="killWorkflow")

    """
        Pauses a workflow
        :param .abstracts.workflow.Workflow flow
        :param String custom_id the custom ID of the workflow, if any
        :returns None
    """
    def pause_workflow(self, workflow, custom_id):
        query = self.graphql.PAUSE_WORKFLOW
        variables = {
            'input': {
                'intent_id': self.uuid(),
                'environment_name': self.app_env,
                'programming_language': self.PROG,
                'custom_id': custom_id,
                'name': workflow.__name__
            }
        }
        return self.gateway_request(query, variables=variables, data_response_key="pauseWorkflow")

    """
        Resumes a workflow
        :param .abstracts.workflow.Workflow flow
        :param String custom_id the custom ID of the workflow, if any
        :returns None
    """
    def resume_workflow(self, workflow, custom_id):
        query = self.graphql.RESUME_WORKFLOW
        variables = {
            'input': {
                'intent_id': self.uuid(),
                'environment_name': self.app_env,
                'programming_language': self.PROG,
                'custom_id': custom_id,
                'name': workflow.__name__
            }
        }
        return self.gateway_request(query, variables=variables, data_response_key="resumeWorkflow")

    def instance_website_url(self, params=''):
        return self.website_url('instances', params)

    def instance_worker_url(self, params=''):
        return self.worker_url('instances', params)

    def add_app_env(self, url, params):
        app_env = '{}={}&'.format(self.APP_ENV, self.app_env) if self.app_env else ''
        app_id = '{}={}&'.format(self.APP_ID, self.app_id) if self.app_id else ''
        return '{}{}{}{}'.format(url, app_env, app_id, urllib.parse.quote_plus(params, safe='=&'))

    def gateway_headers(self):
        return {'Accept': 'application/json',
                'Content-type': 'application/json',
                'app-id': self.app_id,
                'api-token': self.api_token}

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
        return type(flow).__name__ if isinstance(flow, Version) else None

    def class_name(self, flow):
        if issubclass(type(flow), Version):
            return type(flow.current_implementation()).__name__
        return type(flow).__name__

    def gateway_request(self, query, variables=None, data_response_key=None, throw_on_error=True):
        url = self.gateway_url()
        headers = self.gateway_headers()
        res = self.graphql.request(url, query, variables=variables, headers=headers)

        errors = self.get_graphql_errors(res)
        if errors:
            if throw_on_error:
                raise ExternalError(errors)
            else:
                return res

        if data_response_key:
            return res['data'][data_response_key]
        else:
            return res['data']

    def contains_not_found_error(self, errors):
        not_found_errors = list(filter(lambda error: error.get('type') == 'NOT_FOUND', errors))
        return len(not_found_errors) > 0

    def get_graphql_errors(self, response):
        errors = response.get('errors')
        if isinstance(errors, list) and len(errors) > 0:
            for error in errors:
                if 'locations' in error:
                    del error['locations']
        return errors

    @contextmanager
    def _connect_to_agent(self):
        """Display nice error message if connection to agent fails."""
        try:
            yield
        except ConnectionError:
            url = os.environ.get('ZENATON_WORKER_URL') or self.ZENATON_WORKER_URL
            port = os.environ.get('ZENATON_WORKER_PORT') or self.DEFAULT_WORKER_PORT
            raise ConnectionError(
                'Could not connect to Zenaton agent at "{}:{}", make sure it is running and '
                'listening.'.format(url, port))

    def uuid(self):
        """Generate a uuidv4"""
        return str(uuid.uuid4())
