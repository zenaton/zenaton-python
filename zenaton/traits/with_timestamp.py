import datetime
import itertools

import pytz

from .with_duration import WithDuration
from ..exceptions import ExternalError, InternalError


class WithTimestamp(WithDuration):
    WEEKDAYS = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    MODE_AT = 'AT'  # When specifying a time
    MODE_WEEK_DAY = 'WEEK_DAY'  # When specifying a day of the week
    MODE_MONTH_DAY = 'MONTH_DAY'  # When specifying a day of the month
    MODE_TIMESTAMP = 'TIMESTAMP'  # When specifying a unix timestamp

    timezone = 'UTC'

    HAS_DAY = False

    def get_timetamp_or_duration(self):
        if getattr(self, 'buffer', None) is None:
            return [None, None]
        now, now_dup = self._WithDuration__init_now_then()
        self.mode = None
        for (time_unit, time_value) in sorted(self.buffer.items(), key=lambda kv: kv[0]):
            now_dup = self.__apply(time_unit, time_value, now, now_dup)
        if self.mode is None:
            return [None, self._WithDuration__diff_in_secondes(now, now_dup)]
        if self.mode == self.MODE_TIMESTAMP:
            return [int(now_dup), None]
        return [int(now_dup.timestamp()), None]

    def timestamp(self, value):
        self._WithDuration__push('timestamp', value)
        return self

    def at(self, value):
        self._WithDuration__push('at', value)
        return self

    def day_of_month(self, value):
        self._WithDuration__push('day_of_month', value)
        return self

    def monday(self, value=1):
        self.HAS_DAY = True
        self._WithDuration__push('monday', value)
        return self

    def tuesday(self, value=1):
        self.HAS_DAY = True
        self._WithDuration__push('tuesday', value)
        return self

    def wednesday(self, value=1):
        self.HAS_DAY = True
        self._WithDuration__push('wednesday', value)
        return self

    def thursday(self, value=1):
        self.HAS_DAY = True
        self._WithDuration__push('thursday', value)
        return self

    def friday(self, value=1):
        self.HAS_DAY = True
        self._WithDuration__push('friday', value)
        return self

    def saturday(self, value=1):
        self.HAS_DAY = True
        self._WithDuration__push('saturday', value)
        return self

    def sunday(self, value=1):
        self.HAS_DAY = True
        self._WithDuration__push('sunday', value)
        return self

    def __apply(self, method, value, now, now_dup):
        if method in self.WEEKDAYS:
            return self.__weekday(value, method, now_dup)
        elif method == 'timestamp':
            return self.__timestamp(value)
        elif method == 'at':
            return self.__at(value, now, now_dup)
        elif method == 'day_of_month':
            return self.__day_of_month(value, now, now_dup)
        else:
            return self._WithDuration__apply_duration(method, value, now)

    def __weekday(self, value, day, now_dup):
        self.__set_mode(self.MODE_WEEK_DAY)
        for _ in itertools.repeat(None, value):
            now_dup = self.__next_weekday(now_dup, day)
        return now_dup

    # https://stackoverflow.com/questions/6558535/
    def __next_weekday(self, d, weekday):
        weekday = self.WEEKDAYS.index(weekday)
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)

    def __timestamp(self, timestamp):
        self.__set_mode(self.MODE_TIMESTAMP)
        return timestamp

    def __at(self, time, now, now_dup):
        self.__set_mode(self.MODE_AT)
        hour, minute, second = time.split(':')
        hour, minute, second = int(hour), int(minute), int(second)
        now_dup = now_dup.replace(hour=hour, minute=minute, second=second)
        if now > now_dup:
            now_dup += self.__delay()
        elif self.HAS_DAY:
            now_dup -= datetime.timedelta(weeks=1)
        return now_dup

    def __delay(self):
        if self.mode == self.MODE_AT:
            return datetime.timedelta(days=1)
        elif self.mode == self.MODE_WEEK_DAY:
            return datetime.timedelta(weeks=1)
        elif self.mode == self.MODE_MONTH_DAY:
            days = self.months_to_days(1)
            return datetime.timedelta(days=days)
        else:
            raise InternalError('Unknown mode: {}'.format(self.mode))

    def __day_of_month(self, day, now, now_dup):
        self.__set_mode(self.MODE_MONTH_DAY)
        now_dup = now_dup.replace(day=day)
        if now >= now_dup:
            if now_dup.month > 11:
                now_dup = now_dup.replace(month=1, year=now_dup.year + 1)
            else:
                now_dup = now_dup.replace(month=now_dup.month + 1)
        return now_dup

    def __set_mode(self, mode):
        if not hasattr(self, 'mode') or self.mode is None:
            self.mode = mode
            return
        if mode == self.mode or self.__is_timestamp_mode_set(mode):
            raise ExternalError('Incompatible definition in Wait methods')
        else:
            self.mode = self.MODE_AT

    def __is_timestamp_mode_set(self, mode):
        return (self.mode is not None and self.MODE_TIMESTAMP == mode) or self.mode == self.MODE_TIMESTAMP

    def set_timezone(self, timezone):
        if not self.__is_valid_timezone(timezone):
            raise ExternalError('Unknown timezone')
        self.__class__.timezone = timezone
        return self

    def __is_valid_timezone(self, timezone):
        return timezone in pytz.all_timezones
