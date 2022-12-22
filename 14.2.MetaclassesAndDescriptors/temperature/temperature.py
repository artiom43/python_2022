import typing as tp


class Kelvin:
    def __init__(self, name: str):
        self._name = name

    def __get__(self, obj: tp.Optional[tp.Any], objtype: type) -> tp.Any:
        if obj is None:
            return self
        return getattr(obj, self._name)

    def __set__(self, obj: tp.Any, value: int) -> None:
        if value <= 0:
            raise ValueError
        # print(self._name, obj)
        # raise AttributeError
        # if obj is None:
        #     raise AttributeError
        # print(obj.__dict__)
        if self._name in obj.__dict__:
            obj.__dict__[self._name] = value
        else:
            raise AttributeError
        # setattr(obj, self._name, value)

    def __delete__(self, obj: tp.Any) -> None:
        raise ValueError


class Celsius:
    def __init__(self, name: str):
        self._name = name

    def __get__(self, obj: tp.Optional[tp.Any], objtype: type) -> tp.Any:
        if obj is None:
            return self
        # print(obj, objtype)
        # tre: object = 0
        # print(obj.__doc__)
        if "_temperature" not in obj.__dir__():
            raise AttributeError
        # print(obj.__getattribute__(self._name))
        # print(obj.__dict__ , self._name, type(obj), objtype)
        # if type(obj) != Kelvin:
        #     raise AttributeError
        # answer = obj.temperature
        return getattr(obj, self._name) - 273

    def __set__(self, obj: tp.Any, value: int) -> None:
        raise AttributeError

    def __delete__(self, obj: tp.Any) -> None:
        raise ValueError
