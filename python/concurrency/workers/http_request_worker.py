""" A worker that handles HTTP requests """

import urllib.request

from ..worker import Worker
from ..task import Task
from ..tasks.http_request_task import HttpRequestTask

class HttlRequestWorker(Worker):

    def verify_task(self, task):
        """ Returns True if the task is valid """
        return task == Task.STOP or isinstance(task, HttpRequestTask) and \
                task.url


    def handle_task(self, task):
        """ Handles task and returns results

        Arguments:
            task -      HTTP request task to be handled
        Returns:
            ret_flag -  Indicates whether the task is executed successfully
            ret_res -   Result of the execution
        """
        # Return flag and tasks
        ret_flag = False
        ret_res = None

        # Create a request object to update headers
        req = urllib.request.Request(task.url, data=task.get_data(), \
                headers=task.headers, method=task.method)

        # Retrieve content
        with urllib.request.urlopen(req) as resp:
            ret_res = resp.read().decode(task.charset)
            ret_flag = True

        # Return result
        return (ret_flag, ret_res)

