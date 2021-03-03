"""
All flask configurations shall be put here
"""

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
WORKER_IP = "0.0.0.0"

PARAMS_FILE_ENDPOINT = "/get_saved_params"
PARAMS_JSON_ENDPOINT = "/get_params"
SERVER_MODEL_ENDPOINT = "/get_model"
SERVER_WEIGHT_ENDPOINT = "/get_model_weights"
SAVE_WEIGHT_MATRIX_ENDPOINT = "/save_weights"
PARAMS_SAVE_FILE = "params.txt"
MODEL_SAVE_FILE = "model.h5"


class DefaultConfig:
    """Base config."""
    SERVER_IP = "http://localhost:7000"
    AGGREGATOR_IP = "http://localhost:7200"


class DockerConfig(DefaultConfig):
    """
    Config for docker
    """
    SERVER_IP = "http://fl-demo-server:7000"
    AGGREGATOR_IP = "http://fl-demo-aggregator-service:7200"


class ProdConfig(DefaultConfig):
    """
    Config for production using .env
    """
    load_dotenv()
    SERVER_IP = os.getenv("SERVER_IP")
    AGGREGATOR_IP = "AGGREGATOR_IP"
