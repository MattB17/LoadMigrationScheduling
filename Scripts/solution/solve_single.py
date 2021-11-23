"""Solves an instance of the load migration scheduling problem.

"""
import sys
import random
import numpy as np
from MigrationScheduling import algorithms, specs, utils
from MigrationScheduling.Model import Optimizer


utils.initialize_seeds(specs.SEED_NUM)


if __name__ == "__main__":
    file_path = sys.argv[1]
    run_optimizer = (sys.argv[2].lower() == "true")
    optimizer = Optimizer()
    optimizer.get_model_data(file_path)
    if run_optimizer:
        lb, ub = optimizer.get_model_bounds()
        print("Lower Bound: {}".format(lb))
        print("Upper Bound: {}".format(ub))
        optimizer.build_ip_model(verbose=True)

    print("Number of Rounds for Vector First Fit: {}".format(
        algorithms.vector_first_fit(optimizer.instance_data())))
    print("Number of Rounds for Current Bottleneck First: {}".format(
        algorithms.current_bottleneck_first(
            optimizer.instance_data(), specs.CBF_CHOICES)))
