import pytest
import datetime

from zenaton.tasks.wait import Wait
from zenaton.exceptions import ExternalError


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
