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

        print('class_: {}'.format(class_))
        print('type: {}'.format(type(class_)))

        if isinstance(class_, type(None)) or class_ == 'NoneType':
            return None

        class Empty:
            pass

        print('class_: {}'.format(class_))

        output = Empty()
        output.__class__ = class_
        return output

    def from_(self, object_):
        print('from_')
        if not object_:
            print('from_ None')
            # return {'key': 'value'}
            return None
        if self.is_special_case(object_):
            print('from_ special case')
            return self.from_complex_type(object_)
        else:
            if hasattr(object_, 'buffer'):
                return object_.buffer
            if hasattr(object_, 'args'):
                print('from_ args: {}'.format(object_))
                return object_.args
            print('from_ object: {}'.format(object_))
            # print('from_ object vars: {}'.format(vars(object_)))
            return vars(object_)
            #     print(object_.__dict__)
            #     return object_.__dict__
            # except AttributeError:
            #     return None

    def set(self, object_, properties):
        print("SET")
        # if self.is_special_case(object_):
        #    print("SET is_special_case")
        #    return self.set_complex_type(object_)
        # else:
        if properties != (None,) and properties is not None:
            print('properties: {}'.format(properties))
            for key, value in properties.items():
                setattr(object_, key, value)
        print(object_.__dict__)
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
        return json.dumps(object_)

    def set_complex_type(self, object_):
        print("SET COMPLEX TYPE")
        # props['json_class'] = type(object).__name__
        return json.loads(props)

    def is_special_case(self, object_):
        return type(object_) in self.SPECIAL_CASES or isinstance(object_, BaseException)
