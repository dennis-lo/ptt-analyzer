from concurrent.futures import ThreadPoolExecutor
import logging
from multiprocessing import Queue, freeze_support
from threading import Condition

from concurrency.task import Task
from concurrency.tasks.ptt_board_request import PttBoardRequest
from concurrency.workers.html_content_parser import HtmlContentParser
from concurrency.workers.ptt_content_reader import PttContentReader
from concurrency.workers.ptt_content_merger import PttContentMerger

# Num of HTML request workers
NUM_OF_HTML_REQ_WORKERS = 3

# Num of HTML content parsers
NUM_OF_PARSERS = 2

def workers_are_idle(in_workers):
    """ Returns True if all workers are idel """
    ret_flag = True
    for worker in in_workers:
        if worker.is_working():
            ret_flag = False
            break
    return ret_flag


def start_process(board_name):
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
        workers = [PttContentReader(f'HttpRequestWorker-{i}',
                http_req_queue, {'parse_queue': parse_queue}, executorCv)
                for i in range(NUM_OF_HTML_REQ_WORKERS)]

        #   - HTML content parsers
        workers += [HtmlContentParser(f'Parser-{i}', parse_queue, {
                    'http_req_queue': http_req_queue,
                    'merge_queue': merge_queue
                }, executorCv)
                for i in range(NUM_OF_PARSERS)]

        #   - Parsed content merger
        workers += [PttContentMerger("Merger-0", merge_queue,
                {'http_req_queue': http_req_queue}, cv=executorCv)]

        # Start process
        logging.info("[Executor] Arranging workers ...")
        futures = [executor.submit(worker.run) for worker in workers]

        # Initial task
        http_req_queue.put(PttBoardRequest(board_name))

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
                if workers_are_idle(workers) and \
                        http_req_queue.empty() and \
                        parse_queue.empty() and \
                        merge_queue.empty():
                    # Indicate all workers should stop working
                    http_req_queue.put(Task.STOP)
                    parse_queue.put(Task.STOP)
                    merge_queue.put(Task.STOP)

                    # Exit loop
                    flag_monitor = False

        # Wait until all workers have returned results
        lst_res = [future.result() for future in futures]

        # Collect results
        for res in lst_res:
            if res:
                logging.info("[Executor] Result: %s", res)
        logging.info("[Executor] Exit")

def test_start_process():
    # Log debug messages
    logging.basicConfig(format='%(asctime)s %(levelname)9s: %(message)s',
                        level=logging.INFO)

    # Freeze support for Windows
    freeze_support()

    start_process('Baseball')


if __name__ == '__main__':
    # Start process with a PTT Board Request
    test_start_process()
