import logging
import os
import subprocess
import time
from pathlib import Path

import numpy

from flask import Flask, jsonify, send_file, request

from app.constant.http.error import SERVER_OK, SERVER_OK_MESSAGE

from config.flask_config import *
from model import create_model, num_classes
from tensorflow import keras


def create_app(test_config=None):
    """
    This function serves as a producer for the server instances
    You can call this function multiple times to produce multiple server instances
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'launcher.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Setup model
    import tensorflow as tf
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

    model = create_model()

    # Load model
    # if os.path.exists(MODEL_SAVE_FILE):
    #     try:
    #         model = keras.models.load_model(MODEL_SAVE_FILE)
    #     except:
    #         logging.warning("Error loading previous model! creating a new one...")
    # else:
    #     logging.info("Previous model not found! creating a new one...")

    model.save(MODEL_SAVE_FILE)
    logging.info("Demo model saved!")

    # a simple page that says hello
    @app.route('/')
    def hello():
        """
        Simple homepage for health check
        """
        return 'Hello, World!'

    @app.route('/get_params')
    def get_params():
        """
        API to get information regarding the scheme used in this server.
        """
        return jsonify({
            'success': True,
            'error_code': SERVER_OK,
            'error_message': SERVER_OK_MESSAGE,
            'result': {
                "scheme": "FL plain"
            }
        })

    @app.route('/get_model')
    def get_model():
        """
        API to get the base model definition in '.h5' format
        """
        return send_file(os.path.join(os.path.dirname(app.root_path), MODEL_SAVE_FILE))

    @app.route('/get_model_weights')
    def get_model_weights():
        """
        API to get the latest model weights
        """
        # for i in model.get_weights():
        #     print(i.shape)
        #     print(i[0])
        # print("weight from layers:")
        # for i in model.layers:
        #     print(i.get_weights())
        res = {
            "weights": [i.tolist() for i in model.get_weights()]
        }
        return jsonify({
            'success': True,
            'error_code': SERVER_OK,
            'error_message': SERVER_OK_MESSAGE,
            'result': res
        })

    @app.route('/update_model_weights', methods=['POST'])
    def update_model_weights():
        """
        API to update the weights of the model based on the aggregated weights
        """
        content = request.json
        weights = content['weights']
        num_party = content['num_party']
        logging.info("Num workers involved = {}".format(num_party))

        for idx, weight in enumerate(model.get_weights()):
            shape = weight.shape
            new_weight = numpy.array(weights[idx], dtype="object")/num_party
            weights[idx] = new_weight

        model.set_weights(weights)
        # evaluate_model()
        return jsonify({
            'success': True,
            'error_code': SERVER_OK,
            'error_message': SERVER_OK_MESSAGE,
            'result': {
            }
        })

    @app.route('/evaluate_model')
    def evaluate_model():
        """
        Used to evaluate the current model performance (accuracy and loss).
        """
        (_, _), (x_test, y_test) = keras.datasets.mnist.load_data()
        # Scale images to the [0, 1] range
        x_test = x_test.astype("float32") / 255
        # Make sure images have shape (28, 28, 1)
        x_test = numpy.expand_dims(x_test, -1)
        logging.info("{} test samples".format(x_test.shape[0]))
        y_test = keras.utils.to_categorical(y_test, num_classes)
        score = model.evaluate(x_test, y_test, verbose=0)
        logging.info("Test loss: {}".format(score[0]))
        logging.info("Test accuracy: {}".format(score[1]))
        res = {
            "loss": score[0],
            "accuracy": score[1],
        }
        return jsonify({
            'success': True,
            'error_code': SERVER_OK,
            'error_message': SERVER_OK_MESSAGE,
            'result': res
        })

    return app
