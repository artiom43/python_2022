import time
import traceback
import typing as tp


class TimeoutException(Exception):
    pass


class SoftTimeoutException(TimeoutException):
    pass


class HardTimeoutException(TimeoutException):
    pass


class TimeCatcher:
    def __init__(self, soft_timeout: tp.Optional[float] = None, hard_timeout: tp.Optional[float] = None) -> None:
        self.soft_timeout = soft_timeout
        self.hard_timeout = hard_timeout
        self.start_time = time.time()
        if soft_timeout is not None and soft_timeout <= 0:
            raise AssertionError
        elif soft_timeout is not None and hard_timeout is not None and hard_timeout < soft_timeout:
            raise AssertionError
        elif hard_timeout is not None and hard_timeout <= 0:
            raise AssertionError

    def __enter__(self) -> tp.Any:
        # self.start_time = time.time()
        return self

    def __exit__(self, exit_type: type, exc_value: BaseException,
                 self_traceback: traceback.TracebackException) -> tp.Optional[bool]:
        # print(time.time() - self.start_time)
        self.time = time.time() - self.start_time
        if self.hard_timeout is not None and self.time > self.hard_timeout:
            raise HardTimeoutException
            pass
        elif self.soft_timeout is not None and self.time > self.soft_timeout:
            raise SoftTimeoutException
            pass
        if exc_value is not None:
            return True

    def __float__(self) -> float:
        return time.time() - self.start_time

    def __str__(self) -> str:
        return str("Time consumed: " + str(time.time() - self.start_time))
