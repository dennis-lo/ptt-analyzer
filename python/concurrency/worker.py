""" A worker that handles tasks received from a queue """

import logging
from threading import Lock

from .task import Task

class Worker():
    def __init__(self, name, consuming_queue, feeding_queues={}, cv=None):
        # Name of the worker
        self.name = name

        # Queue from which the worker should receive tasks
        self.consuming_queue = consuming_queue

        # Array of queues to which the worker should feed tasks
        self.feeding_queues = feeding_queues

        # Working status
        self.flag_working = False

        # Condition object
        self.cv = cv

        # Status lock
        self.status_lock = Lock()


    def is_working(self):
        """ Returns True if worker is busy """
        ret_flag = False

        # Check status after acquiring lock
        with self.status_lock:
            ret_flag = self.flag_working

        # Return result
        return ret_flag


    def set_flag_working(self, flag_working):
        """ Updates flag to indicate whether worker is idle or busy """
        with self.status_lock:
            self.flag_working = flag_working


    def feed_task(self, task, name=None):
        """ Feeds task into the specified queue """
        if name == None:
            # Queue name is missing, loop through all feeding queues
            for name in self.feeding_queues.keys():
                self.feed_task(task, name)

        elif name and self.feeding_queues:
            # Feed task to queue retrieved from map
            self.put_task_to_queue(self.feeding_queues.get(name), task)


    def put_task_to_queue(self, queue, task):
        """ Puts task into queue """
        if queue and task:
            try:
                # Try feeding task into queue
                queue.put(task)

            except ValueError as err:
                # Queue might have been closed
                logging.error("Error while feeding task into queue: %s", err)


    def retrieve_task(self):
        """ Retrieves task from queue """
        ret_task = None

        # Try retrieving task from queue
        if self.consuming_queue:
            try:
                ret_task = self.consuming_queue.get()

            except ValueError as err:
                # Queue is closed
                logging.error("Error while retrieving task from queue: %s", \
                        err)

        # Return retrieved task
        return ret_task


    def return_task(self, task):
        """ Returns task to the consuming queue """
        self.put_task_to_queue(self.consuming_queue, task)


    def run(self):
        """ Starts working as a workers """
        logging.debug(f'[{self.name}] Starts working ...')
        # Indicate whether the process should remain running
        flag_continue = True

        while flag_continue:
            # Try receive task from queue
            in_task = self.retrieve_task()

            if in_task != None:
                if not self.verify_task(in_task):
                    # Invalid task
                    logging.warning(f'[{self.name}] Invalid Task')

                elif in_task == Task.STOP:
                    logging.debug(f'[{self.name}] Received STOP')

                    # Stop worker
                    flag_continue = False

                    # Return task to queue
                    self.return_task(in_task)

                else:
                    logging.debug(f'[{self.name}] Received task')

                    # Indicate worker is busy
                    self.set_flag_working(True)

                    # Handle task
                    self.handle_task(in_task)

                    # Indicate worker is idle again
                    self.set_flag_working(False)

                # Notify that task has been completed
                if self.cv != None:
                    with self.cv:
                        self.cv.notify_all()

        # Return result
        return None


    # Override this method if necessary
    def verify_task(self, task):
        """ Returns True if the task is valid """
        return task == Task.STOP or isinstance(task, Task)


    # Override this method
    def handle_task(self, task):
        """ Handles task and returns results """
        pass

