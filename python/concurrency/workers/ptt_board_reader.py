""" A worker that read content from a PTT board """

from ..task import Task
from ..tasks.parse_ptt_board_index import ParsePttBoardIndex
from ..tasks.ptt_board_request import PttBoardRequest
from .http_request_worker import HttlRequestWorker

class PttBoardReader(HttlRequestWorker):

    def verify_task(self, task):
        """ Returns True if the task is valid """
        return task == Task.STOP or isinstance(task, PttBoardRequest) and \
                task.url


    def handle_task(self, task):
        """ Handles task and returns results """
        # Reuse inherited method
        ret_flag, ret_res = super().handle_task(task)

        if ret_flag and ret_res:
            # Construct parse-content request
            self.feed_task(ParsePttBoardIndex(ret_res), 'parse_queue')

        # Return result
        return (ret_flag, ret_res)

