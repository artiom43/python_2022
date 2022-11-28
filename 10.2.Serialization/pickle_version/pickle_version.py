import dataclasses


@dataclasses.dataclass
class PickleVersion:
    is_new_format: bool
    version: int


def get_pickle_version(data: bytes) -> PickleVersion:
    """
    Returns used protocol version for serialization.

    :param data: serialized object in pickle format.
    :return: protocol version.
    """
    print(data[1: 2])
    version = data[1: 2]
    if version == b'\x02':
        return PickleVersion(True, 2)
    if version == b'\x03':
        return PickleVersion(True, 3)
    if version == b'\x04':
        return PickleVersion(True, 4)
    if version == b'\x05':
        return PickleVersion(True, 5)
    return PickleVersion(False, -1)
