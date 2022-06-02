import os, sys
import time
from ReadTest import ReadTest
from redisHandler import RedisHandler
import pickle
from dotenv import load_dotenv
import globals
from locust import events
import logging
TOTAL_CUSTOMERS = 6000
ENTRY_PER_CUSTOMER = 1000
TTL = 1800
BATCH_SIZE = 10000
load_dotenv()

class ExecuteRedisTest():
    def __init__(self,via_lua=False,pipeline=True):
        if not via_lua:
            self.cluster_client = RedisHandler(pipeline=pipeline, password=os.environ.get('PASSWORD'))
        else:
            self.cluster_client = None
        self.added_keys = []
        self.customer_id = None
        self.user_id = 0
        self.hashtag=None

    def generate_data_for_customer(self,customer_id,iter):
        versions = ['_1.0']
        version = versions[0] #random.choice(versions)
        ct = int(round(time.time() * 1000))
        event_timestamp = int(round(time.time() * 1000))
        feature_id = iter
        #binary = b64encode(os.urandom(200)).decode('utf-8')
        binary = 'ayataseaasdacaqwaaaartyaaabgtuaiaoaapamaallbnkauuiopa'
        mapValues = {
             #"pk": customer_id,
             #"sk": str(feature_id) + version,
             "b": binary,
             "ct": ct,
             "ev": event_timestamp
        }
        key = customer_id
        self.hashtag = "{"+key+"}:"+str(feature_id)+":"+version
        return (key,self.hashtag,mapValues)

    def generate_customer_id(self,worker_id,user_id):
        entity_id = '{0:07}'.format(user_id)
        # entity_id = str(uuid.uuid1())
        # entity_names = ['A_', 'C_']
        entity_name = 'A_'
        customer_id = str(worker_id) +'_'+entity_name + entity_id
        return customer_id

    def write_data_no_pipeline(self,worker_id=None):
        # no pipeline
        for user_iter in range(TOTAL_CUSTOMERS):
            customer_id = self.generate_customer_id(worker_id, user_iter)
            for iter in range(ENTRY_PER_CUSTOMER):
                key, hashtag, value = self.generate_data_for_customer(customer_id, iter)
                logging.info("Writing key " + hashtag)
                start_time = time.time()
                try:
                    self.cluster_client.setHashWithExpire(key, hashtag, value, TTL)
                    resp_time = int((time.time() - start_time) * 1000)
                    events.request_success.fire(request_type="Single write", name="Write Success",
                                                response_time=resp_time, response_length=512)
                except Exception as e:
                    logging.error(str(e))
                    resp_time = int((time.time() - start_time) * 1000)
                    events.request_failure.fire(request_type="Single write", name="Write Failure",
                                                response_time=resp_time, response_length=512, exception=e)

    def write_data_pipeline(self,worker_id=None):
        batch = 0
        for user_iter in range(TOTAL_CUSTOMERS):
            keys = []
            customer_id = self.generate_customer_id(worker_id,user_iter)
            for iter in range(ENTRY_PER_CUSTOMER):
                key,hashtag,value = self.generate_data_for_customer(customer_id,iter)
                logging.info("Writing key " + hashtag)
                keys.append(hashtag)
                batch += 1
                self.cluster_client.setHashWithExpire(key,hashtag,value,TTL)
                if self.cluster_client.pipeline and batch>=BATCH_SIZE:
                    start_time = time.time()
                    try:
                        logging.info("Executing Write")
                        self.cluster_client.pipeline.execute()
                        resp_time = int((time.time() - start_time) * 1000)
                        events.request_success.fire(request_type="Pipeline Bulk write", name="Write Success",
                                                    response_time=resp_time, response_length=512)
                    except Exception as e:
                        logging.error(str(e))
                        resp_time = int((time.time() - start_time) * 1000)
                        events.request_failure.fire(request_type="Pipeline Bulk read", name="Write Failure",
                                                    response_time=resp_time, response_length=512, exception=e)
                    batch=0
                    keys = []
        if self.cluster_client.pipeline and batch > 0:
            start_time = time.time()
            try:
                logging.info("Executing Write")
                self.cluster_client.pipeline.execute()
                resp_time = int((time.time() - start_time) * 1000)
                events.request_success.fire(request_type="Pipeline Bulk write", name="Write Success",
                                            response_time=resp_time, response_length=512)
            except Exception as e:
                logging.error(str(e))
                resp_time = int((time.time() - start_time) * 1000)
                events.request_failure.fire(request_type="Pipeline Bulk read", name="Write Failure",
                                            response_time=resp_time, response_length=512, exception=e)

    def generate_data(self,is_bulk=None,worker_id=None):
        # legacy fumction
        if is_bulk:
            batch = 0
            for user_iter in range(TOTAL_CUSTOMERS):
                keys = []
                customer_id = self.generate_customer_id(worker_id,user_iter)
                for iter in range(ENTRY_PER_CUSTOMER):
                    key,hashtag,value = self.generate_data_for_customer(customer_id,iter)
                    logging.info("Writing key " + hashtag)
                    np_start_time = time.time()
                    self.cluster_client.setHashWithExpire(key,hashtag,value,TTL)
                    keys.append(hashtag)
                    batch +=1
                    if not self.cluster_client.pipeline:
                        resp_time = int((time.time() - np_start_time) * 1000)
                        events.request_success.fire(request_type="Pipeline 1 write only", name="Write Success",
                                                    response_time=resp_time, response_length=512)
                        if os.environ.get('READ_TEST').lower() in ['true','1','t']:
                            np_start_time = time.time()
                            resp = ReadTest.read_batch(keys,self.cluster_client)
                            logging.info("Reading key " + resp)
                            resp_time = int((time.time() - np_start_time) * 1000)
                            keys = []
                            events.request_success.fire(request_type="Pipeline 1 read only", name="Read Success",
                                                        response_time=resp_time, response_length=512)
                    if self.cluster_client.pipeline and batch>=BATCH_SIZE:
                        start_time = time.time()
                        try:
                            logging.info("Executing Write")
                            self.cluster_client.pipeline.execute()
                        except Exception as e:
                            logging.error(str(e))
                        resp_time = int((time.time() - start_time) * 1000)
                        events.request_success.fire(request_type="Pipeline 10k write", name="Write Success",response_time=resp_time, response_length=512)
                        # import pdb;pdb.set_trace()
                        if os.environ.get('READ_TEST').lower() in ('true', '1', 't'):
                            start_time = time.time()
                            resp = ReadTest.read_batch(keys,self.cluster_client)
                            logging.info(resp)
                            resp_time = int((time.time() - start_time) * 1000)
                            events.request_success.fire(request_type="Pipeline 10k read", name="Read Success", response_time=resp_time, response_length=512)
                        batch=0
                        keys = []
                # self.user_id +=1
            if self.cluster_client.pipeline and batch > 0:
                start_time = time.time()
                resp = self.cluster_client.pipeline.execute()
                logging.info(resp)
                resp_time = int((time.time() - start_time) * 1000)
                events.request_success.fire(request_type="Pipeline 10k write", name="Write Success",response_time=resp_time, response_length=512)


    def read_data_using_worker_id(self, worker_id):
        # read only, for bulk only
        batch = 0
        for user_iter in range(TOTAL_CUSTOMERS):
            customer_id = self.generate_customer_id(worker_id, user_iter)
            for iter in range(ENTRY_PER_CUSTOMER):
                key = "{" + customer_id + "}:" + str(iter) + ":" + '_1.0'
                logging.info("Scheduling key " + key)
                self.cluster_client.readHashSingle(key)
                batch += 1
                if batch >= BATCH_SIZE:
                    start_time = time.time()
                    resp = self.cluster_client.pipeline.execute()
                    logging.info(resp)
                    resp_time = int((time.time() - start_time) * 1000)
                    events.request_success.fire(request_type="Pipeline 10k read", name="Read Success",
                                                response_time=resp_time, response_length=512)
                    batch = 0
        # self.user_id +=1

    def write_read_data(self, worker_id = None):
        # for bulk requests
        batch = 0
        keys = []
        for user_iter in range(TOTAL_CUSTOMERS):
            customer_id = self.generate_customer_id(worker_id,user_iter)
            for iter in range(ENTRY_PER_CUSTOMER):
                key, hashtag, value = self.generate_data_for_customer(customer_id, iter)
                self.cluster_client.setHashWithExpire(key, hashtag, value, TTL)
                keys.append(hashtag)
                batch += 1
                if self.cluster_client.pipeline and batch >= BATCH_SIZE:
                    write_start_time = time.time()
                    try:
                        logging.info("Executing Write")
                        self.cluster_client.pipeline.execute()
                        resp_time = int((time.time() - write_start_time) * 1000)
                        events.request_success.fire(request_type="Pipeline bulk write", name="Write Success",
                                                    response_time=resp_time, response_length=512)
                    except Exception as e:
                        logging.error(str(e))
                        resp_time = int((time.time() - write_start_time) * 1000)
                        events.request_failure.fire(request_type="Pipeline bulk write", name="Write Failure",
                                                response_time=resp_time, response_length=512, exception=e)


                        #----------------------------------#
                    read_start_time = time.time()
                    try:
                        ReadTest.read_batch(keys, self.cluster_client)
                        resp_time = int((time.time() - read_start_time) * 1000)
                        events.request_success.fire(request_type="Pipeline bulk read ", name="Read Success",
                                                    response_time=resp_time, response_length=512)
                    except Exception as e:
                        resp_time = int((time.time() - read_start_time) * 1000)
                        events.request_failure.fire(request_type="Pipeline bulk read", name="Read Failure",
                                                    response_time=resp_time, response_length=512, exception=e)
                    keys = []
                    batch = 0

    def write_process_file(self):
        pid = str(os.getpid())
        outputFile = open('{0}.txt'.format(pid), "w")
        outputFile.write(pid)
        outputFile.close()

    def write_data(self,worker_id):
        if self.cluster_client.pipeline:
            self.write_data_pipeline(worker_id)
        else:
            self.write_data_no_pipeline(worker_id)



if __name__== '__main__':
    READ_TEST = os.environ.get('READ_TEST').lower() in ('true', '1', 't')
    WRITE_TEST = os.environ.get('WRITE_TEST').lower() in ('true', '1', 't')
    obj = ExecuteRedisTest()
    obj.write_process_file()
    if WRITE_TEST and READ_TEST:
        obj.write_read_data(worker_id=os.getpid())
    elif WRITE_TEST:
        obj.write_data(worker_id=os.getpid())
    elif READ_TEST:
        argv = sys.argv[0]
        obj.read_data_using_worker_id(worker_id=argv)
    globals.increment()