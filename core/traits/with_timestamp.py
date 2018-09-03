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
        if self.buffer is None:
            return [None, None]
        now, now_dup = self.__init_now_then()
        self.mode = None
        for (time_unit, time_value) in self.buffer.items():
            now_dup = self.__apply(time_unit, time_value, now, now_dup)
        if self.mode is None:
            return [None, self.diff_in_secondes(now, now_dup)]
        return [int(now_dup), None]

    def timestamp(self, value):
        return self.__push('timestamp', value)

    def at(self, value):
        return self.__push('at', value)

    def on_day(self, value):
        return self.__push('on_day', value)

    def monday(self, value):
        return self.__push('monday', value)

    def tuesday(self, value):
        return self.__push('tuesday', value)

    def wednesday(self, value):
        return self.__push('wednesday', value)

    def thursday(self, value):
        return self.__push('thursday', value)

    def friday(self, value):
        return self.__push('friday', value)

    def saturday(self, value):
        return self.__push('saturday', value)

    def sunday(self, value):
        return self.__push('sunday', value)

    def __apply(self, method, value, now, now_dup):
        if method in self.WEEKDAYS:
            return self.__weekday(value, method, now_dup)
        elif method == 'timestamp':
            return self.__timestamp(value)
        elif method == 'at':
            return self.at(value, now, now_dup)
        elif method == 'on_day':
            return self.on_day(value, now, now_dup)
        else:
            return self.__apply_duration(method, value, now)

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
            now += self.__delay()
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
