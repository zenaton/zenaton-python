import copy
import datetime
import pytest

from freezegun import freeze_time
import pytz

from zenaton.exceptions import ExternalError
from zenaton.tasks.wait import Wait
from zenaton.traits.with_timestamp import WithTimestamp


@freeze_time("2017-02-03 12:00:00")
@pytest.mark.usefixtures("wait")
def test_get_timetamp_or_duration_day_of_month_overflow_pos(wait):
    now = datetime.datetime.now()
    with pytest.raises(ValueError):
        wait.day_of_month(32)
        wait.get_timetamp_or_duration()


@freeze_time("2017-02-03 12:00:00")
@pytest.mark.usefixtures("wait")
def test_get_timetamp_or_duration_day_of_month_overflow_zero(wait):
    now = datetime.datetime.now()
    with pytest.raises(ValueError):
        wait.day_of_month(0)
        wait.get_timetamp_or_duration()


@freeze_time("2017-02-03 12:00:00")
@pytest.mark.usefixtures("wait")
def test_get_timetamp_or_duration_day_of_month_overflow_neg(wait):
    now = datetime.datetime.now()
    with pytest.raises(ValueError):
        wait.day_of_month(-1)
        wait.get_timetamp_or_duration()


@freeze_time("2017-02-03 12:00:00")
@pytest.mark.usefixtures("wait")
def test_get_timetamp_or_duration_day_of_month_end_of_month_no_skip(wait):
    wait.day_of_month(28)
    assert wait.get_timetamp_or_duration()[0] == 1488283200  # i.e: "2017-02-28 12:00:00"


@freeze_time("2017-02-03 12:00:00")
@pytest.mark.usefixtures("wait")
def test_get_timetamp_or_duration_day_of_month_end_of_month_next(wait):
    wait.day_of_month(1)
    assert wait.get_timetamp_or_duration()[0] == 1488369600  # i.e: "2017-03-01 12:00:00"


@freeze_time("2017-02-03 12:00:00")
@pytest.mark.usefixtures("wait")
def test_get_timetamp_or_duration_day_of_month_end_of_month_skip(wait):
    wait.day_of_month(31)
    assert wait.get_timetamp_or_duration()[0] == 1490961600 # i.e: "2017-03-31 12:00:00"


@pytest.mark.usefixtures("wait")
@freeze_time("2017-02-03 12:01:02")  # It's a Friday.
def test_get_timetamp_or_duration_next_weekday(wait):
    wait2 = copy.deepcopy(wait)
    now = datetime.datetime.now(pytz.timezone('Europe/Paris'))
    now_day = (now.weekday() + 1) % 7
    weekday = WithTimestamp.WEEKDAYS[now.weekday()]
    getattr(wait2, weekday)()
    assert wait2.get_timetamp_or_duration()[0] - int(now.timestamp()) == (7 * 24 * 60 * 60)
    for i in range(1, 6):
        new_wait = copy.deepcopy(wait)
        getattr(new_wait, new_wait.WEEKDAYS[now_day])(i)
        assert new_wait.get_timetamp_or_duration()[0] - int(now.timestamp()) == (24 * 60 * 60) * (1 + (7 * (i - 1)))


@pytest.mark.usefixtures("wait")
@freeze_time("2017-02-03 11:01:02")  # It's a Friday, and 11:01 UTC is 12:01 in Paris that day.
def test_get_timetamp_or_duration_weekday(wait):
    wait2 = copy.deepcopy(wait)
    now = datetime.datetime.now(pytz.timezone('Europe/Paris'))
    wait.friday().at("13:01:02")
    assert wait.get_timetamp_or_duration()[0] - int(now.timestamp()) == (60 * 60)
    wait2.friday().at("11:01:02")
    assert wait2.get_timetamp_or_duration()[0] - int(now.timestamp()) == (7 * 24 * 60 * 60) - (60 * 60)


