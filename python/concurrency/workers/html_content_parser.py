""" A worker that parses HTML content """

from ..task import Task
from ..tasks.merge_ptt_content import MergePttContent
from ..tasks.parse_content_task import ParseContentTask
from ..tasks.parse_ptt_article import ParsePttArticle
from ..tasks.parse_ptt_board_index import ParsePttBoardIndex
from ..worker import Worker
import ptt.parser


class HtmlContentParser(Worker):

    def verify_task(self, task):
        """ Returns True if the task is valid """
        return task == Task.STOP or isinstance(task, ParseContentTask) and \
                task.data

    def handle_task(self, task):
        """ Handles task and returns results """
        # Return flag and tasks
        ret_flag = False
        parsed_content = None

        if isinstance(task, ParsePttBoardIndex):
            # Parse board index
            parsed_content = ptt.parser.parse_index(task.data)

        elif isinstance(task, ParsePttArticle):
            # Parse article
            parsed_content = ptt.parser.parse_article(
                task.data,
                task.article_path)

        # Feed parsed content to merger
        if parsed_content:
            ret_flag = self.feed_task(MergePttContent(parsed_content),
                                     'merge_queue')

        return (ret_flag, None)
