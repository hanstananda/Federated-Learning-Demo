"""
Demo script to use the federated training system
"""

from datetime import datetime

import requests
import pandas as pd

WORKER1_HOST = "http://localhost:7101/"
WORKER2_HOST = "http://localhost:7102/"
AGGREGATOR_HOST = "http://localhost:7200/"
SERVER_HOST = "http://localhost:7000/"
WORKER_TRAIN_ENDPOINT = "train"
AGGREGATOR_ENDPOINT = "agg_val"
SERVER_EVALUATE_ENDPOINT = "evaluate_model"

aggregation_time = []
test_accuracy = []
test_loss = []

for i in range(20):
    print(f"Epoch {i+1} starting")

    resp_worker1 = requests.get(WORKER1_HOST + WORKER_TRAIN_ENDPOINT)
    resp_worker1_json = resp_worker1.json()

    resp_worker2 = requests.get(WORKER2_HOST + WORKER_TRAIN_ENDPOINT)
    resp_worker2_json = resp_worker2.json()

    resp_aggregator = requests.get(AGGREGATOR_HOST + AGGREGATOR_ENDPOINT)
    resp_aggregator_json = resp_aggregator.json()
    aggregation_time.append(resp_aggregator_json['result']['aggregation_time'])

    resp_server = requests.get(SERVER_HOST + SERVER_EVALUATE_ENDPOINT)
    resp_server_json = resp_server.json()
    test_accuracy.append(resp_server_json['result']['accuracy'])
    test_loss.append(resp_server_json['result']['loss'])
    print(f"End of epoch {i+1}")


df = pd.DataFrame(data={
    'aggregation time': aggregation_time,
    'test loss': test_loss,
    'test accuracy': test_accuracy,
})
df.index += 1

dt_string = datetime.now().replace(microsecond=0).strftime("%Y-%m-%d_%H-%M-%S")

df.to_csv(f'test_results_plain_fl_{dt_string}.csv', index_label="Epochs")
