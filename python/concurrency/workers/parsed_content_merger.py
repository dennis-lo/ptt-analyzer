""" A worker that merges parsed HTML content """

import logging

from ..task import Task
from ..tasks.merge_parsed_content import MergeParsedContent
from ..worker import Worker

class ParsedContentMerger(Worker):

    def verify_task(self, task):
        """ Returns True if the task is valid """
        return task == Task.STOP or isinstance(task, MergeParsedContent) and \
                task.data


    def handle_task(self, task):
        """ Handles task and returns results """
        logging.debug("Parsed content: %s", task.data)
        return (False, None)

