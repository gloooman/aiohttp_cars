import motor.motor_asyncio as aiomotor
import yaml
from trafaret import extract_error


def load_config(f_name):
    with open(f_name, 'rt') as f:
        data = yaml.load(f)
    return data


async def init_mongo(conf, loop):
    conf['host'] = '127.0.0.1'
    mongo_uri = "mongodb://{}:{}".format(conf['host'], conf['port'])
    conn = aiomotor.AsyncIOMotorClient(
        mongo_uri,
        maxPoolSize=conf['max_pool_size'],
        io_loop=loop
    )
    db_name = conf['database']
    return conn[db_name]


def check_input_form(model, form):
    errors = extract_error(model, form)
    del errors['_id']
    return errors
