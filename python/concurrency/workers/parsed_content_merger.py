""" A worker that merges parsed HTML content """

import logging

from ..task import Task
from ..tasks.merge_parsed_content import MergeParsedContent
from ..worker import Worker


class ParsedContentMerger(Worker):

    def __init__(self, name, consuming_queue, feeding_queues=None, cv=None):
        """ Initializes content merger

        Arguments:
            name -              Name of the merger
            consuming_queue -   Queue from which a task should be retrieved
            feeding_queues -    Dict of queues into which a task should be put
            cv -                Condiction object
        """
        super().__init__(name, consuming_queue, feeding_queues=feeding_queues,
                cv=cv)

        # Initialize dict for merged content
        self.merged_content = {}

    def verify_task(self, task):
        """ Returns True if the task is valid """
        return task == Task.STOP or isinstance(task, MergeParsedContent) and \
                task.data

    def handle_task(self, task):
        """ Handles task and returns results """
        logging.debug("[%s] Parsed content: %s", self.name, task.data)
        return (False, None)
