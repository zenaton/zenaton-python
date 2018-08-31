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

    def minutes(self, value):
        self.__push('minutes', value)

    def hours(self, value):
        self.__push('hours', value)

    def days(self, value):
        self.__push('days', value)

    def weeks(self, value):
        self.__push('weeks', value)

    def months(self, value):
        self.__push('months', value)

    def years(self, value):
        self.__push('years', value)

    def __init_now_then(self):
        tz = self.timezone if self.timezone else 'UTC'
        now = datetime.datetime.now(pytz.timezone(tz))
        return now, copy.deepcopy(now)

    def __push(self, key, value=1):
        if self.buffer is None:
            self.buffer = {}
        else:
            self.buffer[key] = value

    def __apply_duration(self, time_unit, time_value, time):
        return time + datetime.timedelta(time_unit=time_value)

    def __diff_in_secondes(self, before, after):
        return int(after - before)
