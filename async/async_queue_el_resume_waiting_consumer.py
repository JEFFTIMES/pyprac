
"""
    A non-length-limited queue, means the producers can put as many items as they want into the queue.
    However, the consumers have to wait if the queue is empty.

    The Queue exposes two interfaces, all are coroutines:
        put(), a coroutine that pushes an item into the queue at a time.
        get(), a coroutine that retrieves an item from the queue.
    
    In this implementation, the put() doesn't call the inner scheduler resume() to resume the consumers,
    letting the event loop to wake up the consumers.
    
    The event loop takes care of both iterating the tasks and waking up the tasks in the waiting list.

    
"""

import types
import builtins
from random import shuffle, randint

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
                    #print(f'Queue.put(): {task['type']}: {task['inst']} updated the Queue.\nQueue: {self._items}\n')
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
                    #print(f'Queue.get(): {task['type']}: {task['inst']} popped the Queue.\nQueue:{self._items}')
                    return item
        except GeneratorExit as err:
            print(f'Queue.get(): calling consumer task has been terminated by the event loop')


async def producer(name, count, queue):
    """
    A producer task that puts items into the queue.
    """
    try:
        for i in range(count):
            result = await queue.put(f'Item {i} from {name}')
            print(f'producer <{name}> in iter<{i}> has pushed <{result}>')
        return f'producer <{name}> has completed <{i}>th iteration of pushing and returned'
    except GeneratorExit as err:
        print(f'producer <{name}> has been terminated at its <{i}>th iteration')
    

async def consumer(name, count, queue):
    """
    A consumer coroutine that takes items from the queue.
    """
    try:
        for i in range(count):
            item = await queue.get()
            print(f'consumer <{name}> in iter<{i})> has popped <{item}>')
        return f'consumer <{name}> has completed <{i}>th iteration of popping and returned'
    except GeneratorExit as err:
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

        self._tasks = [{'type':'consumer','inst':c, 'operation': 'activate'} for c in self._consumers] + [{'type':'producer', 'inst': p, 'operation':'activate'} for p in self._producers]
        shuffle(self._tasks) 
        
    def decide_to_proceed(self, monitored):
        '''
        
        '''
    
        def update_waits(task_type, counter):
            '''
            inner function to reduce counters con_waits or prod_waits
            '''
            if task_type == 'consumer':
                self._con_waits = counter 
            else:
                self._prod_waits = counter
        

        if monitored['type'] == 'consumer':
            is_queue_not_good = self._queue.is_empty 
            is_waiting = self._queue.is_consumer_waiting
            waiting_list = self._queue._consumers
            counter = self._con_waits  
        else:
            is_queue_not_good = self._queue.is_full
            is_waiting = self._queue.is_producer_waiting
            waiting_list = self._queue._producers
            counter = self._prod_waits

        if is_queue_not_good():                     # queue is empty or full
            if counter:                             
                monitored['operation'] = 'skip'
                to_proceed = monitored 
                if monitored in waiting_list:       # was existing in the waiting list, countdown the waits 
                    counter -= 1
                    update_waits(monitored['type'], counter)
                    #print(f'path: queue_not_good -> monitored in waiting list -> counter -1\n')
                else:                               # increase the waits up to the maximum retries, append the monitored to the waiting list
                    counter = min(1, counter+1)
                    update_waits(monitored['type'], counter)
                    waiting_list.append(monitored)
                    #print(f'path: queue_not_good -> monitored not in waiting list -> increase counter\n')
            else:                                   # retry counts has been exhausted, terminate the first task in the waiting list
                #print(f'path: queue_not_good -> counter == 0 ')
                if monitored in waiting_list: 
                    waiting_list.remove(monitored)
                monitored['operation'] = 'terminate'
                to_proceed = monitored    

        else:                                       
            if is_waiting():                        # other tasks are waiting
                to_proceed = waiting_list.pop(0)
                to_proceed['operation'] = 'activate'
                if to_proceed != monitored and \
                    monitored not in waiting_list:  # monitored is not in the waiting list and not the one being popped
                    monitored['operation'] = 'skip'
                    waiting_list.append(monitored)
            else:
                monitored['operation'] = 'activate'
                to_proceed = monitored
        return (to_proceed, monitored)
            



    def run_until_complete(self):
        """
        Initiates all the tasks by sending None into them.
        Repeatedly Reactivate each task until reaching StopIteration.
        """
        # Initiating
        for task in self._tasks:
            response = task['inst'].send(None)
        
        # revisiting
        while self._tasks:
            print('\n' + '='*100 + '\n')
            print(f'con_waits     : <{self._con_waits}>\nprod_waits    : <{self._prod_waits}> \ntasks         : <{len(self._tasks)}>\n')
            print(f'q.items       : <{len(self._queue._items)}><{self._queue._items})>\nq.waiting_prod: <{len(self._queue._producers)}>\nq.waiting_cons: <{len(self._queue._consumers)}>\n')
            
            task = self._tasks.pop(0)
            to_proceed, to_monitor = self.decide_to_proceed(task)
            
            #print(f'monitored : <{task}>\nto_monitor: <{to_monitor}>\nto_proceed: <{to_proceed}>\n')

            if to_proceed != to_monitor:
                #print('to_proceed != to_monitor')

                self._tasks.append(to_monitor)
                #print(f'Event loop saved: <{to_monitor}> back to the monitoring task list')

                if to_proceed['operation'] == 'terminate':
                    to_proceed['inst'].close()
                    self._tasks.remove(to_proceed)
                    #print(f'Event loop terminated: <{to_proceed}> and remove it from the monitoring task list')
                
                elif to_proceed['operation'] == 'skip':
                    print(f'Event loop skipped: <{to_proceed}>')

                else:
                    try:
                        to_proceed['inst'].send(to_proceed)
                        #print(f'Event Loop activated: <{to_proceed}>')
                    except StopIteration as err:
                        self._tasks.remove(to_proceed)
                        #print(f'Event Loop removed: <{to_proceed}> after it had completed and returned')
                    
            
            else:

                #print('to_proceed == to_monitor')

                if to_proceed['operation'] == 'terminate':
                    to_proceed['inst'].close()
                    #print(f'Event loop terminated: <{to_proceed}> and remove it from the monitoring task list')

                elif to_proceed['operation'] == 'skip':
                    #print(f'Event loop skipped: <{to_proceed}>, \nEvent loop saved: <{to_monitor}> back to the task list')
                    self._tasks.append(to_monitor)

                else:
                    try:
                        to_proceed['inst'].send(to_proceed)
                        self._tasks.append(to_monitor)
                        #print(f'Event Loop activated: <{to_proceed}>, \nEvent loop saved: <{to_monitor}> back to the task list')
                    except StopIteration as err:
                        pass
                        #print(f'Event Loop removed: <{to_proceed}> after it had completed and returned')
        
        print('Event loop: all tasks have been activated or terminated ')
        


def main():
    """Create producer and consumer tasks and start the event loop."""
    q = Queue()

    producers = [ producer('P' + str(i), randint(1, 10), q) for i in range(6) ]
    consumers = [ consumer('C' + str(i), randint(1,20), q) for i in range(5) ]

    loop = QueueEventLoop(q, producers, consumers)

    loop.run_until_complete()
    #print(f'q._items: {q._items}\tq._consumers:{q._consumers}\tq._producers{q._producers}')


if __name__ == '__main__':
    main()
