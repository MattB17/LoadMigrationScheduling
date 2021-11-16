"""Solves an instance of the load migration scheduling problem.

"""
import sys
from MigrationScheduling import algorithms
from MigrationScheduling.Model import Optimizer


if __name__ == "__main__":
    file_path = sys.argv[1]
    optimizer = Optimizer()
    optimizer.get_model_data(file_path)
    lb, ub = optimizer.get_model_bounds()
    optimizer.build_ip_model()
    print("Number of Rounds for Vector First Fit: {}".format(
        algorithms.vector_first_fit(optimizer.instance_data())))
    print("Number of Rounds for Current Bottleneck First: {}".format(
        algorithms.current_bottleneck_first(optimizer.instance_data())))
    print("Lower Bound: {}".format(lb))
    print("Upper Bound: {}".format(ub))
