import json
import copy

from zenaton.services.properties import Properties
from zenaton.exceptions import InvalidArgumentError


class Serializer:
    # this string prefixes ids that are used to identify objects
    ID_PREFIX = '@zenaton#'

    KEY_OBJECT = 'o'  # JSON key for objects
    KEY_OBJECT_NAME = 'n'  # JSON key for class name
    KEY_OBJECT_PROPERTIES = 'p'  # JSON key for object ivars
    KEY_ARRAY = 'a'  # JSON key for array and hashes
    KEY_DATA = 'd'  # JSON key for json compatibles types
    KEY_STORE = 's'  # JSON key for deserialized complex object

    def __init__(self):
        self.properties = Properties()
        self.encoded = []
        self.decoded = []

    # def encode(self, data):
        # return '{\"o\":\"@zenaton#0\",\"s\":[{\"a\":' + json.dumps(data, sort_keys=True) + '}]}'

    def encode(self, data):

        print('encode')
        print(data)
        self.encoded = []
        self.decoded = []
        value = {}
        # TO DO ? : Test if data is a Proc
        if self.__is_basic_type(data):
            print('encode basic type: {}'.format(data))
            value[self.KEY_DATA] = data
        else:
            print('encode other type: {}'.format(data))
            value[self.KEY_OBJECT] = self.__encode_to_store(data)
        value[self.KEY_STORE] = self.encoded
        print('encode return value: {}'.format(value))
        return json.dumps(value, sort_keys=True)

    # def decode(self, json_string):
        # return json.loads(json_string)['s'][0]['a']

    def decode(self, json_string):

        print('Serializer.decode {}'.format(json_string))
        parsed_json = json.loads(json_string)
        self.decoded = []
        encoded_json = copy.deepcopy(parsed_json)
        self.encoded = encoded_json[self.KEY_STORE]
        del encoded_json[self.KEY_STORE]
        print('parsed_json {}'.format(parsed_json))
        print('encoded {}'.format(self.encoded))
        # first_key = list(parsed_json.keys())[0]
        # print('first_key: {}'.format(first_key))
        # if first_key == self.KEY_DATA:
        print(parsed_json.get(self.KEY_DATA, None))
        # print(parsed_json['d'])
        if self.KEY_DATA in parsed_json:
            print('CASE KEY_DATA')
            return parsed_json[self.KEY_DATA]
        # if first_key == self.KEY_ARRAY:
        if self.KEY_ARRAY in parsed_json:
            print('CASE KEY_ARRAY')
            return self.__decode_enumerable(parsed_json[self.KEY_ARRAY])
        # if first_key == self.KEY_OBJECT:
        if self.KEY_OBJECT in parsed_json:
            print('CASE KEY_OBJECT')
            print('parsed_json {}'.format(parsed_json))
            id_ = int(parsed_json[self.KEY_OBJECT][len(self.ID_PREFIX):])
            print('id_: {}'.format(id_))
            print('self.encoded: {}'.format(self.encoded))
            return self.__decode_from_store(id_, self.encoded[id_])
        print("FAIL")

    def __is_basic_type(self, data):
        return isinstance(data, str) or isinstance(data, int) or isinstance(data, bool) or data is None

    def __encode_value(self, value):
        if self.__is_basic_type(value):
            return value
        else:
            return self.__encode_to_store(value)

    def __encode_to_store(self, object_):

        element = [element for element in self.decoded if id(element) == id(object_)]
        if len(element) >= 1:
            id_ = element[0]
            return self.__store_id(id_)
        else:
            return self.__store_and_encode(object_)

    def __store_and_encode(self, object_):
        print('__store_and_encode')
        id_ = len(self.encoded)
        print('__store_and_encode id: {}'.format(id_))
        print('__store_and_encode object_: {}'.format(object_))
        self.decoded.insert(id_, object_)
        self.encoded.insert(id_, self.__encode_object_by_type(object_))
        return self.__store_id(id_)

    def __store_id(self, id):
        return '{}{}'.format(self.ID_PREFIX, id)

    def __encode_object_by_type(self, object_):
        print('__encode_object_by_type')
        print('object_ {}'.format(object_))
        if isinstance(object_, list):
            print('__encode_object_by_type list')
            return self.__encode_list(object_)
        if isinstance(object_, dict):
            print('__encode_object_by_type dict')
            return self.__encode_dict(object_)
        print('__encode_object_by_type object')
        return self.__encode_object(object_)

    def __encode_object(self, object_):
        print("__encode_object")
        return {
            self.KEY_OBJECT_NAME: type(object_).__name__,
            self.KEY_OBJECT_PROPERTIES: self.__encode_legacy_dict(self.properties.from_(object_))
        }

    def __encode_list(self, list_):
        return {
            self.KEY_ARRAY: [self.__encode_value(element) for element in list_]
        }

    def __encode_dict(self, dict_):
        return {
            self.KEY_ARRAY: {key: self.__encode_value(value) for key, value in dict_.items()}
        }

    def __encode_legacy_dict(self, dict_):
        print('__encode_legacy_dict: {}'.format(dict_))
        return {key: self.__encode_value(value) for key, value in dict_.items()}

    def __is_store_id(self, string_):
        return isinstance(string_, str) and \
               string_.startswith(self.ID_PREFIX) and \
               int(string_[len(self.ID_PREFIX):]) <= len(self.encoded)

    def __decode_element(self, value):
        print('__decode_element')
        if self.__is_store_id(value):
            id_ = int(value[len(self.ID_PREFIX):])
            encoded = self.encoded[id_]
            return self.__decode_from_store(id_, encoded)
        elif isinstance(value, list):
            return self.__decode_legacy_list(value)
        elif isinstance(value, dict):
            return self.__decode_legacy_dict(value)
        else:
            return value

    def __decode_enumerable(self, enumerable):
        print('__decode_enumerable')
        if isinstance(enumerable, list):
            return self.__decode_legacy_list(enumerable)
        if isinstance(enumerable, dict):
            return self.__decode_legacy_dict(enumerable)
        raise InvalidArgumentError('Unknown type')

    def __decode_legacy_list(self, list_):
        print('__decode_legacy_list')
        return [self.__decode_element(element) for element in list_]

    def __decode_legacy_dict(self, dict_):
        print('__decode_legacy_dict')
        ret = {key: self.__decode_element(value) for key, value in dict_.items()}
        print('__decode_legacy_dict return: {}'.format(ret))
        return ret

    def __decode_list(self, id_, list_):
        print('__decode_list')
        # TO DO: Ask Igor about the Ruby Code
        # ??
        decoded_list = [self.__decode_element(element) for element in list_]
        self.decoded[id_].extend(decoded_list)
        return decoded_list

    def __decode_dict(self, id_, dict_):
        print('__decode_dict')
        decoded_dict = {key: self.__decode_element(value) for key, value in dict_.items()}
        return decoded_dict

    def __decode_from_store(self, id_, encoded):
        print('\n')
        print('__decode_from_store')
        print('self.decoded: {}'.format(self.decoded))

        if len(self.decoded) >= id_ + 1:
            decoded = self.decoded[id_]
            return decoded
        else:
            # encoded_value = encoded[self.KEY_ARRAY]
            encoded_value = encoded.get(self.KEY_ARRAY, None)
            if isinstance(encoded_value, list):
                print('__decode_from_store list')
                return self.__decode_list(id_, encoded_value)
            if isinstance(encoded_value, dict):
                print('__decode_from_store dict')
                return self.__decode_dict(id_, encoded_value)
            print('__decode_from_store object')
            return self.__decoded_object(id_, encoded)

    def __decoded_object_by_type(self, id_, encoded):
        print('__decoded_object_by_type')
        enumerable = encoded[self.KEY_ARRAY]
        if isinstance(enumerable, list):
            return self.__decode_list(id_, enumerable)
        if isinstance(enumerable, dict):
            return self.__decode_dict(id_, enumerable)
        else:
            self.__decoded_object(id_, encoded)

    def __decoded_object(self, id_, encoded_object):
        print('__decoded_object')
        print(id_)
        print(self.decoded)
        try:
            object_ = self.properties.blank_instance(encoded_object[self.KEY_OBJECT_NAME])
        except KeyError:
            object_ = None

        try:
            self.decoded[id_] = object_
        except IndexError:
            self.decoded.insert(id_, object_)
        print('__decoded_object encoded_object: {}'.format(encoded_object))
        # properties = self.__decode_legacy_dict(encoded_object[self.KEY_OBJECT_PROPERTIES])
        properties = self.__decode_legacy_dict(encoded_object.get(self.KEY_OBJECT_PROPERTIES, None))
        self.properties.set(object_, properties)

