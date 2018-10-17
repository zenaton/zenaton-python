import pytest
import json
import datetime


@pytest.mark.usefixtures("serializer")
def test_str(serializer):
    str_ = 'foo bar'
    assert '{"d": "foo bar", "s": []}' == serializer.encode(str_)
    assert serializer.decode('{"d": "foo bar", "s": []}') == str_

    empty_str_ = ''
    assert '{"d": "", "s": []}' == serializer.encode(empty_str_)
    assert serializer.decode('{"d": "", "s": []}') == empty_str_


@pytest.mark.usefixtures("serializer")
def test_int(serializer):
    int_ = 10
    assert '{"d": 10, "s": []}' == serializer.encode(int_)
    assert serializer.decode('{"d": 10, "s": []}') == int_

    neg_int_ = -10
    assert '{"d": -10, "s": []}' == serializer.encode(neg_int_)
    assert serializer.decode('{"d": -10, "s": []}') == neg_int_

    zero_int_ = 0
    assert '{"d": 0, "s": []}' == serializer.encode(zero_int_)
    assert serializer.decode('{"d": 0, "s": []}') == zero_int_


@pytest.mark.usefixtures("serializer")
def test_float(serializer):
    float_ = 10.0
    assert '{"d": 10.0, "s": []}' == serializer.encode(float_)
    assert serializer.decode('{"d": 10.0, "s": []}') == float_

    neg_float_ = -10.0
    assert '{"d": -10.0, "s": []}' == serializer.encode(neg_float_)
    assert serializer.decode('{"d": -10.0, "s": []}') == neg_float_

    zero_float_ = 0.0
    assert '{"d": 0.0, "s": []}' == serializer.encode(zero_float_)
    assert serializer.decode('{"d": 0.0, "s": []}') == zero_float_


@pytest.mark.usefixtures("serializer")
def test_bool(serializer):
    true = True
    assert '{"d": true, "s": []}' == serializer.encode(true)
    assert serializer.decode('{"d": true, "s": []}') == true

    false = False
    assert '{"d": false, "s": []}' == serializer.encode(false)
    assert serializer.decode('{"d": false, "s": []}') == false


@pytest.mark.usefixtures("serializer")
def test_none(serializer):
    none = None
    assert '{"d": null, "s": []}' == serializer.encode(none)
    assert serializer.decode('{"d": null, "s": []}') == none


datetime_ = datetime.datetime(2018, 10, 16, 16, 53, 29, 164069)


@pytest.mark.usefixtures("serializer")
def test_datetime(serializer):
    assert '{"o": "@zenaton#0",' \
           ' "s": [{"n": "datetime",' \
           ' "p": {"day": 16, "hour": 16, "microsecond": 164069, "minute": 53, "month": 10, "second": 29, "tzinfo": null, "year": 2018}}]}' == serializer.encode(
        datetime_)


@pytest.mark.usefixtures("serializer")
def test_date(serializer):
    date_ = datetime_.date()
    assert '{"o": "@zenaton#0", "s": [{"n": "date", "p": {"day": 16, "month": 10, "year": 2018}}]}' == serializer.encode(
        date_)


@pytest.mark.usefixtures("serializer")
def test_time(serializer):
    time_ = datetime_.time()
    assert '{"o": "@zenaton#0",' \
           ' "s": [{"n": "time", "p": {"hour": 16, "microsecond": 164069, "minute": 53, "second": 29, "tzinfo": null}}]}' == serializer.encode(
        time_)


@pytest.mark.usefixtures("serializer")
def test_dict(serializer):
    dict_ = {'foo': 'bar'}
    assert '{"o": "@zenaton#0", "s": [{"a": {"foo": "bar"}}]}' == serializer.encode(dict_)
    assert serializer.decode('{"o": "@zenaton#0", "s": [{"a": {"foo": "bar"}}]}') == dict_

    empty_dict_ = dict()
    assert '{"o": "@zenaton#0", "s": [{"a": {}}]}' == serializer.encode(empty_dict_)
    assert serializer.decode('{"o": "@zenaton#0", "s": [{"a": {}}]}') == empty_dict_


