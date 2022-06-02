# © 2021 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.

# This AWS Content is provided subject to the terms of the AWS Customer Agreement
# available at http://aws.amazon.com/agreement or other written agreement between
# Customer and either Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
import random
import time
import datetime
from locust import User, task, between, Locust, TaskSet, SequentialTaskSet, events
import gevent
import subprocess
import gevent.monkey

gevent.monkey.patch_all()
# import psycogreen.gevent
#
# psycogreen.gevent.patch_psycopg()
from main import ExecuteRedisTest, TOTAL_CUSTOMERS

ENABLE_PIPELINE = False
BULK_READ = False
BULK_WRITES = False

HASH = "fe1efc53f8ff67db8043666185cd3e5d99f94f46"
import globals
def increment():
    globals.CUSTOMER_ID += 1

execObj = ExecuteRedisTest(pipeline=ENABLE_PIPELINE)
class TaskSequence(SequentialTaskSet):
    wait_time = between(3, 5)
    def __init__(self, *args, **kwargs):
        super(TaskSequence,self).__init__(*args, **kwargs)
        time.sleep(2)
        self.iter = 0


    def on_start(self):
        # self.execObj.generate_customer_id()
        print("Increasing customer"+str(globals.CUSTOMER_ID))
        increment()


    # @task
    # def write_single_user_to_redis(self):
    #     start = time.time()
    #     print("Executing WRITE")
    #     try:
    #         execObj.generate_data(is_bulk=BULK_WRITES)
    #         resp_time = int((time.time() - start) * 1000)
    #         events.request_success.fire(request_type="Redis write",name="Write Success",response_time = resp_time,response_length=512)
    #     except Exception as e:
    #         resp_time = int((time.time() - start) * 1000)
    #         events.request_failure.fire(request_type="Redis write", name="Write Failed", response_time=resp_time,
    #                                     response_length=1,exception=e)

    @task
    def read_single_user_from_redis(self):
        print("Executing Not READS")
        feature_id = str(self.iter)
        self.iter += 1
        version = '_1.0'
        customer_id = '{0:06}'.format(globals.CUSTOMER_ID)
        key = "{"+random.choice(['A_', 'C_'])+customer_id+"}"
        args = "1" +" "+version
        # command = "redis-cli -c -p 6379   -a 'a-very-complex-password-here'  --eval /Users/Ashish/Documents/projects/jkhunt/redisupwork/test.lua "+key + " , " +args
        start = time.time()
        try:
            # result = subprocess.run([command], stdout=subprocess.PIPE,shell=True)
            # print(result.stdout)
            print(execObj.cluster_client.evalsha(HASH,1,'{C_000001}'+ ' , '+args))
            resp_time = int((time.time() - start) * 1000)
            events.request_success.fire(request_type="Lua Redis Reads", name="Read Success", response_time=resp_time,
                                        response_length=512)
        except Exception as e:
            resp_time = int((time.time() - start) * 1000)
            events.request_failure.fire(request_type="Lua Redis Reads", name="Read Failed", response_time=resp_time,
                                    response_length=1,exception= e)
        # self.user.environment.runner.quit()


class UserTask(User):
    wait_time = between(0, 1)
    tasks = [TaskSequence]






