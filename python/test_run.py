from concurrent.futures import ThreadPoolExecutor
import logging
from multiprocessing import Queue, freeze_support
from threading import Condition

from concurrency.task import Task
from concurrency.tasks.ptt_board_request import PttBoardRequest
from concurrency.workers.html_content_parser import HtmlContentParser
from concurrency.workers.parsed_content_merger import ParsedContentMerger
from concurrency.workers.ptt_board_reader import PttBoardReader

# Num of HTML request workers
NUM_OF_HTML_REQ_WORKERS = 3

# Num of HTML content parsers
NUM_OF_PARSERS = 3

def workers_are_idle(in_workers):
    """ Returns True if all workers are idel """
    ret_flag = True
    for worker in in_workers:
        if worker.is_working():
            ret_flag = False
            break
    return ret_flag


def start_process(init_task):
    """ Initializes executor, queues, and workers and starts process """
    # Init executer
    with ThreadPoolExecutor() as executor:
        logging.info("[Executor] Initialization ...")

        # Condition object
        executorCv = Condition()

        # Init queues:
        #   - HTTP request queue (Multiple workers)
        #   - HTML content parsing queue (Multiple workers)
        #   - Parsed content merging queue (1 worker)
        http_req_queue = Queue()
        parse_queue = Queue()
        merge_queue = Queue()

        # Init workers
        #   - HTML request workers
        http_req_workers = [PttBoardReader(f'HttpRequestWorker-{i}', \
                http_req_queue, {'parse_queue': parse_queue}, executorCv) \
                for i in range(NUM_OF_HTML_REQ_WORKERS)]

        #   - HTML content parsers
        parsers = [HtmlContentParser(f'Parser-{i}', parse_queue, {
                    'http_req_queue': http_req_queue,
                    'merge_queue': merge_queue
                }, executorCv) \
                for i in range(NUM_OF_PARSERS)]

        #   - Parsed content merger
        mergers = [ParsedContentMerger("Merger-0", merge_queue, \
                cv=executorCv)]

        # Start process
        logging.info("[Executor] Arranging workers ...")
        futures = [executor.submit(worker.run) for worker in \
                http_req_workers + parsers + mergers]

        # Initial task
        http_req_queue.put(init_task)

        # Monitor workers and queues
        logging.info("[Executor] Monitoring workers ...")
        flag_monitor = True
        while flag_monitor:
            with executorCv:
                # Wait for updates
                logging.info("[Executor] Waiting for notification ...")
                executorCv.wait()

                logging.info("[Executor] Received notification ...")
                # Examine HTML request workers
                if workers_are_idle(http_req_workers) and \
                        http_req_queue.empty() and \
                        workers_are_idle(parsers) and parse_queue.empty() and \
                        workers_are_idle(mergers) and merge_queue.empty():
                    # Indicate all workers should stop working
                    http_req_queue.put(Task.STOP)
                    parse_queue.put(Task.STOP)
                    merge_queue.put(Task.STOP)

                    # Exit loop
                    flag_monitor = False

        # Wait until all workers have returned results
        res = [future.result() for future in futures]
        logging.info("[Executor] Exit")


def test_start_process():
    # Log debug messages
    logging.basicConfig(format='%(asctime)s %(levelname)9s: %(message)s', \
            level=logging.DEBUG)

    # Freeze support for Windows
    freeze_support()

    start_process(PttBoardRequest('Baseball'))


if __name__ == '__main__':
    # Start process with a PTT Board Request
    test_start_process()

