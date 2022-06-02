import time, logging, os

from dotenv import load_dotenv
from locust import events

from main import ExecuteRedisTest
load_dotenv()
ENABLE_PIPELINE = os.environ.get("ENABLE_PIPELINE").lower() in ('true', '1', 't')
execObj = ExecuteRedisTest(pipeline=ENABLE_PIPELINE)


class LocustTasks:
    @staticmethod
    def write_only(is_bulk=None, worker_id = None):
        logging.info("Executing WRITE")
        start = time.time()
        try:
            execObj.write_data(worker_id=worker_id)
        except Exception as e:
            logging.error(e)
            resp_time = int((time.time() - start) * 1000)
            events.request_failure.fire(request_type="Redis write", name="Write Failed", response_time=resp_time,
                                        response_length=1, exception=e)

    @staticmethod
    def read_only(worker_id=None):
        execObj.read_data_using_worker_id(worker_id)

    @staticmethod
    def write_read_together(worker_id=None):
        logging.info("Executing WRITE")
        start = time.time()
        try:
            execObj.write_read_data(worker_id=worker_id)
        except Exception as e:
            logging.error(e)
            resp_time = int((time.time() - start) * 1000)
            events.request_failure.fire(request_type="Redis write", name="Write Failed", response_time=resp_time,
                                        response_length=1, exception=e)

