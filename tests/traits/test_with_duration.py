import pytest
import datetime


@pytest.mark.usefixtures("wait")
def test_get_duration(wait):

    def assert_duration():
        assert wait.get_duration() == duration

    wait.seconds(20)
    duration = 20.0
    assert_duration()
    wait.seconds(20)
    duration += 20
    assert wait.get_duration() == duration
    wait.hours(10)
    duration += (10 * 3600)
    assert wait.get_duration() == duration
    wait.days(1)
    duration += (24 * 3600)
    assert wait.get_duration() == duration
    wait.weeks(1)
    duration += (7 * 24 * 3600)
    assert wait.get_duration() == duration
    wait.months(1)
    duration28 = duration + (24 * 3600 * 28)
    duration31 = duration + (24 * 3600 * 31)
    duration += (24 * 3600 * 30)
    assert duration28 <= wait.get_duration() <= duration31
    wait.years(1)
    duration_31_full_year = duration31 + (24 * 3600 * 365)
    duration_28_leap_year = duration28 - (24 * 3600)
    assert duration_28_leap_year <= wait.get_duration() <= duration_31_full_year


@pytest.mark.usefixtures("wait")
def test_time_functions(wait):
    for name in ['seconds', 'minutes', 'hours', 'days', 'weeks']:
        getattr(wait, name)(1)
        assert wait.buffer[name] == 1
        getattr(wait, name)(1)
        assert wait.buffer[name] == 2
        wait.buffer = {}
    wait.months(1)
    assert 28 <= wait.buffer['days'] <= 31
    wait.months(1)
    assert 59 <= wait.buffer['days'] <= 62
    wait.buffer = {}
    wait.years(1)
    assert wait.buffer['days'] in [364, 365]
    wait.years(1)
    assert wait.buffer['days'] in [729, 730]


@pytest.mark.usefixtures("wait")
def test_add_months(wait):
    days = wait.months_to_days(1)
    assert 28 <= days <= 31
    days = wait.months_to_days(2)
    assert 56 <= days <= 62
    assert wait.months_to_days(12) == 365


@pytest.mark.usefixtures("wait")
def test_add_years(wait):
    days = wait.years_to_days(1)
    assert days in [364, 365]


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
