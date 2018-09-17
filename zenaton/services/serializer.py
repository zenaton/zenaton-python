import json


class Serializer:

    def __init__(self):
        pass

    def encode(self, data):
        return '{\"o\":\"@zenaton#0\",\"s\":[{\"a\":' + json.dumps(data, sort_keys=True) + '}]}'

    def decode(self, json_string):
        return json.loads(json_string)['s'][0]['a']

    def __is_basic_type(self, data):
        pass

    def __encode_value(self, value):
        pass

    def __encode_to_store(self, object_):
        pass

    def __store_and_encode(self, object_):
        pass

    def __store_id(self, id):
        pass

    def __encode_object_by_type(self, object_):
        pass

    def __encode_object(self, object_):
        pass

    def __encode_list(self, list_):
        pass

    def __encode_dict(self, dict_):
        pass

    def __encode_legacy_dict(self, dict_):
        pass

    def __is_store_if(self, string_):
        pass

    def __decode_element(self, value):
        pass

    def __decode_enumerable(self, enumerable):
        pass

    def __decode_legacy_list(self, list_):
        pass

    def __decode_legacy_dict(self, dict_):
        pass

    def __decode_list(self, list_):
        pass

    def __decode_dict(self, dict_):
        pass

    def __decode_from_store(self, id, encoded):
        pass

    def __decoded_object_by_type(self, id, encoded):
        pass

    def __decoded_object(self, id, encoded_object):
        pass

    def __transsform_values(self, dict_):
        pass
