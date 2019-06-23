import pytest

from zenaton.engine import Engine
from zenaton.client import Client


import os

import pytest
from dotenv import load_dotenv

from zenaton.client import Client

# LOADING CONFIG FROM .env file
load_dotenv()
app_id = os.getenv('ZENATON_APP_ID')
api_token = os.getenv('ZENATON_API_TOKEN')
app_env = os.getenv('ZENATON_APP_ENV')

@pytest.fixture
def engine():
    Client(app_id, api_token, app_env)
    return Engine()
