import time
import queue
import threading

from loguru import logger
from api_server.settings import settings


class QueueManager:
    def __init__(self, max_concurrent_jobs=settings.max_concurrent_jobs, max_retries_jobs=settings.job_max_retries, retry_sleep_time_jobs=settings.retry_sleep_time_jobs):
        self.queue = queue.Queue()
        self.semaphore = threading.Semaphore(max_concurrent_jobs)
        self.max_retries = max_retries_jobs
        self.retry_sleep_time_jobs = retry_sleep_time_jobs
        self.start_workers()

    def start_workers(self):
        for _ in range(self.semaphore._value):
            worker_thread = threading.Thread(target=self.worker)
            worker_thread.start()

    def add_job(self, func, *args, **kwargs):
        self.queue.put((func, args, kwargs))

    def worker(self):
        while True:
            func, args, kwargs = self.queue.get()
            retries = 0
            while retries < self.max_retries:
                with self.semaphore:
                    try:
                        func(*args, **kwargs)
                        break
                    except Exception as e:
                        retries += 1
                        logger.error(f"Error executing function: {e}. Retry {retries}/{self.max_retries}")
                        time.sleep(self.retry_sleep_time_jobs)
            self.queue.task_done()
