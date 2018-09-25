import copy
import datetime
import calendar

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

    # Inspired by https://stackoverflow.com/a/50301887
    def months_to_days(self, months):

        now = datetime.datetime.today().date()
        months_count = now.month + months

        year = now.year + int(months_count / 13)

        month = (months_count % 12)
        if month == 0:
            month = 12

        day = now.day
        last_day_of_month = calendar.monthrange(year, month)[1]
        if day > last_day_of_month:
            day = last_day_of_month

        new_date = datetime.date(year, month, day)

        return (new_date - now).days

    def months(self, value):
        days = self.months_to_days(value)
        self.__push('days', days)
        return self

    def years_to_days(self, years):
        return self.months_to_days(years * 12)

    def years(self, value):
        days = self.years_to_days(value)
        self.__push('days', days)
        return self

    def __init_now_then(self):
        tz = self.timezone if self.timezone else 'UTC'
        now = datetime.datetime.now(pytz.timezone(tz))
        return now, copy.deepcopy(now)

    def __push(self, key, value=1):
        if not hasattr(self, 'buffer'):
            self.buffer = {}
        if not self.buffer.get(key):
            self.buffer[key] = value
        else:
            self.buffer[key] += value

    def __apply_duration(self, time_unit, time_value, time):
        args = {str(time_unit): int(time_value)}
        return time + datetime.timedelta(**args)

    def __diff_in_secondes(self, before, after):
        return (after - before) / datetime.timedelta(seconds=1)
