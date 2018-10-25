import json
import datetime


class Properties:
    SPECIAL_CASES = [
        Exception,
        datetime.datetime,
        datetime.date,
        datetime.time,
    ]

    def blank_instance(self, class_):

        if isinstance(class_, type(None)) or class_ == 'NoneType':
            return None

        class Empty:
            pass

        output = Empty()
        output.__class__ = class_
        return output

    def from_(self, object_):
        if not object_:
            return None
        if self.is_special_case(object_):
            return self.from_complex_type(object_)
        else:
            if hasattr(object_, 'buffer'):
                return object_.buffer
            if hasattr(object_, 'args'):
                return object_.args
            return vars(object_)

    def set(self, object_, properties):
        if properties != (None,) and properties is not None:
            for key, value in properties.items():
                setattr(object_, key, value)
        return object_

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
        if isinstance(object_, datetime.datetime):
            return {'year': object_.year, 'month': object_.month, 'day': object_.day, 'hour': object_.hour,
                    'minute': object_.minute, 'second': object_.second, 'microsecond': object_.microsecond,
                    'tzinfo': object_.tzinfo}
        if isinstance(object_, datetime.date):
            return {'year': object_.year, 'month': object_.month, 'day': object_.day}
        if isinstance(object_, datetime.time):
            return {'hour': object_.hour, 'minute': object_.minute, 'second': object_.second,
                    'microsecond': object_.microsecond, 'tzinfo': object_.tzinfo}
        if issubclass(type(object_), BaseException):
            return {'error_class': object_.__class__.__name__, 'error_args': list(object_.args)}
        return json.dumps(object_)

    def set_complex_type(self, object_):
        return json.loads(object_)

    def is_special_case(self, object_):
        return type(object_) in self.SPECIAL_CASES or isinstance(object_, BaseException)
