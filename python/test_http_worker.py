import logging

from concurrency.tasks.http_request_task import HttpRequestTask
from concurrency.tasks.merge_ptt_content import MergePttContent
from concurrency.tasks.parse_ptt_board_index import ParsePttBoardIndex
from concurrency.tasks.ptt_board_request import PttBoardRequest
from concurrency.workers.html_content_parser import HtmlContentParser
from concurrency.workers.http_request_worker import HttlRequestWorker
from concurrency.workers.ptt_content_merger import PttContentMerger

def test_run_worker():
    # Create task
    task = PttBoardRequest('Baseball')

    # Handle task
    handler = HttlRequestWorker('Tester', None)
    parser = HtmlContentParser('Parser', None)

    # Run task and check result
    flag_res, http_content = handler.handle_task(task)
    #print(http_content)

    # Parse content task
    task_parse = ParsePttBoardIndex(http_content)
    flag_res, parsed_content = parser.handle_task(task_parse)
    print(parsed_content)

    # Test merger
    task_merge = MergePttContent(parsed_content)
    merger = PttContentMerger('Merger', None)
    flag_res, merged_content = merger.handle_task(task_merge)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)9s: %(message)s',
            level=logging.DEBUG)
    test_run_worker()

