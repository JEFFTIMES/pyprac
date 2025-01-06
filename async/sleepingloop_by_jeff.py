"""
Try to create(duplicate) the sleeping loop by Brett Cannon.

To my understanding, 3 crucial parts compose the async event loop: a scheduler; some coroutines that yield the control
back to the scheduler while they are doing their job in the background; the tasks(business logical) depend on the
returning results of the coroutines.

The scheduler does:
    (1) receiving the tasks(coroutines)
    (2) starting the tasks
    (3) queuing them in a certain order, by comparing the status of each task.
    (4) revisiting the queued tasks, checking the completion of each task by triggering exception StopIteration.
        update the status of the revisited task and push it back to the queue for next visiting if StopIteration
        has not been triggered.

In the sleeping loop case, the function run_to_complete(), as the scheduler does:
    (1) receives the tasks,
    (2) starts them and pushes the tasks in a priority queue.
    (3) the pqueue sorts the tasks by comparing the delayed_to stats of the tasks.
    (4) the scheduler forms a while loop that pops the task having the least delayed_to value from the pqueue, sending
        the current time into the task to wake it up. the scheduler updates the task's wait_until and pushes it back
        into the pqueue if exception StopIteration is not triggered. Otherwise, discards the exhausted task.

The second element, the background coroutine does:
    (1) receives the signal--started from the scheduler, forwarded by the calling task--being sent in and starts the
        job of itself.
    (2) yields the control along with a stat to the calling task while the coroutine is doing its job in the background,
        then the task forwards the yielded control to the scheduler. the calling task does not catch the stats, it only
        catch the returned value from the background coroutine.
    (3) waits for the revisiting of the scheduler(by receiving another signal), returns the value to the calling task
        if the background job is completed. Otherwise, yields the control as well as a stat, waits for the next
        revisiting.

In this case, the sleep(), acts as the background coroutine, and the countdown() is the calling task. When the event
loop send(None) to initiate each task, the sleep() receives the signal forwarded by the calling task and starts its
background job: sets up the wakeup time then yield the value back to the event loop, simply waits for being sent in
the signal. When the event loop revisits a coroutine sleep() and sends in a timestamp value, the sleep() subtract its
wakeup timestamp from it and returns result.

The third part of the event loop are the tasks that represent some business logic could be executed asynchronously
because the section of the business logic that is fulfilled by calling the awaitable coroutine. In this case,
each countdown pauses itself for 1 second between two counts. By employing the asynchronous, instead of blocking the
whole process, it yields the control to the scheduler letting the scheduler set off other countdown(s).

a helper class Task is provided to wrap each countdown with its waiting duration, which makes the tasks comparable
when the tasks are pushed in the priority queue.
"""

import time
import heapq
import types
import datetime


class Task:
    """
    A helper class Task that wraps each countdown coroutine with the next waking up time stamp,
    which makes the tasks comparable when the tasks are pushed in the priority queue. 
    """

    def __init__(self, wait_until, coro):
        self.wait_until = wait_until
        self.coro = coro

    def __lt__(self, other):
        return self.wait_until < other.wait_until

    def __eq__(self, other):
        return self.wait_until == other.wait_until


class SleepingLoop:

    def __init__(self, *coros):
        self._coros = list(coros)
        self._tasks = []

    def run_until_complete(self):
        """
        receives a list of coroutines, initializes them and pushes them in a heapq,
        forms a while loop to exhaust all coroutines.
        """
        # sends None to each coroutine to initialize them, expects a datetime object that represents the absolute
        # time to be delayed to. wraps the coroutine along with the delayed_to into a Task instance and pushes it in
        # the heapq _tasks.
        for coro in self._coros:
            delayed_to = coro.send(None)
            heapq.heappush(self._tasks, Task(delayed_to, coro))

        # forms a while loop to exhaust all the tasks
        while self._tasks:
            # pops up the task with the least waiting time
            task = heapq.heappop(self._tasks)

            # if the current time is ahead of the wait_until time of the task that has the least waiting time
            # the event loop has to block itself to the wait_until time.
            if (now := datetime.datetime.now()) < task.wait_until:
                wait_for = task.wait_until - now
                time.sleep(wait_for.total_seconds())

            # wakes up the countdown by sending 'now' into it, and expects a wait_until to be yield
            # update the task's variable wait_until and pushes the task back into the queue.
            # once the countdown is completed, a StopIteration exception is raised, no more 
            try:
                task.wait_until = task.coro.send(datetime.datetime.now())
                heapq.heappush(self._tasks, task)

            except StopIteration:
                print('One countdown complete.')


async def countdown(title, counts, delay=0):
    """
    the business logic is counting down the counts to zero with 1 second pause in between.
    the starting could be delayed. It yields the control to the scheduler while being paused 
    between two counts. It calls sleep() to achieve the delay starting and the pauses between
    two counts.
    """

    delayed = await sleep(delay)
    print(f'{title} starts to count down from {counts} after being delayed {delayed} seconds.')

    while counts:
        paused = await sleep(1)
        counts -= 1
        print(f'{title} counts down to {counts} after being paused {paused} seconds.')

    print(f'{title} completed.')


@types.coroutine
def sleep(seconds):
    """
    receives the sleep duration and turns it to an absolute datetime object wait_until representing
    the upcoming future time, and yield it to the scheduler. 
    calculates the actual eclipsed and return it when being resumed
    """

    now = datetime.datetime.now()
    wait_until = now + datetime.timedelta(seconds=seconds)
    actual = yield wait_until
    return actual - now


def main():
    """creates 3 countdown tasks and passes them to the SleepingLoop instance, starts the event loop.
    """
    start_from = datetime.datetime.now()
    loop = SleepingLoop(countdown('Jeff', 7), countdown('Lily', 4, delay=2), countdown('Victor', 5, delay=1))
    loop.run_until_complete()
    end_at = datetime.datetime.now()
    print(f'the event loop exhausted 3 jobs of total 16 countdowns in {(end_at - start_from).total_seconds()} seconds.')


if __name__ == '__main__':
    main()