@pytest.mark.usefixtures("wait")
@freeze_time("2017-02-03 11:01:02")
def test_get_timetamp_or_duration_day_of_month(wait):
    wait2 = copy.deepcopy(wait)
    wait3 = copy.deepcopy(wait)
    now = datetime.datetime.now(pytz.timezone('Europe/Paris'))
    wait.day_of_month(now.day + 1)
    assert wait.get_timetamp_or_duration()[0] - int(now.timestamp()) == 24 * 60 * 60
    wait2.day_of_month(now.day - 1)
    wait_duration = wait2.get_timetamp_or_duration()[0] - int(now.timestamp())
    assert 27 * 24 * 60 * 60 <= wait_duration <= 30 * 24 * 60 * 60
    wait3.day_of_month(now.day)
    wait_duration = wait3.get_timetamp_or_duration()[0] - int(now.timestamp())
    assert 28 * 24 * 60 * 60 <= wait_duration <= 31 * 24 * 60 * 60


@pytest.mark.usefixtures("wait")
@freeze_time("2017-02-03 11:01:02")  # 11:01 UTC is actually 12:01 Paris time that day.
def test_get_timetamp_or_duration_day_of_month_at(wait):
    wait2 = copy.deepcopy(wait)
    now = datetime.datetime.now(pytz.timezone('Europe/Paris'))
    wait.day_of_month(3).at("13:01:02")
    assert wait.get_timetamp_or_duration()[0] - int(now.timestamp()) == 60 * 60
    wait2.day_of_month(3).at("11:01:02")
    assert 28 * 24 * 60 * 60 - 60 * 60 == wait2.get_timetamp_or_duration()[0] - int(now.timestamp())


@pytest.mark.usefixtures("wait")
@freeze_time("2017-02-03 11:01:02")  # 11:01 UTC is actually 12:01 Paris time that day.
def test_get_timetamp_or_duration_at(wait):
    now = datetime.datetime.now(pytz.timezone('Europe/Paris'))
    wait.set_timezone('Europe/Paris')
    wait.at('13:01:02')
    assert wait.get_timetamp_or_duration()[0] - int(now.timestamp()) == 60 * 60


@pytest.mark.usefixtures("wait")
def test_get_timetamp_or_duration_timestamp(wait):
    now_timestamp = int(datetime.datetime.now().timestamp())
    wait.timestamp(now_timestamp + 10.0)
    assert wait.get_timetamp_or_duration()[0] - now_timestamp == 10


@pytest.mark.usefixtures("wait")
def test_get_timetamp_push(wait):
    for name in ['timestamp', 'at', 'day_of_month', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
                 'sunday']:
        getattr(wait, name)(1)
        assert wait.buffer.get(name, None)


@pytest.mark.usefixtures("wait")
def test_set_mode(wait):
    wait._WithTimestamp__set_mode(wait.MODE_WEEK_DAY)
    assert wait.mode == wait.MODE_WEEK_DAY
    with pytest.raises(ExternalError):
        wait._WithTimestamp__set_mode(wait.MODE_WEEK_DAY)
    wait._WithTimestamp__set_mode(wait.MODE_MONTH_DAY)
    assert wait.mode == wait.MODE_AT


@pytest.mark.usefixtures("wait")
def test_is_timestamp_mode_set(wait):
    wait.mode = wait.MODE_WEEK_DAY
    assert not wait._WithTimestamp__is_timestamp_mode_set(wait.MODE_WEEK_DAY)
    assert wait._WithTimestamp__is_timestamp_mode_set(wait.MODE_TIMESTAMP)
    assert not wait._WithTimestamp__is_timestamp_mode_set(wait.MODE_WEEK_DAY)


@pytest.mark.usefixtures("wait")
def test_set_timezone(wait):
    wait.set_timezone('Africa/Libreville')
    assert wait.timezone == 'Africa/Libreville'
    new_wait = Wait()
    assert new_wait.timezone == 'Africa/Libreville'
    with pytest.raises(ExternalError):
        wait.set_timezone('Africa/Leconi')


@pytest.mark.usefixtures("wait")
def test_valid_timezone(wait):
    assert wait._WithTimestamp__is_valid_timezone('Africa/Libreville')
    assert not wait._WithTimestamp__is_valid_timezone('Africa/Mvengué')
