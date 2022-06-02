from main import ExecuteRedisTest

data_creator = ExecuteRedisTest(via_lua=True)
# currently reading data only not writing data
customer_ids = []
READ_COMMANDS_PER_LUA = 10
for customer_id in customer_ids:
    chunk = 0
    while chunk>=1000:
        readkeys = []
        for iter in range(chunk,1000):
            key,hashtag,value = data_creator.generate_data_for_customer(customer_id,iter)



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