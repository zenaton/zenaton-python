import copy
import json
import inspect
import importlib.util

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

    def __init__(self, boot=None, name=None):
        self.properties = Properties()
        self.encoded = []
        self.decoded = []
        self.boot = boot
        self.name = name

    def encode(self, data):
        self.encoded = []
        self.decoded = []
        value = dict()
        if self.__is_basic_type(data):
            value[self.KEY_DATA] = data
        else:
            value[self.KEY_OBJECT] = self.__encode_to_store(data)
        value[self.KEY_STORE] = self.encoded
        return json.dumps(value, sort_keys=True)

    def decode(self, json_string):
        parsed_json = json.loads(json_string)
        encoded_json = copy.deepcopy(parsed_json)
        self.encoded = encoded_json[self.KEY_STORE]
        del encoded_json[self.KEY_STORE]
        self.decoded = []
        if self.KEY_DATA in parsed_json:
            return parsed_json[self.KEY_DATA]
        if self.KEY_ARRAY in parsed_json:
            return self.__decode_enumerable(parsed_json[self.KEY_ARRAY])
        if self.KEY_OBJECT in parsed_json:
            id_ = int(parsed_json[self.KEY_OBJECT][len(self.ID_PREFIX):])
            return self.__decode_from_store(id_, self.encoded[id_])

    def __encode_value(self, value):
        if self.__is_basic_type(value):
            return value
        else:
            return self.__encode_to_store(value)

    def __encode_to_store(self, object_):

        for index, element in enumerate(self.decoded):
            if id(element) == id(object_):
                return self.__store_id(index)

        id_ = len(self.decoded)
        self.insert_at_index(self.decoded, id_, object_)
        self.insert_at_index(self.encoded, id_, self.__encode_object_by_type(object_))
        return self.__store_id(id_)

    def insert_at_index(self, list_, index, value):
        try:
            list_[index] = value
        except IndexError:
            for i in range(0, index - len(list_) + 1):
                list_.append(None)
            list_[index] = value

    def append_at_index(self, list_, index, value):
        if len(list_[index]) >= len(value):
            return
        try:
            list_[index].extend(value)
        except (TypeError, IndexError, AttributeError):
            for i in range(0, index - len(list_) + 1):
                list_.append(None)
            list_[index] = value

    def update_at_index(self, list_, index, value):
        if len(list_[index]) >= len(value):
            return
        try:
            list_[index].update(value)
        except (TypeError, IndexError, AttributeError):
            for i in range(0, index - len(list_) + 1):
                list_.append(None)
            list_[index] = value

    def __encode_object_by_type(self, object_):
        if isinstance(object_, list):
            return self.__encode_list(object_)
        if isinstance(object_, dict):
            return self.__encode_dict(object_)
        return self.__encode_object(object_)

    def __encode_object(self, object_):
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
        return {key: self.__encode_value(value) for key, value in dict_.items()}

    def __decode_element(self, value):
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
        if isinstance(enumerable, list):
            return self.__decode_legacy_list(enumerable)
        if isinstance(enumerable, dict):
            return self.__decode_legacy_dict(enumerable)
        raise InvalidArgumentError('Unknown type')

    def __decode_legacy_list(self, list_):
        return [self.__decode_element(element) for element in list_]

    def __decode_legacy_dict(self, dict_):
        ret = {key: self.__decode_element(value) for key, value in dict_.items()}
        return ret

    def __decode_list(self, id_, list_):
        self.insert_at_index(self.decoded, id_, [])
        decoded_list = [self.__decode_element(element) for element in list_]
        self.append_at_index(self.decoded, id_, decoded_list)
        return self.decoded[id_]

    def __decode_dict(self, id_, dict_):
        self.insert_at_index(self.decoded, id_, dict())
        decoded_dict = {key: self.__decode_element(value) for key, value in dict_.items()}
        self.update_at_index(self.decoded, id_, decoded_dict)
        return self.decoded[id_]

    def __decode_from_store(self, id_, encoded):
        if len(self.decoded) >= id_ + 1 and self.decoded[id_] is not None:
            decoded = self.decoded[id_]
            return decoded
        else:
            encoded_value = encoded.get(self.KEY_ARRAY, None)
            if isinstance(encoded_value, list):
                return self.__decode_list(id_, encoded_value)
            if isinstance(encoded_value, dict):
                return self.__decode_dict(id_, encoded_value)
            return self.__decoded_object(id_, encoded)

    def __decoded_object(self, id_, encoded_object):
        if len(self.decoded) >= id_ + 1 and self.decoded[id_] is not None:
            return self.decoded[id_]
        try:
            object_class = self.import_class(self.name, encoded_object[self.KEY_OBJECT_NAME])
            object_ = self.properties.blank_instance(object_class)
            self.insert_at_index(self.decoded, id_, object_)
            properties = self.__decode_legacy_dict(encoded_object.get(self.KEY_OBJECT_PROPERTIES, None))
            self.properties.set(object_, properties)
            return object_
        except TypeError:
            properties = self.__decode_legacy_dict(encoded_object.get(self.KEY_OBJECT_PROPERTIES, None))
            object_ = object_class(**properties)
            self.insert_at_index(self.decoded, id_, object_)
            return object_
        except KeyError:
            return None

    def __is_store_id(self, string_):
        try:
            suffix = int(string_[len(self.ID_PREFIX):])
        except (TypeError, ValueError):
            return False
        return isinstance(string_, str) and \
               string_.startswith(self.ID_PREFIX) and \
               suffix <= len(self.encoded)

    def __store_id(self, id):
        return '{}{}'.format(self.ID_PREFIX, id)

    def __is_basic_type(self, data):
        return (isinstance(data, str) or
                isinstance(data, int) or
                isinstance(data, float) or
                isinstance(data, bool) or data is None)

    def import_class(self, workflow_name, class_name):
        spec = importlib.util.spec_from_file_location('boot', self.boot)
        boot = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(boot)
        workflow_class = getattr(boot, workflow_name)
        workflow_path = inspect.getfile(workflow_class)
        workflow_spec = importlib.util.spec_from_file_location('workflow', workflow_path)
        workflow_module = importlib.util.module_from_spec(workflow_spec)
        workflow_spec.loader.exec_module(workflow_module)
        return getattr(workflow_module, class_name)
