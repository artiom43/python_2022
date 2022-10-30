import traceback
from contextlib import contextmanager
from typing import Iterator, TextIO, Type
import sys


@contextmanager
def supresser(*types_: Type[BaseException]) -> Iterator[None]:
    try:
        yield None
    except types_:
        pass


@contextmanager
def retyper(type_from: Type[BaseException], type_to: Type[BaseException]) -> Iterator[None]:
    try:
        yield None
    except type_from as e:
        raise type_to(*e.args)


@contextmanager
def dumper(stream: TextIO | None = None) -> Iterator[None]:
    try:
        yield None
    finally:
        if stream is not None and sys.exc_info()[1] is not None:
            stream.write(traceback.format_exception_only(sys.exc_info()[0], value=sys.exc_info()[1])[0])
        elif sys.exc_info()[1] is not None:
            sys.stderr.write(traceback.format_exception_only(sys.exc_info()[0], value=sys.exc_info()[1])[0])
        pass
