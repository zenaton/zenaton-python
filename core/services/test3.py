"""import datetime, os
LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
print(LOCAL_TIMEZONE)
# print(os.environ[])



class Test:
    class_var = 1

    def __init__(self):
        pass

    def get_value(self):
        return self.class_var

    def set_value(self, value):
        self.__class__.class_var = value



test_instance1 = Test()
print(test_instance1.class_var)
test_instance1.set_value(value=2)
Test().set_value(value=2)
# Test.class_var = 2
test_instance2 = Test()
print(test_instance2.class_var)
print(test_instance1.class_var)

now = datetime.datetime.now()
print(now)
now = now.replace(day=23)
print(now)

print(now.month)"""


class WithDuration:
    def __test(self):
        print('__init_now_then')


class WithTimestamp(WithDuration):
    pass


class Wait(WithTimestamp):
    pass


# Wait().__test()

import time

print(time.time())
