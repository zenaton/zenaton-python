import json
import datetime

from zenaton.services.properties import Properties
from zenaton.services.serializer import Serializer

properties = Properties()
serializer = Serializer()


class MyClass:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def my_method(self):
        return self.a + self.b


class ParentClass:

    def __init__(self, child_object):
        self.child_object = child_object


class CustomEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return {'__datetime__': o.replace(microsecond=0).isoformat()}
        return {'__{}__'.format(o.__class__.__name__): o.__dict__}


class MyClass:
    dictionary = {'a': 1, 'b': 2}


child_object = MyClass(1, 2)
child_dict = json.dumps(child_object, cls=CustomEncoder)
new_child_dict = json.loads(child_dict)
new_child_object = properties.object_from(MyClass, new_child_dict['__MyClass__'], MyClass)

parent_object = ParentClass(child_object)
parent_dict = json.dumps(parent_object, cls=CustomEncoder)
new_parent_dict = json.loads(parent_dict)
new_parent_object = properties.object_from(ParentClass, new_parent_dict['__ParentClass__'], ParentClass)
_ = new_parent_object.__dict__
child_in_parent = new_parent_object.child_object

pass
