import datetime
import itertools

import pytz

from .with_duration import WithDuration
from ..exceptions import ExternalError, InternalError


class WithTimestamp(WithDuration):
    WEEKDAYS = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
    MODE_AT = 'AT'  # When specifying a time
    MODE_WEEK_DAY = 'WEEK_DAY'  # When specifying a day of the week
    MODE_MONTH_DAY = 'MONTH_DAY'  # When specifying a day of the month
    MODE_TIMESTAMP = 'TIMESTAMP'  # When specifying a unix timestamp

    timezone = 'UTC'

    def get_timetamps_or_duration(self):
        pass

    def __apply(self, method, value, now, now_dup):
        pass

    def __weekday(self, value, day, now_dup):
        self.__set_mode(self.MODE_WEEK_DAY)
        for _ in itertools.repeat(None, value):
            now_dup = self.__next_weekday(now_dup, day)

    # https://stackoverflow.com/questions/6558535/
    def __next_weekday(self, d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)

    def __timestamp(self, timestamp):
        self.__set_mode(self.MODE_TIMESTAMP)
        return timestamp

    def __at(self, time, now, now_dup):
        self.__set_mode(self.MODE_AT)
        hour = int(time.hour)
        min = int(time.minute)
        sec = int(time.second)
        now_dup = now_dup.replace(hour=hour, minute=min, second=sec)
        if now > now_dup:
            nom += self.__delay()
        return now_dup

    def __delay(self):
        if self.mode == self.MODE_AT:
            return datetime.timedelta(days=1)
        elif self.mode == self.MODE_WEEK_DAY:
            return datetime.timedelta(weeks=1)
        elif self.mode == self.MODE_MONTH_DAY:
            return datetime.timedelta(months=1)
        else:
            raise InternalError('Unknown mode: {}'.format(self.mode))

    def __on_day(self, day, now, now_dup):
        self.__set_mode(self.MODE_MONTH_DAY)
        now_dup = now_dup.replace(day=day)
        if now > now_dup:
            now_dup = now_dup.replace(now_dup.month + 1)
        return now_dup

    def __set_mode(self, mode):
        if mode == self.mode or self.__is_timestamp_mode_set(mode):
            raise ExternalError('Incompatible definition in Wait methods')
        if self.mode is None:
            self.mode = mode
        else:
            self.mode = self.MODE_AT

    def __is_timestamp_mode_set(self, mode):
        return (self.mode is not None and self.MODE_TIMESTAMP == mode) or self.mode == self.MODE_TIMESTAMP

    def set_timezone(self, timezone):
        if not self.__is_valid_timezone(timezone):
            raise ExternalError('Unknown timezone')
        self.__class__.timezone = timezone

    def __is_valid_timezone(self, timezone):
        return timezone in pytz.all_timezones
