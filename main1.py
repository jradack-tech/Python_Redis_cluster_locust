import os, sys
import random
import time
import uuid
from base64 import b64encode
from redisHandler import RedisHandler
import pickle
from dotenv import load_dotenv
import globals
from locust import events

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
        # print(self.user_id)
        entity_id = '{0:07}'.format(user_id)
        # entity_id = str(uuid.uuid1())
        # entity_names = ['A_', 'C_']
        entity_name = 'A_'#random.choice(entity_names)
        customer_id = str(worker_id) +'_'+entity_name + entity_id
        return customer_id

    def generate_data(self,is_bulk=None,worker_id=None):
        if is_bulk:
            batch = 0
            for user_iter in range(TOTAL_CUSTOMERS):
                keys = []
                customer_id = self.generate_customer_id(worker_id,user_iter)
                for iter in range(ENTRY_PER_CUSTOMER):
                    key,hashtag,value = self.generate_data_for_customer(customer_id,iter)
                    # print("Writing key " + hashtag)
                    self.cluster_client.setHashWithExpire(key,hashtag,value,TTL)
                    keys.append(hashtag)
                    batch +=1
                    if self.cluster_client.pipeline and batch>=BATCH_SIZE:
                        start_time = time.time()
                        try:
                            print("Executing Write")
                            self.cluster_client.pipeline.execute()
                        except Exception as e:
                            print(str(e))
                        resp_time = int((time.time() - start_time) * 1000)
                        events.request_success.fire(request_type="Pipeline 10k write", name="Write Success",response_time=resp_time, response_length=512)
                        if os.environ.get('READ_TEST').lower() in ('true', '1', 't'):
                            start_time = time.time()
                            self.read_batch(keys)
                            resp_time = int((time.time() - start_time) * 1000)
                            events.request_success.fire(request_type="Pipeline 10k read", name="Read Success",
                                                        response_time=resp_time, response_length=512)
                        keys = []
                        batch=0
                # self.user_id +=1
            if self.cluster_client.pipeline and batch > 0:
                start_time = time.time()
                self.cluster_client.pipeline.execute()
                resp_time = int((time.time() - start_time) * 1000)
                events.request_success.fire(request_type="Pipeline 10k write", name="Write Success",response_time=resp_time, response_length=512)

    def read_data(self,key):
        # print(key)


        if self.cluster_client.pipeline:
            self.cluster_client.readHashSingle(key)


            return self.cluster_client.pipeline.execute()
        else:
            return self.cluster_client.readHashSingle(key)




    def read_data_bulk(self,key):
        if self.cluster_client.pipeline:
            batch = 0
            for iter in range(ENTRY_PER_CUSTOMER):
                key = key.split('}:')[0]+'}:'+str(iter) + ':_1.0'
                #print("Scheduling key "+key)
                self.cluster_client.readHashSingle(key)
                batch += 1
                if batch>=BATCH_SIZE:
                    self.cluster_client.pipeline.execute()
            return
        else:
            for iter in range(ENTRY_PER_CUSTOMER):
                key = key.split('}:')[0]+'}:'+str(iter) + ':_1.0'
                print("Firing for key " + key)
                return self.cluster_client.readHashSingle(key)




    # def read_data_from_keys(self,is_bulk=None,worker_id=None):
    #     if is_bulk:
    #         response = self.read_data_bulk(worker_id)
    #     else:
    #         # key = "{"+self.hashtag+"}:"+str(self.iter)+":_1.0"
    #         response =  self.read_data(worker_id)
    #     print(response)
    #     return response

    def read_data_using_worker_id(self, worker_id):
        batch = 0
        for user_iter in range(TOTAL_CUSTOMERS):
            customer_id = self.generate_customer_id(worker_id, user_iter)
            for iter in range(ENTRY_PER_CUSTOMER):
                key = "{" + customer_id + "}:" + str(iter) + ":" + '_1.0'
                # print("Scheduling key " + key)
                self.cluster_client.readHashSingle(key)
                batch += 1
                if batch >= BATCH_SIZE:
                    start_time = time.time()
                    resp = self.cluster_client.pipeline.execute()
                    # print(resp)
                    resp_time = int((time.time() - start_time) * 1000)
                    events.request_success.fire(request_type="Pipeline 10k read", name="Read Success",
                                                response_time=resp_time, response_length=512)
                    batch = 0
        # self.user_id +=1

    def read_write_together(self, is_bulk = True, worker_id = None):
        ## WRITE STEP
        batch = 0
        keys = []
        for user_iter in range(TOTAL_CUSTOMERS):
            customer_id = self.generate_customer_id(worker_id,user_iter)
            for iter in range(ENTRY_PER_CUSTOMER):
                key, hashtag, value = self.generate_data_for_customer(customer_id, iter)
                # print("Writing key " + hashtag)
                self.cluster_client.setHashWithExpire(key, hashtag, value, TTL)
                keys.append(hashtag)
                batch += 1
                if self.cluster_client.pipeline and batch >= BATCH_SIZE:
                    start_time = time.time()
                    try:
                        print("Executing Write")
                        self.cluster_client.pipeline.execute()
                        self.read_batch(keys)
                        keys = []
                    except Exception as e:
                        print(str(e))
                    resp_time = int((time.time() - start_time) * 1000)
                    # events.request_success.fire(request_type="Pipeline 10k write", name="Write Success",
                    #                             response_time=resp_time, response_length=512)
                    batch = 0

    def read_batch(self,keys):
        for key in keys:
            self.cluster_client.readHashSingle(key)
            print("Executing READ")
            return self.cluster_client.pipeline.execute()

    def write_process_file(self):
        pid = str(os.getpid())
        outputFile = open('{0}.txt'.format(pid), "w")
        outputFile.write(pid)
        outputFile.close()

if __name__== '__main__':

    READ_TEST = os.environ.get('READ_TEST').lower() in ('true', '1', 't')
    WRITE_TEST = os.environ.get('WRITE_TEST').lower() in ('true', '1', 't')
    obj = ExecuteRedisTest()
    obj.write_process_file()
    if WRITE_TEST and READ_TEST:
        obj.read_write_together(is_bulk=True,worker_id=os.getpid())
    elif WRITE_TEST:
        obj.generate_data(is_bulk=True,worker_id=os.getpid())
    elif READ_TEST:
        argv = sys.argv[0]
        obj.read_data_using_worker_id(worker_id=argv)
        obj.read_data_using_worker_id(worker_id=os.getpid())
    globals.increment()