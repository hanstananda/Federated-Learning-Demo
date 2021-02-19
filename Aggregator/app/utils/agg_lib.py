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
        agg_weights = numpy.array(self._weights[0], dtype="object")

        for i in range(1, num_party):
            agg_weights += numpy.array(self._weights[i], dtype="object")

        time_elapsed = time.perf_counter() - start_time

        del self._weights[:num_party]

        return {
            "weights": agg_weights.tolist(),
            "num_party": num_party,
            "aggregation_time": time_elapsed,
        }
