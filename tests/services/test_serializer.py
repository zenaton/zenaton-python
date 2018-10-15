import pytest
import json


@pytest.mark.usefixtures("serializer")
def test_str(serializer):
    str_ = 'foo bar'
    assert '{"d": "foo bar", "s": []}' == serializer.encode(str_)
    assert serializer.decode('{"d": "foo bar", "s": []}') == str_


@pytest.mark.usefixtures("serializer")
def test_str(serializer):
    int_ = 10
    assert '{"d": 10, "s": []}' == serializer.encode(int_)
    assert serializer.decode('{"d": 10, "s": []}') == int_


@pytest.mark.usefixtures("serializer")
def test_dict(serializer):
    dict_ = {'foo': 'bar'}
    assert '{"o": "@zenaton#0", "s": [{"a": {"foo": "bar"}}]}' == serializer.encode(dict_)
    assert serializer.decode('{"o": "@zenaton#0", "s": [{"a": {"foo": "bar"}}]}') == dict_


@pytest.mark.usefixtures("serializer")
def test_list(serializer):
    list_ = ['foo', 'bar', 1, 10]
    assert '{"o": "@zenaton#0", "s": [{"a": ["foo", "bar", 1, 10]}]}' == serializer.encode(list_)
    assert serializer.decode('{"o": "@zenaton#0", "s": [{"a": ["foo", "bar", 1, 10]}]}') == list_


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
    assert '{"o": "@zenaton#0",' \
           ' "s": [{"n": "Container",' \
           ' "p": {"dict0": "@zenaton#2", "dict1": "@zenaton#1"}},' \
           ' {"a": {"dict0": "@zenaton#2"}},' \
           ' {"a": {"dict1": "@zenaton#1"}}]}') == serializer.encode(container)
