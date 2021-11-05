"""Solves an instance of the load migration scheduling problem.

"""
import sys
from MigrationScheduling.Model import Optimizer


if __name__ == "__main__":
    file_path = sys.argv[1]
    optimizer = Optimizer()
    optimizer.get_model_data(file_path)
    print("Solving IP instance")
    print("-------------------")
    optimizer.build_ip_model()
    print()
    print("Solving LP instance")
    print("-------------------")
    optimizer.build_lp_model()
