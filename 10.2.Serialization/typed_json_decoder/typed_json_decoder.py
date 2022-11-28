import typing as tp
import json

from decimal import Decimal


def as_special_type(dct: tp.Any) -> tp.Any:
    val = dct.get("__custom_key_type__")
    dct1: tp.Any = {}
    # print(dct, " try ")
    if val is not None:
        if val == 'int':
            for key in dct:
                if key != "__custom_key_type__":
                    dct1[int(key)] = dct[key]

        if val == 'float':
            for key in dct:
                if key != "__custom_key_type__":
                    dct1[float(key)] = dct[key]

        if val == 'decimal':
            for key in dct:
                if key != "__custom_key_type__":
                    dct1[Decimal(key)] = dct[key]
        return dct1
    else:
        return dct


def decode_typed_json(json_value: str) -> tp.Any:
    """
    Returns deserialized object from json string.
    Checks __custom_key_type__ in object's keys to choose appropriate type.

    :param json_value: serialized object in json format
    :return: deserialized object
    """

    deserialized_obj = json.loads(json_value, object_hook=as_special_type)
    # print(deserialized_obj)
    # print(json_value)
    return deserialized_obj
