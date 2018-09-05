import copy
import datetime

import pytz


class WithDuration:

    def get_duration(self):
        if self.buffer is None:
            return
        now, now_dup = self.__init_now_then()
        for (time_unit, time_value) in self.buffer.items():
            now_dup = self.__apply_duration(time_unit, time_value, now_dup)
        return self.__diff_in_secondes(now, now_dup)

    def seconds(self, value):
        self.__push('seconds', value)
        return self

    def minutes(self, value):
        self.__push('minutes', value)
        return self

    def hours(self, value):
        self.__push('hours', value)
        return self

    def days(self, value):
        self.__push('days', value)
        return self

    def weeks(self, value):
        self.__push('weeks', value)
        return self

    def months(self, value):
        self.__push('months', value)
        return self

    def years(self, value):
        self.__push('years', value)
        return self

    def __init_now_then(self):
        tz = self.timezone if self.timezone else 'UTC'
        now = datetime.datetime.now(pytz.timezone(tz))
        return now, copy.deepcopy(now)

    def __push(self, key, value=1):
        if not hasattr(self, 'buffer') is None:
            self.buffer = {}
        self.buffer[key] = value

    def __apply_duration(self, time_unit, time_value, time):
        args = {str(time_unit): int(time_value)}
        return time + datetime.timedelta(**args)

    def __diff_in_secondes(self, before, after):
        return (after - before) / datetime.timedelta(seconds=1)
