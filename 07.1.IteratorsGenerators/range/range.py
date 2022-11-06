from typing import Iterable, Sized, Iterator
# import typing as tp


class RangeIterator(Iterator[int]):
    def __init__(self, start: int, stop: int, step: int) -> None:
        self.start = start
        self.stop = stop
        self.step = step
        self.current = start

    def __next__(self) -> int:
        if self.step > 0:
            if self.current >= self.stop:
                raise StopIteration
            else:
                self.current += self.step
                return self.current - self.step
        else:
            if self.current <= self.stop:
                raise StopIteration
            else:
                self.current += self.step
                return self.current - self.step


class Range(Sized, Iterable[int]):
    """The range-like type, which represents an immutable sequence of numbers"""

    def __init__(self, *args: int) -> None:
        """
        :param args: either it's a single `stop` argument
            or sequence of `start, stop[, step]` arguments.
        If the `step` argument is omitted, it defaults to 1.
        If the `start` argument is omitted, it defaults to 0.
        If `step` is zero, ValueError is raised.
        """
        self.start = 0
        self.step = 1
        self.stop = 0
        if len(args) == 1:
            self.stop = args[0]
        elif len(args) == 2:
            self.stop = args[1]
            self.start = args[0]
        elif len(args) == 3:
            self.stop = args[1]
            self.start = args[0]
            self.step = args[2]
            if self.step == 0:
                raise ValueError

    def __iter__(self) -> 'RangeIterator':
        return RangeIterator(self.start, self.stop, self.step)

    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        if self.step == 1:
            answer = "range({}, {})".format(self.start, self.stop)
        else:
            answer = "range({}, {}, {})".format(self.start, self.stop, self.step)
        return answer

    def __contains__(self, key: int) -> bool:
        if (self.start - key) % self.step != 0:
            return False
        if self.step > 0:
            if key < self.start or key >= self.stop:
                return False
            return True
        if key > self.start or key <= self.stop:
            return False
        return True

    def __getitem__(self, key: int) -> int:
        answer = key*self.step + self.start
        if self.step > 0:
            if answer >= self.stop or answer < self.start:
                raise IndexError
        if self.step < 0:
            if answer <= self.stop or answer > self.start:
                raise IndexError
        return answer

    def __len__(self) -> int:
        # print((abs(self.stop - self.start) + abs(self.step) - 1)//abs(self.step))
        if self.step > 0:
            return max((self.stop - self.start + self.step - 1)//self.step, 0)
        else:
            return max((self.start - self.stop - self.step - 1)//(-self.step), 0)
