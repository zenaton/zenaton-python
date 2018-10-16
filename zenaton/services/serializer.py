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
        print('Serializer.encode: {}'.format(data))
        try:
            print('Serializer.encode vars: {}'.format(vars(data['child'])))
            v = vars(data['child'])
            print(id(v['dict1']['teammate']))
            print(v['dict1']['teammate'])
            print(id(v['dict2']))
            print(v['dict2'])
        except:
            pass
        print(data)
        self.encoded = []
        self.decoded = []
        value = dict()
        # TO DO ? : Test if data is a Proc
        if self.__is_basic_type(data):
            print('encode basic type: {}'.format(data))
            value[self.KEY_DATA] = data
        else:
            print('encode other type: {}'.format(data))
            value[self.KEY_OBJECT] = self.__encode_to_store(data)
        value[self.KEY_STORE] = self.encoded
        print('Serializer.encode return value: {}'.format(value))
        return json.dumps(value, sort_keys=True)

    def decode(self, json_string):
        print('Serializer.decode {}'.format(json_string))
        parsed_json = json.loads(json_string)
        # self.decoded = []
        encoded_json = copy.deepcopy(parsed_json)
        self.encoded = encoded_json[self.KEY_STORE]
        del encoded_json[self.KEY_STORE]
        # self.decoded = [None] * len(self.encoded)
        self.decoded = []
        print('parsed_json {}'.format(parsed_json))
        print('decode self.encoded {}'.format(self.encoded))
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
            ret = self.__decode_from_store(id_, self.encoded[id_])
            print('Serializer.decode return value: {}'.format(ret))
            try:
                print('Serializer.decode return vars: {}'.format(vars(ret['child'])))
                child = ret['child']
                print(child)
                """
                print(id(child.cir0))
                print(child.cir0)
                print(id(child.cir1[3]))
                print(child.cir1[3])
                print(vars(child))
                """
                print(id(child.dict1))
                print(child.dict1)
                print(id(child.dict2['teammate']))
                print(child.dict2['teammate'])
                print(vars(child))
            except:
                pass
            return ret
        print("FAIL")

    def __encode_value(self, value):
        if self.__is_basic_type(value):
            return value
        else:
            return self.__encode_to_store(value)

    def __encode_to_store(self, object_):

        for index, element in enumerate(self.decoded):
            if id(element) == id(object_):
                print('__encode_to_store: len>=1')
                print('__encode_to_store: len>=1 object {}'.format(object_))
                print('__encode_to_store: len>=1 self.decoded {}'.format(self.decoded))
                print('__encode_to_store: len>=1 len(self.decoded) {}'.format(len(self.decoded)))
                print('__encode_to_store: len>=1 element {}'.format(element))
                print('__encode_to_store len >=1 id: {}'.format(index))
                print('__encode_to_store len >=1 object id(): {}'.format(id(object_)))
                return self.__store_id(index)
        """
        print('__encode_to_store self.decoded: {}'.format(self.decoded))
        element = [element for element in self.decoded if id(element) == id(object_)]
        print('__encode_to_store element: {}'.format(element))

        if len(element) >= 1:
            print('__encode_to_store: len>=1')
            print('__encode_to_store: len>=1 object {}'.format(object_))
            print('__encode_to_store: len>=1 self.decoded {}'.format(self.decoded))
            print('__encode_to_store: len>=1 len(self.decoded) {}'.format(len(self.decoded)))
            print('__encode_to_store: len>=1 element {}'.format(element))
            id_ = self.decoded.index(element[0])
            print('__encode_to_store len >=1 id: {}'.format(id_))
            print('__encode_to_store len >=1 id(): {}'.format(id(element[0])))
            print('__encode_to_store len >=1 object id(): {}'.format(id(object_)))
            return self.__store_id(id_)
        else:
        """
        print('__encode_to_store: __store_and_encode')
        print('__store_and_encode: object_ : {}'.format(object_))
        id_ = len(self.decoded)
        print('__store_and_encode before self.encoded: {}'.format(self.encoded))
        print('__store_and_encode id: {}'.format(id_))
        print('__store_and_encode id len(self.encoded): {}'.format(len(self.encoded)))
        print('__store_and_encode object_: {}'.format(object_))
        self.insert_at_index(self.decoded, id_, object_)
        self.insert_at_index(self.encoded, id_, self.__encode_object_by_type(object_))
        print('__store_and_encode after self.encoded: {}'.format(self.encoded))
        print('__store_and_encode after self.decode: {}'.format(self.decoded))
        return self.__store_id(id_)

    def insert_at_index(self, list_, index, value):
        print('insert_at_index: list_: {}, index: {}, value:{}'.format(list_, index, value))

        try:
            list_[index] = value
            print("TRI OK")
        except IndexError:
            print("EXCEPT ADD INDEX")
            for i in range(0, index - len(list_) + 1):
                list_.append(None)
            list_[index] = value
            print('insert_at_index output: list_: {}'.format(list_))

    def append_at_index(self, list_, index, value):
        print('append_at_index: list_: {}, index: {}, value:{}'.format(list_, index, value))
        if len(list_[index]) >= len(value):
            print('PASS')
            return
        try:
            list_[index].extend(value)
            print("TRY OK")
            print('append_at_index output: list_: {}'.format(list_))
        except (TypeError, IndexError, AttributeError):
            print("EXCEPT APPEND INDEX")
            for i in range(0, index - len(list_) + 1):
                list_.append(None)
            list_[index] = value
            print('append_at_index output: list_: {}'.format(list_))

    def update_at_index(self, list_, index, value):
        print('update_at_index: list_: {}, index: {}, value:{}'.format(list_, index, value))
        if len(list_[index]) >= len(value):
            print('PASS')
            return
        try:
            list_[index].update(value)
            print("TRY OK")
            print('update_at_index output: list_: {}'.format(list_))
        except (TypeError, IndexError, AttributeError):
            print("EXCEPT APPEND INDEX")
            for i in range(0, index - len(list_) + 1):
                list_.append(None)
            list_[index] = value
            print('update_at_index output: list_: {}'.format(list_))

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
        print("__encode_object: {}".format(object_))
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

    def __decode_element(self, value):
        print('__decode_element: {}'.format(value))
        element = [element for element in self.decoded if id(element) == id(value)]
        if len(element) > 0:
            print('ELEMENT')
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
        print('__decode_list: {}'.format(list_))
        print('__decode_list id_: {}'.format(id_))
        self.insert_at_index(self.decoded, id_, [])
        decoded_list = [self.__decode_element(element) for element in list_]
        print('__decode_list len: {}'.format(len(self.decoded)))
        self.append_at_index(self.decoded, id_, decoded_list)
        print('__decode_list self.decoded: {}'.format(self.decoded))
        return self.decoded[id_]

    def __decode_dict(self, id_, dict_):
        print('__decode_dict dict_: {}'.format(dict_))
        self.insert_at_index(self.decoded, id_, dict())
        """for key, value in dict_.items():
            self.decoded[id_]"""
        print('newly create dict id: {}'.format(id(self.decoded[id_])))
        decoded_dict = {key: self.__decode_element(value) for key, value in dict_.items()}
        self.update_at_index(self.decoded, id_, decoded_dict)
        print('updated dict id: {}'.format(id(self.decoded[id_])))
        print('__decode_dict dict_: {} return self.decoded[id_] : {}'.format(dict_, self.decoded[id_]))
        print('__decode_dict dict_ return self.decoded: {}'.format(self.decoded))
        # return decoded_dict
        return self.decoded[id_]
        """
        if id_ == 0:
            print(self.decoded[2]['teammate'])
            print(self.decoded[3])
            assert id(self.decoded[2]['teammate']) == id(self.decoded[3])
            assert id(self.decoded[3]['teammate']) == id(self.decoded[2])
        """


    def __decode_from_store(self, id_, encoded):
        print('__decode_from_store id_: {}, encoded: {}'.format(id_, encoded))
        if len(self.decoded) >= id_ + 1 and self.decoded[id_] is not None:
            decoded = self.decoded[id_]
            print('__decode_from_store ALREADY DECODED {}'.format(decoded))
            encoded_value = encoded.get(self.KEY_ARRAY, None)
            print('__decode_from_store encoded_value: {}'.format(encoded_value))
            return decoded
        else:
            encoded_value = encoded.get(self.KEY_ARRAY, None)
            print('__decode_from_store encoded_value: {}'.format(encoded_value))
            if isinstance(encoded_value, list):
                print('__decode_from_store list')
                return self.__decode_list(id_, encoded_value)
            if isinstance(encoded_value, dict):
                print('__decode_from_store dict')
                return self.__decode_dict(id_, encoded_value)
            print('__decode_from_store object')
            return self.__decoded_object(id_, encoded)


    def __decoded_object(self, id_, encoded_object):
        print('__decoded_object')
        print(id_)
        print(self.decoded)

        if len(self.decoded) >= id_ + 1 and self.decoded[id_] is not None:
            print('__decoded_object already in self.decode: {}'.format(encoded_object))
            return self.decoded[id_]
        """try:
            print('__decoded_object already in self.decode: {}'.format(encoded_object))
            
        except IndexError:
            print('__decoded_object INDEX ERROR')
            print(id_)
            print(self.decoded)"""

        try:
            object_class = self.import_class(self.name, encoded_object[self.KEY_OBJECT_NAME])
            object_ = self.properties.blank_instance(object_class)
            print('BLANK INSTANCE: {}'.format(object_))
            print('BLANK INSTANCE TYPE: {}'.format(type(object_)))
        except KeyError:
            object_ = None

        self.insert_at_index(self.decoded, id_, object_)
        print('__decoded_object encoded_object: {}'.format(encoded_object))
        # properties = self.__decode_legacy_dict(encoded_object[self.KEY_OBJECT_PROPERTIES])
        properties = self.__decode_legacy_dict(encoded_object.get(self.KEY_OBJECT_PROPERTIES, None))
        self.properties.set(object_, properties)
        print('__decoded_object final object: {}'.format(object_))
        print('__decoded_object final object vars: {}'.format(vars(object_)))
        return object_

    def __is_store_id(self, string_):
        print('__is_store_id: {}'.format(string_))
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
        return isinstance(data, str) or isinstance(data, int) or isinstance(data, float) or isinstance(data,
                                                                                                       bool) or data is None

    def import_class(self, workflow_name, class_name):
        spec = importlib.util.spec_from_file_location('boot', self.boot)
        boot = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(boot)
        workflow_class = getattr(boot, workflow_name)
        print('workflow_class: {}'.format(workflow_class))
        workflow_path = inspect.getfile(workflow_class)
        workflow_spec = importlib.util.spec_from_file_location('workflow', workflow_path)
        workflow_module = importlib.util.module_from_spec(workflow_spec)
        workflow_spec.loader.exec_module(workflow_module)
        return getattr(workflow_module, class_name)
