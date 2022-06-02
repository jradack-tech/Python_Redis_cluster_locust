# Quick start

1. Run ./locust_master.sh to start the master locust
2. Run ./locust_worker.sh 1 <MASTER IP ADDRESS> to start one worker and connect to the locust master  
3. Export AWS STS creds (MASTER and WORKER)
4. Open <MASTER IP ADDRESS>:8089
5. Run performance test with your conf parameters, for example, the number of users and spawn rate, set the host to http://localhost 



Run in master:
chmod +x locust_master.sh
 ./locust_master.sh
Open http://localhost:8089

Port FW:
ssh -i MyKey-Oregon.pem -N -L 8089:<master private IP>:8089 <master public domain name>
ssh -i "us-east-1.pem" -N -L 8089:10.0.1.137:8089 ec2-user@ec2-3-80-196-106.compute-1.amazonaws.com


Run in worker:
chmod +x locust_worker.sh
./locust_worker.sh 1 <MASTER EC2 private IP ADDRESS>
./locust_worker.sh 1 10.0.1.137
./locust_worker.sh 3 10.0.1.137

./locust_worker.sh 30 10.0.1.137

./locust -f locustfile.py --worker --master-host=10.0.1.137

locust -f /home/ec2-user/locustfiles/redis-code/locustfile.py --worker --master-host=10.0.1.137


Open http://localhost:8089

user: 100 users per worker (random values)


UI config:
2

host: http://localhost


kill -9 `pgrep -f locust`


redis-cli -h clustercfg.new-db-r6g-xlarge-tls.g4qo13.memorydb.us-east-1.amazonaws.com -p 6379  -c  --user memdbroot1 --pass memdbroot1234567890 --tls


redis-cli -h clustercfg.new-db-r6g-xslarge-tls.g4qo13.memorydb.us-east-1.amazonaws.com  -p 6379  -c  --user memdbroot1 --pass memdbroot1234567890 --tls

redis-cli -h clustercfg.new-db-r6g-xlarge-tls-4.g4qo13.memorydb.us-east-1.amazonaws.com  -p 6379 -c  --tls --user memdbroot1 --pass  memdbroot1234567890



 source redis-code/locust-memdb/bin/activate


 Steps:
1: Scp to desited path "<path/to/folder>"
2: Unzip folder (say the name = "redis-code")
3: cd redis-code
4: rm -rf venv

## Install virtual env
# Make sure python 3.7 or python 3.8
## make sure you are inside "redis-code" folder
1: pip3 install virtualenv
2: virtualenv venv
3: source venv/bin/activate
4: pip install -r requirements.txt


Master command: locust --master
Worker command: locust --worker

screen -r worker -d

bash start.sh



ssh -i "us-east-1.pem" ec2-user@ec2-54-210-141-246.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-54-210-120-168.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-3-84-142-52.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-174-129-87-28.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-52-202-138-163.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-54-167-218-147.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-54-161-99-94.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-18-232-154-151.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-35-175-227-78.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-54-145-110-196.compute-1.amazonaws.com



IType:
ssh -i "us-east-1.pem" ec2-user@ec2-54-166-243-165.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-54-167-213-123.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-18-232-103-96.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-54-242-109-202.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-54-152-221-245.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-54-204-178-33.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-52-91-47-22.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-54-162-223-135.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-34-239-183-215.compute-1.amazonaws.com
ssh -i "us-east-1.pem" ec2-user@ec2-54-224-113-65.compute-1.amazonaws.com


