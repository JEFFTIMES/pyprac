
"""
    A non-length-limited queue, means the producers can put as many items as they want into the queue.
    However, the consumers have to wait if the queue is empty.

    The Queue exposes two interfaces, all are coroutines:
        put(), a coroutine that pushes an item into the queue at a time.
        get(), a coroutine that retrieves an item from the queue.
    
    In the current implementation, the put() calls the inner scheduler resume() to resume the consumers 
    waiting in the list self._consumer[].

    The event loop call only iterate all the tasks, not knowing the existence of the waiting list in 
    the queue.

"""

import types
import builtins

class Queue:
    """
    Attributes:
        _items: 
        _consumers:
    """

    def __init__(self, waits=10):
        """
        initialize the attributes
        """
        self._items = []  
        self._consumers = []
        self.waits = waits

    
    def resume(self, queue):
        """
        resume a waiting task from self._consumer[]
        it works as an inner scheduler, activates the consumer and exams the response 
        """
        if queue:
            task = queue.pop(0)
            print(f'resume(): task:{task}\twaiting list: {queue}')       
            try:
                response = task.send({
                    'resumer': 'producer',
                    'task': task
                })
            except StopIteration as err:
                response = err.value 
            print(f'resume(): resumed: {task}\tresponds: {response}')
        return None

    @types.coroutine
    def _put(self, item):
        """
        Add an item to the queue, wake up a consumer and yield the control.
        It pushes an item to the queue when it is initiated by the event loop, this is not an expected behavior.
        """
        print(f'put(): items: {self._items}\tconsumers: {self._consumers}')
        self._items.append(item)
        print(f'put(): items: {self._items}\tconsumers: {self._consumers}')
        self.resume(self._consumers)
        yield f'queue.put() has put {item} in {self._items}'                              


    @types.coroutine
    def put(self, item):
        """
        Add an item to the queue, wake up a consumer and yield the control.
        This version won't push an item during the initialize.
        """
        while True:
            activator = yield f'Producer is paused.'
            if activator:
                self._items.append(item)
                print(f'Producer: {activator['task']} reactivated by {activator['resumer']} and pushed {item}')
                print(f'put(): _items: {self._items}\t_consumers: {self._consumers}')
                self.resume(self._consumers)
                return None


    @types.coroutine
    def get(self):
        """
        Pops an item from the queue and returns it.
        Yields control when the event loop sends None to initiate the calling consumer.
        When the calling consumer is reactivated by the Event Loop or the Producer.
        if _items[] is empty: push the consumer in the waiting list _consumer[]
        if _items[] is not empty:
            if _consumer[] is empty: return an item from the queue _items[]
            if _consumer[] is not empty: push the consumer in the waiting list _consumer[]
        
        """
        while True:
            activator = yield 'Consumer is paused.'
            print(f'get(): task: {activator['task']}\treactivated by: "{activator['resumer']}",\t_items:{self._items}\t_consumers:{self._consumers}')
            if not self._items:                                             # empty queue
                if activator['resumer'] == 'event loop':                    # waken up by event loop
                    if activator['task'] not in self._consumers:            # only push the consumer to the waiting list once
                        self._consumers.append(activator['task'])       
                        print(f'---update _consumers: {activator['task']} appended, _consumers: {self._consumers}')
                    else:                                                   
                        if self.waits:                                      # don't let the consumer wait for every
                            print(f'---update _consumers: {activator['task']} was in, _consumers:{self._consumers}, self.waits: {self.waits}')
                            self.waits -= 1
                        else:
                            self._consumers.remove(activator['task'])
                            return f'Maximum getting retry exceeded, {activator['task']} returned'
                elif activator['resumer'] == 'producer':                    # waken up by inner scheduler resume(), not possible
                    print(f'It\'s not an expected path')
            else:                                                           # not empty queue, pop up an item
                item = self._items.pop(0)
                print(f'---Update items: {self._items}')
                return item
                
                


async def producer(name, count, queue):
    """
    A producer task that puts items into the queue.
    """
    for i in range(count):
        print(f'Producer: {name} is going to put item {i}')
        await queue.put(f'Item {i} from {name}')
        
    return f'Producer {name}: completed and returned'


@types.coroutine
def consumer(name, count, queue):
    """A consumer coroutine that takes items from the queue."""

    for i in range(count):
        print(f'Consumer: {name} is getting item from the queue on its {i+1}th iteration of total {count}.')
        item = yield from queue.get()
        print(f'Consumer {name} got: {item}')
    return f'Consumer {name}: completed and returned'


class SimpleEventLoop:
    """
    A simplified event loop that drives the producers and consumers to interactive with the queue.
    """
    def __init__(self,  queue, *tasks):
        """
        :param tasks: a tuple of tasks, type of coroutine.
        """
        self._queue = queue
        self._tasks = list(tasks)


    def run_until_complete(self):
        """
        Initiates all the tasks by sending None into them.
        Repeatedly Reactivate each task until reaching StopIteration.
        """
        # Initiating
        for task in self._tasks:
            response = task.send(None)
            print(f'Event Loop Initialized: {task},  it responds: "{response}"')
        
        while self._tasks:
            task = self._tasks.pop(0)
            try:
                response = task.send({
                    'resumer':'event loop',
                    'task':task
                })  # sending the task itself to reactivate it
                self._tasks.append(task)
            except StopIteration as err:
                response = err.value
            print(f'Event Loop Reactivated: {task}, it responds "{response}"')



def main():
    """Create producer and consumer tasks and start the event loop."""
    q = Queue()

    loop = SimpleEventLoop(
        q,
        consumer('C1', 6, q),
        consumer('C2', 5, q),
        producer('P1', 5, q),
        producer('P2', 5, q)

    )

    loop.run_until_complete()
    print(f'q._items: {q._items}\tq._consumers:{q._consumers}')


if __name__ == '__main__':
    main()
