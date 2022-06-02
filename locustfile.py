# © 2021 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.

# This AWS Content is provided subject to the terms of the AWS Customer Agreement
# available at http://aws.amazon.com/agreement or other written agreement between
# Customer and either Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.

import time
from locust import User, task, between, Locust, TaskSet, SequentialTaskSet
import gevent.monkey
from dotenv import load_dotenv

from tasks import LocustTasks

gevent.monkey.patch_all()
import os

load_dotenv()
ENABLE_PIPELINE = os.environ.get("ENABLE_PIPELINE").lower() in ('true', '1', 't')
READ_TEST = os.environ.get('READ_TEST').lower() in ('true', '1', 't')
WRITE_TEST = os.environ.get('WRITE_TEST').lower() in ('true', '1', 't')



# @events.init_command_line_parser.add_listener
# def init_parser(parser):
#     parser.add_argument(
#         '--worker-id',
#         help="This worker's ID",
#         include_in_web_ui=False,
#         type=int
#     )

import globals
def increment():
    globals.CUSTOMER_ID += 1

class TaskSequence(SequentialTaskSet):
    wait_time = between(3, 5)
    def __init__(self, *args, **kwargs):
        super(TaskSequence,self).__init__(*args, **kwargs)
        time.sleep(2)


    def on_start(self):
        print("Increasing customer"+str(globals.CUSTOMER_ID))
        increment()

    @task
    def write_data_to_redis(self):
        if( not READ_TEST and WRITE_TEST):
            LocustTasks.write_only(worker_id=os.getpid())

    @task
    def write_read_data(self):
        if READ_TEST and WRITE_TEST:
            LocustTasks.write_read_together(worker_id=os.getpid())

    @task
    def read_data(self):
        if READ_TEST and not WRITE_TEST:
            LocustTasks.read_only(worker_id=os.getpid())

class UserTask(User):
    wait_time = between(2, 8)
    tasks = [TaskSequence]







