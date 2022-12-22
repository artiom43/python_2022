import typing as tp
# from collections import defaultdict


class MetaClass(type):
    # def __call__(cls, name, bases, members):
    #     # print(args, kwargs)
    #     obj = cls.__new__(cls, name, bases, members)
    #     obj.__init__(cls, name, bases, members)
    #     # bases = cls.__bases__
    #     # print(bases)
    #     # old_class = bases[0]
    #     # print(old_class.__dict__)
    #     # # print(cls.__dict__)
    #     # for name, value in old_class.__dict__.items():
    #     #     if name.startswith('get'):
    #     #         print(name, value, name[4:])
    #     #         if name[4:] not in cls.__dict__:
    #     #
    #     #             obj.__dict__[name[4:]] = ClassGet(name[4:])
    #     # print(obj.__dict__)
    #     return obj

    def __new__(cls: type, name: str, bases: tp.Tuple[type], members: tp.Dict[str, tp.Any]) -> tp.Any:
        # print(*args, **kwargs)
        # print(cls, name, bases, members)
        old_class: type = MetaClass
        # second_class
        for base in bases:
            old_class = base
            break
        # new_items = {}
        getter = {}
        setter = {}
        name_get_or_set = set()
        for name, value in old_class.__dict__.items():
            # print(name, value)
            if name[4:] in members:
                continue
            if name.startswith("get"):
                getter[name[4:]] = value
                name_get_or_set.add(name[4:])
            if name.startswith("set"):
                setter[name[4:]] = value
                name_get_or_set.add(name[4:])
        # members[]
        for name_get in name_get_or_set:
            print(name_get)
            f_get = None
            f_set = None
            if name_get in getter:
                f_get = getter[name_get]
            if name_get in setter:
                f_set = setter[name_get]

            members[name_get] = property(f_get, f_set)
        return type.__new__(cls, name, bases, members)

    # def __init__(cls, *args, **kwargs):
        # print(cls.__bases__)
        # cls.__init__(cls, *args, **kwargs)


class PropertyConverter(metaclass=MetaClass):
    def __getattr__(self, item: str) -> tp.Any:
        # print("sdf")
        # if item in self.__dict__:
        #     return self.__dict__[item]
        # else:
        #     raise AttributeError
        return object.__getattribute__(self, item)

    def __setattr__(self, key: str, value: tp.Any) -> None:
        # pass
        # setattr(self, key, value)
        object.__setattr__(self, key, value)
    # def __int__(self):
    #     self.__dict__['__setattr__'] = object.__setattr__
    #     self.__dict__['__getattr__'] = object.__getattribute__
    # pass
