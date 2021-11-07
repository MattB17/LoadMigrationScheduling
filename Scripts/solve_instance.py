"""Solves an instance of the load migration scheduling problem.

"""
import sys
from MigrationScheduling.Model import Optimizer


if __name__ == "__main__":
    file_path = sys.argv[1]
    optimizer = Optimizer()
    optimizer.get_model_data(file_path)
    lb, ub = optimizer.get_model_bounds()
    optimizer.build_ip_model()
    print("Lower Bound: {}".format(lb))
    print("Upper Bound: {}".format(ub))
