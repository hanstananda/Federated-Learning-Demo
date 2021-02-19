import time

import numpy


class Aggregator:

    def __init__(self):
        self._weights = []

    @staticmethod
    def get_param_info():
        res = {
            "scheme": "FL plain"
        }
        return res

    def save_weight(self, weights):
        self._weights.append(weights)

    def aggregate_weights(self):
        start_time = time.perf_counter()
        num_party = len(self._weights)
        if num_party == 0:
            time_elapsed = time.perf_counter() - start_time
            return {
                "weights": None,
                "num_party": num_party,
                "aggregation_time": time_elapsed.__str__(),
            }
        agg_weights = [numpy.asarray(i) for i in self._weights[0]]

        for i in range(1, num_party):
            for j in range(len(agg_weights)):
                agg_weights[j] += numpy.asarray(self._weights[i][j])

        time_elapsed = time.perf_counter() - start_time

        del self._weights[:num_party]

        return {
            "weights": [i.tolist() for i in agg_weights],
            "num_party": num_party,
            "aggregation_time": time_elapsed,
        }
