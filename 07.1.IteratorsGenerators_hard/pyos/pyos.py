from queue import Queue
from abc import ABC, abstractmethod
from typing import Generator, Any


class SystemCall(ABC):
    """SystemCall yielded by Task to handle with Scheduler"""

    @abstractmethod
    def handle(self, scheduler: 'Scheduler', task: 'Task') -> bool | int:
        """
        :param scheduler: link to scheduler to manipulate with active tasks
        :param task: task which requested the system call
        :return: an indication that the task must be scheduled again
        """


Coroutine = Generator[SystemCall | None, Any, None]


class Task:
    def __init__(self, task_id: int, target: Coroutine) -> None:
        """
        :param task_id: id of the task
        :param target: coroutine to run. Coroutine can produce system calls.
        System calls are being executed by scheduler and the result sends back to coroutine.
        """
        self.task_id = task_id
        self.target = target
        self.last_syscall_result = None

    def set_syscall_result(self, result: Any) -> None:
        """
        Saves result of the last system call
        """
        self.last_syscall_result = result

    def step(self) -> SystemCall | None:
        """
        Performs one step of coroutine, i.e. sends result of last system call
        to coroutine (generator), gets yielded value and returns it.
        """
        result = self.target.send(self.last_syscall_result)
        return result


class Scheduler:
    """Scheduler to manipulate with tasks"""

    def __init__(self) -> None:
        self.task_id = 1
        self.task_queue: Queue[Task] = Queue()
        self.task_map: dict[int, Task] = {}  # task_id -> task
        self.wait_map: dict[int, list[Task]] = {}  # task_id -> list of waiting tasks

    def _schedule_task(self, task: Task) -> None:
        """Add task into task queue
        :param task: task to schedule for execution
        """
        self.task_queue.put(task)

    def new(self, target: Coroutine) -> int:
        """Create and schedule new task
        :param target: coroutine to wrap in task
        :return: id of newly created task
        """
        new_task = Task(self.task_id, target)
        self._schedule_task(new_task)
        self.task_map[self.task_id] = new_task
        self.task_id += 1
        return self.task_id - 1

    def exit_task(self, task_id: int) -> bool:
        """PRIVATE API: can be used only from scheduler itself or system calls
        Hint: do not forget to reschedule waiting tasks
        :param task_id: task to remove from scheduler
        :return: true if task id is valid
        """

    def wait_task(self, task_id: int, wait_id: int) -> bool:
        """PRIVATE API: can be used only from scheduler itself or system calls
        :param task_id: task to hold on until another task is finished
        :param wait_id: id of the other task to wait for
        :return: true if task and wait ids are valid task ids
        """

    def run(self, ticks: int | None = None) -> None:
        """Executes tasks consequently, gets yielded system calls,
        handles them and reschedules task if needed
        :param ticks: number of iterations (task steps), infinite if not passed
        """
        i = 0
        while (ticks is not None and i < ticks) or ticks is None:
            i += 1
            if self.task_queue.empty():
                continue
            task_to_run = self.task_queue.get()
            # print("task_id  ", task_to_run.task_id)
            if task_to_run.task_id not in self.task_map:
                continue
            try:
                x = task_to_run.step()
                if x is not None:
                    tr = x.handle(self, task_to_run)
                    task_to_run.set_syscall_result(tr)
                    # print(tr)
                    if isinstance(x, WaitTask) and tr:
                        continue

            # print(self.task_queue, "Queue")
            except StopIteration:
                del self.task_map[task_to_run.task_id]
                try:
                    for task_to_reschedule in self.wait_map[task_to_run.task_id]:
                        self.task_queue.put(task_to_reschedule)
                except KeyError:
                    pass
                continue
            # try:
            #     for task_to_reschedule in self.wait_map[task_to_run.task_id]:
            #         self.task_queue.put(task_to_reschedule)
            # except KeyError:
            #     pass
            # print(x)
            self.task_queue.put(task_to_run)

    def empty(self) -> bool:
        """Checks if there are some scheduled tasks"""
        return not bool(self.task_map)


class GetTid(SystemCall):
    """System call to get current task id"""

    def handle(self, scheduler: Scheduler, task: Task) -> int | bool:
        # return False
        return task.task_id
        pass


class NewTask(SystemCall):
    """System call to create new task from target coroutine"""

    def __init__(self, target: Coroutine) -> None:
        self.target = target

    def handle(self, scheduler: Scheduler, task: Task) -> int | bool:
        return scheduler.new(self.target)
        pass


class KillTask(SystemCall):
    """System call to kill task with particular task id"""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id

    def handle(self, scheduler: Scheduler, task: Task) -> bool | int:
        try:
            scheduler.task_map[self.task_id].target.close()
            del scheduler.task_map[self.task_id]
        except KeyError:
            pass
        return False


class WaitTask(SystemCall):
    """System call to wait task with particular task id"""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id

    def handle(self, scheduler: Scheduler, task: Task) -> bool | int:
        # Note: One shouldn't reschedule task which is waiting for another one.
        # But one must reschedule task if task id to wait for is invalid.
        if self.task_id not in scheduler.task_map:
            return False
        if self.task_id in scheduler.wait_map:
            scheduler.wait_map[self.task_id].append(task)
        else:
            scheduler.wait_map[self.task_id] = [task]
        pass
        return True
