''' Module with class and metaclass implementation '''


class CustomMeta(type):
    ''' Custom MetaClass, that renames all attrs '''
    @classmethod
    def __correct(cls, classdict):
        new_dict = {}
        for key, val in classdict.items():
            if '__' != key[:2] and '__' != key[-2:]:
                new_dict['custom_'+key] = val
            else:
                new_dict[key] = val
        return new_dict

    def __new__(cls, name, bases, classdict):
        new_dict = CustomMeta.__correct(classdict)
        return super().__new__(cls, name, bases, new_dict)

    def __custom_set(cls, name, value):
        if '__' != name[:2] and '__' != name[-2:]:
            name = 'custom_' + name
        cls.__dict__[name] = value

    def __prepare__(cls, *args):
        return {'__setattr__': CustomMeta.__custom_set}


class CustomClass(metaclass=CustomMeta):
    ''' All attrs will be renamed '''
    x = 50

    def __init__(self, val=99):
        self.val = val

    def __str__(self):
        return "Custom_by_metaclass"

    def line(self):
        ''' Just some line func  '''
        return 100
