from core.services.http_service import HttpService

class client:

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

    PROG = 'Ruby' # The current programming language

    EVENT_INPUT = 'event_input' # Parameter name for event data
    EVENT_NAME = 'event_name' # Parameter name for event name

    WORKFLOW_KILL = 'kill' # Worker update mode to stop a worker
    WORKFLOW_PAUSE = 'pause' # Worker udpate mode to pause a worker
    WORKFLOW_RUN = 'run' # Worker update mode to resume a worker

    def __init__(self, appId, apiToken, appEnv):
        self.appId = appId
        self.apiToken = apiToken
        self.appEnv = appEnv

