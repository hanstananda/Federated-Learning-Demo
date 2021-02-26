import logging

import keras
import numpy as np


class LoaderMNIST:
    """
    This is a custom Data Loader that is used to partition the keras pre-build dataset and
    give the correct data partition to the specific worker part.
    In practice, this class should be exchanged with specific folder loader for each instance.
    """

    def __init__(self, num_partition: int):
        """
        Load dataset and initialize based on the number of partitions specified
        """
        (x_train, y_train), (_, _) = keras.datasets.mnist.load_data()
        logging.info(f"Total Dataset size={x_train.shape}")
        self.x_partition = np.array_split(x_train, num_partition)
        self.y_partition = np.array_split(y_train, num_partition)

    def get_train_data_partitions(self, idx):
        return self.x_partition[idx-1], self.y_partition[idx-1]
