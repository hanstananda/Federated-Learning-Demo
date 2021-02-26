"""
All flask configurations shall be put here
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

AGGREGATOR_IP = "0.0.0.0"
PARAMS_FILE_ENDPOINT = "/get_saved_params"
PARAMS_JSON_ENDPOINT = "/get_params"
UPDATE_MODEL_ENDPOINT = "/update_model_weights"


class DefaultConfig:
    """Base config."""
    SERVER_IP = "http://localhost:7000"


class DockerConfig(DefaultConfig):
    SERVER_IP = "http://he-ew-demo-server:7000"
