import os

import pytest
from dotenv import load_dotenv

from zenaton.client import Client

# LOADING CONFIG FROM .env file
load_dotenv()
app_id = os.getenv('ZENATON_APP_ID')
api_token = os.getenv('ZENATON_API_TOKEN')
app_env = os.getenv('ZENATON_APP_ENV')

if not app_id:
    raise Exception('Please include your ZENATON_APP_ID in the .env file')

if not api_token:
    raise Exception('Please include your ZENATON_API_TOKEN in the .env file')

if not app_env:
    raise Exception('Please include your ZENATON_APP_ENV in the .env file')


@pytest.fixture
def client():
    return Client(app_id, api_token, app_env)
