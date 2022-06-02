import logging, os

from rediscluster import RedisCluster


logging.basicConfig()
logger = logging.getLogger('rediscluster')
logger.setLevel(logging.DEBUG)
logger.propagate = True



class RedisHandler():
    def __init__(self,pipeline=False,password=None):
        startup_nodes = [{"host": os.environ.get('HOST'), "port": os.environ.get('PORT')}]
        username = os.environ.get("USERNAME")
        self.rc = RedisCluster(username=username, ssl=os.environ.get('SSL').lower() in ('true', '1', 't'), startup_nodes=startup_nodes,
                               decode_responses=True, skip_full_coverage_check=True, password=password )
        self.pipeline = None
        if(pipeline):
            self.pipeline = self.rc.pipeline()
            self.rc.cluster_delslots()

    def setHash(self,key,hashtag,value):
        if self.pipeline:
            self.pipeline.hset(hashtag,key=None,value=None,mapping=value)
        else:
            self.rc.hset(hashtag,key=None,value=None,mapping=value)

    def expire(self,key,time):
        if self.pipeline:
            self.pipeline.expire(key,time)
        else:
            self.rc.expire(key,time)

    def setHashWithExpire(self,key,hashtag,value,ttl):
        self.setHash(key,hashtag,value)
        self.expire(hashtag,ttl)

    def readHashSingle(self,key):
        if self.pipeline:
            return self.pipeline.hgetall(key)
        else:
            return self.rc.hgetall(key)

    def evalsha(self,sha,number,keys_args):
        return self.rc.evalsha(sha,number,keys_args)

    def __del__(self):
        del self.rc
        if self.pipeline:
            del self.pipeline


