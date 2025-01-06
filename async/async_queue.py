import types


class Queue:
    """A simplified queue that works with the custom event loop."""

    def __init__(self):
        self._items = []  # List of items in the queue
        self._getters = []  # List of coroutines waiting for items


    def resume_getter(self,):
        if self._getters:
            getter = self._getters.pop(0)
            try:
                getter.send(None)
            except StopIteration:
                print(f'getter: {getter} has completed.')


    @types.coroutine
    def put(self, item):
        """
        Add an item to the queue.
        """
        self._items.append(item)            # Add the item to the queue
        self.resume_getter()
        yield                               # Yield control back to the event loop

    @types.coroutine
    def get(self):
        """
        Remove and return an item from the queue.
        """
        print(f'how many getters: {len(self._getters)}')
        while not self._items:      # pauses the consumer's getting when the queue is empty
            getter = yield          # if a None is forwarded in, means initiating or being resumed by the queue to get item
            if getter is not None:  # if a coroutine is forwarded in, means the consumer being revisited by the event loop
                self._getters.append(getter)    # then put it in the waiting list again to get items
        return self._items.pop(0)   # Remove and return the first item in the queue


class SimpleEventLoop:
    """A simplified event loop that only manages coroutines for the queue."""

    def __init__(self, *coros):
        self._coros = list(coros)  # List of coroutines to run
        print(self._coros)


    def run_until_complete(self):
        # start all producers and consumers,
        for coro in self._coros:
            coro.send(None)  # send None to start a coroutine

        while self._coros:
            coro = self._coros.pop(0)  # Get the next coroutine to run
            try:
                # Resume the coroutine and advance to the next yield point
                coro.send(coro)
                # Add the coroutine back to the list to continue execution
                self._coros.append(coro)
            except StopIteration:
                # The coroutine has completed
                print(f'{coro} completes.')

@types.coroutine
def producer(name, q, count):
    """A producer coroutine that puts items into the queue."""
    for i in range(count):
        print(f'Producer {name} put item {i}')
        yield from q.put(f'Item {i} from {name}')
    return None

@types.coroutine
def consumer(name, q):
    """A consumer coroutine that takes items from the queue."""

    while True:
        item = yield from q.get()
        print(f'Consumer {name} got {item}')



def main():
    """Create producer and consumer tasks and start the event loop."""
    q = Queue()

    loop = SimpleEventLoop(
        consumer('C1', q),
        #consumer('C2', q),
        producer('P1', q, 3),
        #producer('P2', q, 2)

    )

    loop.run_until_complete()


if __name__ == '__main__':
    main()
