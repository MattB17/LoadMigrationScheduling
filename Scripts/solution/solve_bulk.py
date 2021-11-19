"""Solve all load migration scheduling instances in a specified directory
and write the results to a file.

"""
import os
import sys
import random
import numpy as np
from MigrationScheduling.Model import Optimizer
from MigrationScheduling import algorithms, specs, utils


utils.initialize_seeds()


if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    file_pattern = sys.argv[3]
    optimize = (sys.argv[4].lower() == "true")
    instance_files = utils.get_all_files_by_pattern(input_dir, file_pattern)
    output_file = os.path.join(output_dir, "results.txt")
    with open(output_file, 'w') as result_file:
        result_file.write(utils.get_results_header(optimize))
        for instance_file in instance_files:
            optimizer = Optimizer()
            optimizer.get_model_data(os.path.join(input_dir, instance_file))
            vff = algorithms.vector_first_fit(optimizer.instance_data())
            cbf = algorithms.current_bottleneck_first(
                optimizer.instance_data(), specs.CBF_CHOICES)
            instance_str = "{0} {1} {2}".format(
                optimizer.get_size_string(), vff, cbf)
            if optimize:
                instance_str += " {}".format(
                    int(optimizer.build_ip_model(verbose=False) + 1))
            result_file.write(instance_str + "\n")
