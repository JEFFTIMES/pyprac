
"""
    A non-length-limited queue, means the producers can put as many items as they want into the queue.
    However, the consumers have to wait if the queue is empty.

    The Queue exposes two interfaces, all are coroutines:
        put(), a coroutine that pushes an item into the queue at a time.
        get(), a coroutine that retrieves an item from the queue.
    
    In this implementation, the put() doesn't call the inner scheduler resume() to resume the consumers,
    letting the event loop to wake up the consumers.
    
    The event loop takes care of both iterating the tasks and waking up the tasks in the waiting list.
    Adding async_sleep(m) to the producer and consumer tasks to simulate the delayed incoming tasks.
"""

import types
import builtins
from random import shuffle, randint, random
import time

class Queue:
    """
    Attributes:
        _items: 
        _consumers:
    """

    def __init__(self, length:int = 100):
        """
        initialize the attributes
        """
        self._items = []  
        self._consumers = []
        self._producers = []
        self.length = length


    def is_consumer_waiting(self,):
        '''
        checking emptiness of waiting consumers
        '''
        return bool(self._consumers)


    def is_producer_waiting(self,):
        '''
        checking emptiness of waiting producers
        '''
        return bool(self._producers)
    
    
    def is_empty(self,):
        '''
        checking emptiness of the queue
        '''
        return not bool(self._items)
    
    
    def is_full(self,):
        '''
        checking fullness of the queue
        '''
        return not len(self._items) < self.length
    
    def clear_queue(self,):
        self._items.clear()

    @types.coroutine
    def put(self, item):
        """
        Add an item to the queue.
        In this version, it won't push an item during being initialized.
        Now, it keeps stateless.
        """
        try:
            while True:
                task = yield f'Producer is paused.'
                if task:
                    self._items.append(item)
                    return item
        except GeneratorExit as err:
            print(f'Queue.put(): calling producer has been terminated by the event loop') 


    @types.coroutine
    def get(self):
        """
        Pops an item from the queue and returns it.
        Now, it becomes stateless, doesn't take care of the checking the states of emptiness or 
        fullness of the queue and the waiting lists
        """
        try:
            while True:
                task = yield 'Consumer is paused.'
                if task:
                    item = self._items.pop(0)
                    return item
        except GeneratorExit:
            print(f'Queue.get(): calling consumer task has been terminated by the event loop')

@types.coroutine
def async_sleep(sec):
    '''
    sleep sec seconds before returning
    '''
    sleep_to = time.time() + sec
    while True:
        sig = yield sleep_to
        now = time.time()
        if now > sleep_to:
            return
    



async def producer(name, count, queue):
    """
    A producer task that puts items into the queue.
    """
    
    try:
        for i in range(count):
            await async_sleep(random())
            result = await queue.put(f'Item {i} from {name}')
            print(f'producer <{name}> in iter<{i}> has pushed <{result}>')
        return
    except GeneratorExit:
        print(f'producer <{name}> has been terminated at its <{i}>th iteration')
    

async def consumer(name, count, queue):
    """
    A consumer coroutine that takes items from the queue.
    """
    try:
        for i in range(count):
            await async_sleep(random()*3)
            item = await queue.get()
            print(f'consumer <{name}> in iter<{i})> has popped <{item}>')
        return
    except GeneratorExit:
        print(f'consumer<{name}> has been terminated at its <{i}>th iteration') 
    