@pytest.mark.usefixtures("serializer")
def test_list(serializer):
    list_ = ['foo', 'bar', 1, 10]
    assert '{"o": "@zenaton#0", "s": [{"a": ["foo", "bar", 1, 10]}]}' == serializer.encode(list_)
    assert serializer.decode('{"o": "@zenaton#0", "s": [{"a": ["foo", "bar", 1, 10]}]}') == list_

    empty_list_ = []
    assert '{"o": "@zenaton#0", "s": [{"a": []}]}' == serializer.encode(empty_list_)
    assert serializer.decode('{"o": "@zenaton#0", "s": [{"a": []}]}') == empty_list_


dict0 = {}
dict1 = {'dict0': dict0}
dict0['dict1'] = dict1


@pytest.mark.usefixtures("serializer")
def test_circular_dict(serializer):
    assert '{"o": "@zenaton#0",' \
           ' "s": [{"a": {"dict1": "@zenaton#1"}}, {"a": {"dict0": "@zenaton#0"}}]}' == serializer.encode(dict0)
    decoded = serializer.decode('{"o": "@zenaton#0",'
                                ' "s": [{"a": {"dict1": "@zenaton#1"}}, {"a": {"dict0": "@zenaton#0"}}]}')
    assert id(decoded) == id(decoded['dict1']['dict0'])
    assert id(decoded['dict1']) == id(decoded['dict1']['dict0']['dict1'])

    assert '{"o": "@zenaton#0",' \
           ' "s": [{"a": {"dict0": "@zenaton#1"}}, {"a": {"dict1": "@zenaton#0"}}]}' == serializer.encode(dict1)
    decoded = serializer.decode('{"o": "@zenaton#0",'
                                ' "s": [{"a": {"dict0": "@zenaton#1"}}, {"a": {"dict1": "@zenaton#0"}}]}')
    assert id(decoded) == id(decoded['dict0']['dict1'])
    assert id(decoded['dict0']) == id(decoded['dict0']['dict1']['dict0'])


list0 = ['foo']
list1 = ['bar']
list0.append(list1)
list1.append(list0)


@pytest.mark.usefixtures("serializer")
def test_circular_list(serializer):
    assert '{"o": "@zenaton#0",' \
           ' "s": [{"a": ["foo", "@zenaton#1"]}, {"a": ["bar", "@zenaton#0"]}]}' == serializer.encode(list0)
    decoded = serializer.decode('{"o": "@zenaton#0",'
                                ' "s": [{"a": ["foo", "@zenaton#1"]}, {"a": ["bar", "@zenaton#0"]}]}')
    assert id(decoded) == id(decoded[1][1])
    assert id(decoded[1]) == id(decoded[1][1][1])

    assert '{"o": "@zenaton#0",' \
           ' "s": [{"a": ["bar", "@zenaton#1"]}, {"a": ["foo", "@zenaton#0"]}]}' == serializer.encode(list1)
    decoded = serializer.decode('{"o": "@zenaton#0",'
                                ' "s": [{"a": ["bar", "@zenaton#1"]}, {"a": ["foo", "@zenaton#0"]}]}')
    assert id(decoded) == id(decoded[1][1])
    assert id(decoded[1]) == id(decoded[1][1][1])


class Container:
    pass


container = Container()
container.dict0 = dict0
container.dict1 = dict1


@pytest.mark.usefixtures("serializer")
def test_container(serializer):
    assert ('{"o": "@zenaton#0",' \
            ' "s": [{"n": "Container",' \
            ' "p": {"dict0": "@zenaton#2", "dict1": "@zenaton#1"}},' \
           ' {"a": {"dict0": "@zenaton#2"}},' \
            ' {"a": {"dict1": "@zenaton#1"}}]}' == serializer.encode(container) or
            '{"o": "@zenaton#0",' \
            ' "s": [{"n": "Container",' \
            ' "p": {"dict0": "@zenaton#1", "dict1": "@zenaton#2"}},' \
            ' {"a": {"dict1": "@zenaton#2"}},' \
            ' {"a": {"dict0": "@zenaton#1"}}]}' == serializer.encode(container))


container0 = Container()
container1 = Container()
container0.teammate = container1
container1.teammate = container0


@pytest.mark.usefixtures("serializer")
def test_circular_container(serializer):
    assert '{"o": "@zenaton#0",' \
           ' "s": [{"n": "Container",' \
           ' "p": {"teammate": "@zenaton#1"}},' \
           ' {"n": "Container",' \
           ' "p": {"teammate": "@zenaton#0"}}]}' == serializer.encode(container0)
