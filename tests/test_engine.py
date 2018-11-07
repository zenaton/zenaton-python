import pytest
import pytest_mock

from zenaton.exceptions import InvalidArgumentError


class FakeTask:
    pass


@pytest.mark.usefixtures("engine")
def test_check_argument(engine):
    with pytest.raises(InvalidArgumentError):
        engine.check_argument(FakeTask)


@pytest.mark.usefixtures("engine", "task0", "sequential_workflow")
def test_valid_job(engine, sequential_workflow, task0):
    assert not engine.valid_job(FakeTask)
    assert engine.valid_job(sequential_workflow)
    assert engine.valid_job(task0)


@pytest.mark.usefixtures("client", "engine", "task0")
def test_dispatch_task(client, engine, task0, mocker):
    mocker.spy(client, "start_task")
    task0.dispatch()
    assert client.start_task.call_count == 1