class QueueEventLoop:
    """
    A simplified event loop that drives the producers and consumers to interactive with the queue.
    """
    
    def __init__(   
                    self, 
                    queue:Queue, 
                    producers:list, 
                    consumers:list, 
                    con_waits:int = 0, 
                    prod_waits: int = 0
                ):
        """
        initiate the event loop
        """
        self._queue = queue
        self._consumers = consumers
        self._producers = producers
        self._con_waits = len(self._consumers)//2 if not con_waits else con_waits 
        self._prod_waits = len(self._producers)//2 if not prod_waits else prod_waits
        self.init_counter = max(self._con_waits, self._prod_waits)

        self._tasks = [{'type':'consumer','inst':c, 'operation': 'activate'} for c in self._consumers] + [{'type':'producer', 'inst': p, 'operation':'activate'} for p in self._producers]
        shuffle(self._tasks) 

        
    def decide_to_proceed(self, monitored):
        '''
        decide which task to be proceeded in terms of the existence of the passed in task and the queue's status.
        the counter which represents the con_waits or the prod_waits is used to forcefully terminate the event loop. 
        '''
    
        is_consumer = monitored['type'] == 'consumer'

        queue_is_not_good = self._queue.is_empty() if is_consumer else self._queue.is_full()
        waiting_list = self._queue._consumers if is_consumer else self._queue._producers
        counter = self._con_waits if is_consumer else self._prod_waits
        
        if not queue_is_not_good:                       # queue is not empty or full
            if waiting_list:                              # tasks are waiting
                to_proceed = waiting_list.pop(0)
                to_proceed['operation'] = 'activate'

                if to_proceed != monitored and monitored not in waiting_list:
                    monitored['operation'] = 'skip'
                    waiting_list.append(monitored)
                return to_proceed, monitored           
            
            monitored['operation'] = 'activate'
            return monitored, monitored

        # queue is empty or full
        if counter:
            monitored['operation'] = 'skip'
            if monitored in waiting_list:
                counter -= 1
            else:
                counter = min(self.init_counter, counter + 1)
                waiting_list.append(monitored)

            # update counter
            if is_consumer:
                self._con_waits = counter
            else:
                self._prod_waits = counter
            return monitored, monitored
        
        # no more retries
        if monitored in waiting_list:
            waiting_list.remove(monitored)
        monitored['operation'] = 'terminate'
        return monitored, monitored
                

        # Use enums or constants for task types and operations
        is_consumer = monitored['type'] == 'consumer'
        
        # Direct attribute access instead of function calls
        queue_state = self._queue.is_empty() if is_consumer else self._queue.is_full()
        waiting_list = self._queue._consumers if is_consumer else self._queue._producers
        counter = self._con_waits if is_consumer else self._prod_waits
        
        if not queue_state:  # Good queue state
            if waiting_list:  # Tasks are waiting
                to_proceed = waiting_list.pop(0)
                to_proceed['operation'] = 'activate'
                
                if to_proceed != monitored and monitored not in waiting_list:
                    monitored['operation'] = 'skip'
                    waiting_list.append(monitored)
                return to_proceed, monitored
            
            monitored['operation'] = 'activate'
            return monitored, monitored
        
        # Bad queue state
        if counter:
            monitored['operation'] = 'skip'
            if monitored in waiting_list:
                counter -= 1
            else:
                counter = min(self.init_counter, counter + 1)
                waiting_list.append(monitored)
                
            # Update counter
            if is_consumer:
                self._con_waits = counter
            else:
                self._prod_waits = counter
            return monitored, monitored
        
        # No more retries
        if monitored in waiting_list:
            waiting_list.remove(monitored)
        monitored['operation'] = 'terminate'
        return monitored, monitored

    def run_until_complete(self):
        """
        Initiates all the tasks by sending None into them.
        Repeatedly Reactivate each task until reaching StopIteration.
        """

        # priming the tasks
        for task in self._tasks:
            response = task['inst'].send(None)
                
        # revisiting
        while self._tasks:
            task = self._tasks.pop(0)
            to_proceed, to_monitor = self.decide_to_proceed(task)
            if to_proceed != to_monitor:
                self._tasks.append(to_monitor)
                if to_proceed['operation'] == 'terminate':
                    to_proceed['inst'].close()
                    self._tasks.remove(to_proceed)      
                elif to_proceed['operation'] == 'activate':
                    try:
                        to_proceed['inst'].send(to_proceed)
                    except StopIteration:
                        self._tasks.remove(to_proceed)                      
            else:
                if to_proceed['operation'] == 'terminate':
                    to_proceed['inst'].close()
                elif to_proceed['operation'] == 'skip':
                    self._tasks.append(to_monitor)
                else:
                    try:
                        to_proceed['inst'].send(to_proceed)
                        self._tasks.append(to_monitor)
                    except StopIteration:
                        pass
        
        print('Event loop: all tasks have been activated or terminated ')
        


def main():
    """Create producer and consumer tasks and start the event loop."""
    q = Queue()
    producers = [ producer('P' + str(i), 30, q) for i in range(2) ]
    consumers = [ consumer('C' + str(i), 30, q) for i in range(3) ]
    loop = QueueEventLoop(q, producers, consumers,con_waits=10_000_000, prod_waits=100_000_000)
    loop.run_until_complete()

if __name__ == '__main__':
    main()
