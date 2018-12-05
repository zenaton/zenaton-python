import pytest

from zenaton.exceptions import InvalidArgumentError
from zenaton.client import Client

from .utils import validate_url


@pytest.mark.usefixtures("client")
def test_url_functions(client):
    assert validate_url(client.worker_url())
    assert validate_url(client.send_event_url())
    assert validate_url(client.instance_website_url())
    assert validate_url(client.instance_worker_url())


@pytest.mark.usefixtures("client", "sequential_workflow")
def test_class_name(client, sequential_workflow):
    assert type(client.class_name(sequential_workflow)) == str


@pytest.mark.usefixtures("client", "sequential_workflow", "version_workflow")
def test_canonical_name(client, sequential_workflow, version_workflow):
    assert client.canonical_name(sequential_workflow) is None
    assert type(client.canonical_name(version_workflow)) == str


@pytest.mark.usefixtures("client", "sequential_workflow")
def test_parse_custom_id_from(client, sequential_workflow):
    assert type(client.parse_custom_id_from(sequential_workflow)) == str
    sequential_workflow.set_id(0)
    assert type(client.parse_custom_id_from(sequential_workflow)) == str
    sequential_workflow.set_id({})
    with pytest.raises(InvalidArgumentError):
        client.parse_custom_id_from(sequential_workflow)
    with pytest.raises(InvalidArgumentError):
        sequential_workflow.set_id('A' * (Client.MAX_ID_SIZE + 1))
        client.parse_custom_id_from(sequential_workflow)


@pytest.mark.usefixtures("client", "sequential_workflow")
def test_workflow_lifecycle(client, sequential_workflow):
    response = client.start_workflow(sequential_workflow)
    assert response['status_code'] == 201
    response = client.pause_workflow(type(sequential_workflow), sequential_workflow.id())
    assert response['status_code'] == 200
    response = client.resume_workflow(type(sequential_workflow), sequential_workflow.id())
    assert response['status_code'] == 200
    worfklow = client.find_workflow(type(sequential_workflow), sequential_workflow.id())
    assert type(worfklow) == type(sequential_workflow)
    assert worfklow.id() == sequential_workflow.id()
    response = client.kill_workflow(type(sequential_workflow), sequential_workflow.id())
    assert response['status_code'] == 200


@pytest.mark.usefixtures("client", "sequential_workflow", "my_event")
def test_event_workflow_lifecycle(client, sequential_workflow, my_event):
    sequential_workflow.set_id('MyEventWorkflow')
    response = client.start_workflow(sequential_workflow)
    assert response['status_code'] == 201
    response = client.send_event(type(sequential_workflow).__name__, sequential_workflow.id(), my_event)
    assert response['status_code'] == 200
    response = client.kill_workflow(type(sequential_workflow), sequential_workflow.id())
    assert response['status_code'] == 200


def test_url_params_encoding(client):
    assert client.add_app_env('', 'workflow_id').endswith('workflow_id')
    assert client.add_app_env('', 'yann+1@zenaton.com').endswith('&yann%2B1%40zenaton.com')