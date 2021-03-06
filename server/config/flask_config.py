"""
All flask configurations shall be put here
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

MODEL_SAVE_FILE = "output/demo_model.h5"
PARAMS_SAVE_FILE = "output/params.txt"
CIPHERTEXT_SAVE_FILE = "cipher.txt"