scp -i /Users/injavija/Documents/desktop/work/AWS-env/us-east-1.pem  -r /Users/injavija/Desktop/redis-archive/rediscode  ec2-user@ec2-3-80-196-106.compute-1.amazonaws.com:/tmp 
echo "--------------------------------------Done-----------------------------------------"
scp -i /Users/injavija/Documents/desktop/work/AWS-env/us-east-1.pem  -r /Users/injavija/Desktop/redis-archive/rediscode  ec2-user@ec2-54-167-213-123.compute-1.amazonaws.com:/tmp
echo "--------------------------------------Done-----------------------------------------"
scp -i /Users/injavija/Documents/desktop/work/AWS-env/us-east-1.pem  -r /Users/injavija/Desktop/redis-archive/rediscode  ec2-user@ec2-54-87-49-195.compute-1.amazonaws.com:/tmp
echo "--------------------------------------Done-----------------------------------------"
scp -i /Users/injavija/Documents/desktop/work/AWS-env/us-east-1.pem  -r /Users/injavija/Desktop/redis-archive/rediscode  ec2-user@ec2-54-210-141-246.compute-1.amazonaws.com:/tmp 
echo "--------------------------------------Done-----------------------------------------"
scp -i /Users/injavija/Documents/desktop/work/AWS-env/us-east-1.pem  -r /Users/injavija/Desktop/redis-archive/rediscode  eec2-user@ec2-54-210-120-168.compute-1.amazonaws.com:/tmp
echo "--------------------------------------Done-----------------------------------------"
scp -i /Users/injavija/Documents/desktop/work/AWS-env/us-east-1.pem  -r /Users/injavija/Desktop/redis-archive/rediscode  ec2-user@ec2-3-84-142-52.compute-1.amazonaws.com:/tmp
echo "--------------------------------------Done-----------------------------------------"
scp -i /Users/injavija/Documents/desktop/work/AWS-env/us-east-1.pem  -r /Users/injavija/Desktop/redis-archive/rediscode  ec2-user@ec2-174-129-87-28.compute-1.amazonaws.com:/tmp 
echo "--------------------------------------Done-----------------------------------------"
scp -i /Users/injavija/Documents/desktop/work/AWS-env/us-east-1.pem  -r /Users/injavija/Desktop/redis-archive/rediscode  ec2-user@ec2-54-167-218-147.compute-1.amazonaws.com:/tmp
echo "--------------------------------------Done-----------------------------------------"
scp -i /Users/injavija/Documents/desktop/work/AWS-env/us-east-1.pem  -r /Users/injavija/Desktop/redis-archive/rediscode  ec2-user@ec2-54-161-99-94.compute-1.amazonaws.com:/tmp
echo "------------------------------listeners.py--------Done-----------------------------------------"
scp -i /Users/injavija/Documents/desktop/work/AWS-env/us-east-1.pem  -r /Users/injavija/Desktop/redis-archive/rediscode  ec2-user@ec2-18-232-154-151.compute-1.amazonaws.com:/tmp 
echo "--------------------------------------Done-----------------------------------------"
scp -i /Users/injavija/Documents/desktop/work/AWS-env/us-east-1.pem  -r /Users/injavija/Desktop/redis-archive/rediscode  ec2-user@ec2-35-175-227-78.compute-1.amazonaws.com:/tmp
echo "--------------------------------------Done-----------------------------------------"
scp -i /Users/injavija/Documents/desktop/work/AWS-env/us-east-1.pem  -r /Users/injavija/Desktop/redis-archive/rediscode  ec2-user@ec2-54-145-110-196.compute-1.amazonaws.com:/tmp
echo "--------------------------------------Done-----------------------------------------"


scp -i /Users/injavija/Documents/desktop/work/AWS-env/us-east-1.pem  -r ec2-user@ec2-54-145-110-196.compute-1.amazonaws.com:/tmp/py_move Users/injavija/Desktop/

auth memdbroot1 memdbroot1234567890



rm README.MD && rm locust_worker.sh  && rm  redisHandler.py  && rm  SCP-script.sh  && \\
rm  locustfile.py  && rm  requirements.txt rm   && listeners.py rm   && lualocust.py  && rm test.lua  && \\
rm listeners.py  && rm lualocust.py  && rm locust_master.sh  && rm main.py



Error:
[ec2-user@ip-10-0-1-26 ~]$ redis-cli -h clustercfg.new-db-r6g-xlarge-tls.g4qo13.memorydb.us-east-1.amazonaws.com -p 6379  -c  --user memdbroot1 --pass memdbroot1234567890 --tls
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
clustercfg.new-db-r6g-xlarge-tls.g4qo13.memorydb.us-east-1.amazonaws.com:6379> DBSIZE
(integer) 76330402
clustercfg.new-db-r6g-xlarge-tls.g4qo13.memorydb.us-east-1.amazonaws.com:6379> FLUSHALL
(error) ERR CLUSTERDOWN The cluster is down and only accepts read commands
clustercfg.new-db-r6g-xlarge-tls.g4qo13.memorydb.us-east-1.amazonaws.com:6379>

clustercfg.new-db-r6g-xlarge-tls.g4qo13.memorydb.us-east-1.amazonaws.com:6379> dbsize
(error) LOADING Redis is loading the dataset in memory

[ec2-user@ip-10-0-1-26 ~]$ redis-cli -h clustercfg.new-db-r6g-xlarge-tls.g4qo13.memorydb.us-east-1.amazonaws.com -p 6379    --user memdbroot1 --pass memdbroot1234567890 --tls
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
clustercfg.new-db-r6g-xlarge-tls.g4qo13.memorydb.us-east-1.amazonaws.com:6379> dbsize
(error) LOADING Redis is loading the dataset in memory
clustercfg.new-db-r6g-xlarge-tls.g4qo13.memorydb.us-east-1.amazonaws.com:6379> dbsize
(error) LOADING Redis is loading the dataset in memory
clustercfg.new-db-r6g-xlarge-tls.g4qo13.memorydb.us-east-1.amazonaws.com:6379>
clustercfg.new-db-r6g-xlarge-tls.g4qo13.memorydb.us-east-1.amazonaws.com:6379> dbsize
(error) LOADING Redis is loading the dataset in memory
clustercfg.new-db-r6g-xlarge-tls.g4qo13.memorydb.us-east-1.amazonaws.com:6379> FLUSHALL
(error) ERR CLUSTERDOWN The cluster is down and only accepts read commands
clustercfg.new-db-r6g-xlarge-tls.g4qo13.memorydb.us-east-1.amazonaws.com:6379>







Tests:

Reds:
screen -r worker -d
vi .env --> read_test=true | write_test=false
python main.py 103308


Write:
screen -S worker
screen -r worker -d
bash start.sh
vi .env --> read_test=falase | write_test=true
