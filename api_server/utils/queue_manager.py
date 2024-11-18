import uuid
import time
import queue
import threading
from loguru import logger
from api_server.settings import settings


class QueueManager:
    def __init__(
        self,
        max_concurrent_jobs=settings.max_concurrent_jobs,
        max_retries_jobs=settings.job_max_retries,
        retry_sleep_time_jobs=settings.retry_sleep_time_jobs,
        max_queue_size=settings.max_queue_size  # 新增參數：控制佇列大小
    ):
        # 初始化具有最大大小的佇列
        self.queue = queue.Queue(maxsize=max_queue_size)
        self.semaphore = threading.Semaphore(max_concurrent_jobs)
        self.max_retries = max_retries_jobs
        self.retry_sleep_time_jobs = retry_sleep_time_jobs
        self.task_status = {}  # 用來追蹤任務的狀態
        self.start_workers()

    def start_workers(self):
        for _ in range(self.semaphore._value):
            worker_thread = threading.Thread(target=self.worker, daemon=True)  # 設置為守護執行緒
            worker_thread.start()

    def add_job(self, func, *args, **kwargs):
        task_id = str(uuid.uuid4())  # 生成唯一任務 ID

        # 檢查佇列是否滿載
        if self.queue.full():
            logger.warning(f"Queue is full. Task {task_id} rejected.")
            self.task_status[task_id] = {"status": "rejected", "result": None, "error": "Queue is full"}
            return task_id

        # 將任務加入佇列並初始化狀態
        self.task_status[task_id] = {"status": "pending", "result": None, "error": None}
        self.queue.put((task_id, func, args, kwargs))
        return task_id

    def get_task_status(self, task_id):
        return self.task_status.get(task_id, {"status": "not_found"})

    def worker(self):
        while True:
            task_id, func, args, kwargs = self.queue.get()
            retries = 0
            while retries < self.max_retries:
                with self.semaphore:
                    try:
                        logger.info(f"Executing task {task_id}")
                        result = func(*args, **kwargs)  # 執行實際任務
                        self.task_status[task_id] = {"status": "completed", "result": result, "error": None}
                        break
                    except Exception as e:
                        retries += 1
                        logger.error(f"Task {task_id} failed with error: {e}. Retry {retries}/{self.max_retries}")
                        time.sleep(self.retry_sleep_time_jobs)
            else:
                self.task_status[task_id] = {"status": "failed", "result": None, "error": f"Max retries reached: {e}"}
            self.queue.task_done()
