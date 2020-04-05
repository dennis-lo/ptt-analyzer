""" A worker that merges content parsed from PTT """

import logging

from ..task import Task
from ..tasks.merge_ptt_content import MergePttContent
from ..tasks.ptt_article_request import PttArticleRequest
from ..tasks.ptt_board_request import PttBoardRequest
from .parsed_content_merger import ParsedContentMerger
import ptt.merger


class PttContentMerger(ParsedContentMerger):

    def __init__(self, name, consuming_queue, feeding_queues=None, cv=None,
            min_article_num=30):
        """ Initializes PTT content merger

        Arguments:
            name -              Name of the merger
            consuming_queue -   Queue from which a task should be retrieved
            feeding_queues -    Dict of queues into which a task should be put
            cv -                Condiction object
            min_article_num -   Min num of articles should be read before
                                existing
        """
        super().__init__(name, consuming_queue, feeding_queues=feeding_queues,
                         cv=cv)
        self.min_article_num = min_article_num

    def verify_task(self, task):
        """ Returns True if the task is valid """
        return task == Task.STOP or isinstance(task, MergePttContent) and \
                task.data

    def handle_task(self, task):
        """ Handles task and returns results """
        ret_flag = False
        ret_res = None

        # Determine type of content
        if task.data['type'] == 'board':
            # Merge parsed content of a board
            ptt.merger.merge_index_pages(self.merged_content, task.data)

            # Update count
            count_articles = self.merged_content['count']

            # Board name
            board_name = self.merged_content['name']

            if count_articles < self.min_article_num:
                # Previous page number
                page_num = self.merged_content['page_num'] - 1

                # Retrieve list of articles from the previous page
                self.feed_task(
                    PttBoardRequest(board_name, page_num),
                    'http_req_queue')

                # Indicate that the task has been handled properly
                ret_flag = True

            elif self.merged_content['articles']:
                # Proceed and retrieve articles
                for article_page in self.merged_content['articles'].keys():
                    self.feed_task(PttArticleRequest(board_name, article_page),
                                   'http_req_queue')

                # Indicate that the task has been handled properly
                ret_flag = True

        elif task.data['type'] == 'article':
            # Merge parsed content of an article
            ptt.merger.merge_article_content(self.merged_content['articles'],
                                             task.data)

            # Return merged content
            ret_res = self.merged_content

        # Subsequent request
        logging.debug("[%s] Merged content: %s", self.name,
                      self.merged_content)
        return (ret_flag, ret_res)
