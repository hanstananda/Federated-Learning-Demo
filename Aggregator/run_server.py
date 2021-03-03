import argparse
import logging
import threading

from gevent.pywsgi import WSGIServer
from gevent import monkey

from app import create_app
from config.flask_config import *

parser = argparse.ArgumentParser(description='Run the aggregator service')
parser.add_argument('--server_ip', dest='server_ip', action='store',
                    help='specify server ip to be used', default=None)
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
    app = create_app(config)
    app_server = WSGIServer((AGGREGATOR_IP, 7200), app)
    app_server.serve_forever()