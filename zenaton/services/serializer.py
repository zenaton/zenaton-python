import json

from zenaton.services.properties import Properties
from zenaton.exceptions import InvalidArgumentError

class Serializer:
    # this string prefixs ids that are used to identify objects
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

    def encode(self, data):
        return '{\"o\":\"@zenaton#0\",\"s\":[{\"a\":' + json.dumps(data, sort_keys=True) + '}]}'

    def decode(self, json_string):
        return json.loads(json_string)['s'][0]['a']

    def __is_basic_type(self, data):
        return isinstance(data, str) or isinstance(data, int) or isinstance(data, bool) or None

    def __encode_value(self, value):
        if self.__is_basic_type(value):
            return value
        else:
            return self.__encode_to_store(value)

    def __encode_to_store(self, object_):
        # TO DO Ask Igor about the Ruby code
        pass

    def __store_and_encode(self, object_):
        pass

    def __store_id(self, id):
        return '{}{}'.format(self.ID_PREFIX, id)

    def __encode_object_by_type(self, object_):
        pass

    def __encode_object(self, object_):
        return {
            self.KEY_OBJECT_NAME: type(object_).__name__,
            self.KEY_OBJECT_PROPERTIES: self.__encode_legacy_dict(self.properties.from_(object_))
        }

    def __encode_list(self, list_):
        return {
            self.KEY_ARRAY: [self.encode_value(element) for element in list_]
        }

    def __encode_dict(self, dict_):
        return {
            self.KEY_ARRAY: {self.encode_value(element) for element in dict_}
        }

    def __encode_legacy_dict(self, dict_):
        return {element.encode_value() for element in dict_}

    def __is_store_id(self, string_):
        return isinstance(string_, str) and \
               string_.startswith(self.ID_PREFIX) and \
               int(string_[len(self.ID_PREFIX):-1]) <= len(self.encoded)

    def __decode_element(self, value):
        if self.__is_store_id(value):
            id_ = int(value[len(self.ID_PREFIX):-1])
            encoded = self.encoded[id_]
            return self.__decode_from_store(id_, encoded)
        elif isinstance(value, list):
            return self.__decode_legacy_list(value)
        elif isinstance(value, dict):
            return self.__decode_legacy_dict(value)
        else:
            return value

    def __decode_enumerable(self, enumerable):
        if isinstance(enumerable, list):
            return self.__decode_legacy_list(enumerable)
        if isinstance(enumerable, dict):
            return self.__decode_legacy_dict(enumerable)
        raise InvalidArgumentError('Unknown type')

    def __decode_legacy_list(self, list_):
        return [self.__decode_element(element) for element in list_]

    def __decode_legacy_dict(self, dict_):
        return {self.__decode_element(element) for element in dict_}

    def __decode_list(self, id_, list_):
        # TO DO: Ask Igor about the Ruby Code
        decoded_list = [self.__decode_element(element) for element in list_]
        self.decoded[id_] = decoded_list
        return decoded_list

    def __decode_dict(self, id_, dict_):
        decoded_dict = {self.__decode_element(element) for element in dict_}
        return decoded_dict

    def __decode_from_store(self, id_, encoded):
        decoded = self.decoded[id_]
        if decoded:
            return decoded
        encoded_value = encoded[self.KEY_ARRAY]
        if isinstance(encoded_value, list):
            return self.__decode_list(id_, encoded_value)
        if isinstance(encoded_value, dict):
            return self.__decode_dict(id_, encoded_value)
        return self.__decoded_object(id_, encoded)

    def __decoded_object_by_type(self, id_, encoded):
        enumerable = encoded[self.KEY_ARRAY]
        if isinstance(enumerable, list):
            return self.__decode_list(id_, enumerable)
        if isinstance(enumerable, dict):
            return self.__decode_dict(id_, enumerable)
        else:
            self.__decoded_object(id_, encoded)

    def __decoded_object(self, id_, encoded_object):
        object_ = self.properties.blank_instance(encoded_object[self.KEY_OBJECT_NAME])
        self.decoded[id_] = object_
        properties = self.__decode_legacy_dict(encoded_object[self.KEY_OBJECT_PROPERTIES])
        self.properties.set(object_, properties)

    def __transform_values(self, dict_):
        pass
