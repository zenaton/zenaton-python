import json

class Properties:
    SPECIAL_CASES = [
        Exception,
    ]

    def blank_instance(self, class_):

        class Empty:
            pass

        output = Empty()
        output.__class__ = class_
        return output

    def from_(self, object_):
        if hasattr(object_, 'buffer'):
            return object_.buffer
        return vars(object_)

    def set(self, object_, properties):
        if properties != (None,) and properties is not None:
            for key, value in properties.items():
                setattr(object_, key, value)

    def object_from(self, class_, properties, super_class=None):
        object_ = self.blank_instance(class_)
        self.check_class(object_, super_class)
        self.set(object_, properties)
        return object_

    def check_class(self, object_, super_class):
        error_message = 'Error - #{object.class} should be an instance of #{super_class}'
        if not issubclass(type(object_), super_class):
            raise Exception(error_message)

    def valid_object(self, object_, super_class):
        return not super_class or issubclass(object_, super_class)

    def from_complex_type(self, object_):
        pass

    def set_complex_type(self, object_, props):
        props['json_class'] = type(object).__name__
        return json.dumps(props)

    def is_special_case(self, object_):
        pass
