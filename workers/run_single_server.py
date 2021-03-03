import argparse
import logging
import threading

from gevent.pywsgi import WSGIServer

from app import create_app
from config.flask_config import *

parser = argparse.ArgumentParser(description='Run the aggregator service')
parser.add_argument('--port', dest='worker_port', action='store',
                    help='specify worker port to be used', default=7101)
parser.add_argument('--id', dest='worker_id', action='store',
                    help='specify worker id to be used', default=1)
parser.add_argument('--server_ip', dest='server_ip', action='store',
                    help='specify server ip to be used', default=None)
parser.add_argument('--aggregator_ip', dest='aggregator_ip', action='store',
                    help='specify aggregator ip to be used', default=None)
parser.add_argument('--is_docker', default=False, action='store_true',
                    help='specify whether docker IPs should be used')
parser.add_argument('--is_prod', default=False, action='store_true',
                    help='specify whether production environment is used, implying the use of .env')

results = parser.parse_args()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if results.is_docker:
        config = DockerConfig
    elif results.is_prod:
        config = ProdConfig
    else:
        config = DefaultConfig

    if results.server_ip is not None:
        config.SERVER_IP = results.server_ip

    if results.aggregator_ip is not None:
        config.AGGREGATOR_IP = results.aggregator_ip

    app = create_app(worker_id=int(results.worker_id), config_object=config)
    app_server = WSGIServer((WORKER_IP, int(results.worker_port)), app)
    app_server.serve_forever()
