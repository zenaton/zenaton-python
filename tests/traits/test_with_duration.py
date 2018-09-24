import pytest
import datetime


@pytest.mark.usefixtures("wait")
def test_get_duration(wait):
    wait.seconds(20)
    assert wait.get_duration() == 20.0
    wait.seconds(20)
    assert wait.get_duration() == 20.0 + 20.0
    wait.hours(10)
    assert wait.get_duration() == 20.0 + 20.0 + (10.0 * 3600)


@pytest.mark.usefixtures("wait")
def test_init_now_then(wait):
    now, now_dup = wait._WithDuration__init_now_then()
    assert type(now) is datetime.datetime
    assert type(now_dup) is datetime.datetime


@pytest.mark.usefixtures("wait")
def test_push(wait):
    wait.buffer = {}
    wait.seconds(10)
    assert wait.buffer['seconds'] == 10
    wait.seconds(10)
    assert wait.buffer['seconds'] == 20
    wait.hours(20)
    assert wait.buffer['hours'] == 20


@pytest.mark.usefixtures("wait")
def test_apply_duration(wait):
    time = datetime.datetime.now()
    assert (time + datetime.timedelta(seconds=10)) == wait._WithDuration__apply_duration('seconds', 10, time)


@pytest.mark.usefixtures("wait")
def test_diff_in_seconds(wait):
    now = datetime.datetime.now()
    now_plus_10 = now + datetime.timedelta(seconds=10)
    assert wait._WithDuration__diff_in_secondes(now, now_plus_10) == 10
