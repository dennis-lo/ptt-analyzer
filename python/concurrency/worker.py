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
            retFlag = self.flag_working

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

        elif name and self.feeding_queues and \
                self.feeding_queues.get(name) and task:
            # Try feeding task into queue
            try:
                self.feeding_queues.get(name).put(task)

            except ValueError as err:
                # Queue is closed
                logging.error("Error while feeding task into queue:", err)


    def retrieve_task(self):
        """ Retrieves task from queue """
        ret_task = None

        # Try retrieving task from queue
        if self.consuming_queue:
            try:
                ret_task = self.consuming_queue.get()

            except ValueError:
                # Queue is closed
                logging.error("Error while retrieving task from queue: " + err)

        # Return retrieved task
        return ret_task


    def run(self):
        """ Starts working as a workers """
        logging.debug(f'[{self.name}] Start working ...')
        # Indicate whether the process should remain running
        flag_continue = True

        while flag_continue:
            # Try receive task from queue
            in_task = self.retrieve_task()

            if in_task != None:
                if in_task == Task.STOP:
                    logging.debug(f'{self.name} Received STOP')

                    # Stop worker
                    flag_continue = False

                    # Return task to queue
                    self.feed_task(in_task)

                else:
                    logging.debug(f'{self.name} Received task')

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

    # Override this method
    def handle_task(self, task):
        """ Handles task and returns results """
        pass

