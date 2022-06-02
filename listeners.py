from locust import events
from locust.runners import MasterRunner, WorkerRunner
import globals,os

# Fired when the worker recieves a message of type 'test_users'
def setup_test_users(environment, msg, **kwargs):
    os.environ['WORKER_ID'] = globals.WORKER_COUNT
    print("SETTING WORKER COUNT {0}".format(str(globals.WORKER_COUNT)))
    environment.runner.send_message('acknowledge_users', f"Thanks for the {len(msg.data)} users!")

# Fired when the master recieves a message of type 'acknowledge_users'
def on_acknowledge(msg, **kwargs):
    print("#### MASTER INC WORKER_COUNT")
    globals.WORKER_COUNT +=1
    print(globals.WORKER_COUNT)

@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    if not isinstance(environment.runner, MasterRunner):
        environment.runner.register_message('test_users', setup_test_users)
    if not isinstance(environment.runner, WorkerRunner):
        environment.runner.register_message('acknowledge_users', on_acknowledge)

@events.test_start.add_listener
def on_test_start(environment, **_kwargs):
    if not isinstance(environment.runner, MasterRunner):
        environment.runner.send_message('test_users', globals.WORKER_COUNT)