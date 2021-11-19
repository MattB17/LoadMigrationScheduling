"""Solve all load migration scheduling instances in a specified directory
and write the results to a file.

"""
import re
import os
import sys
import random
import numpy as np
from MigrationScheduling import specs
from MigrationScheduling import algorithms
from MigrationScheduling.Model import Optimizer


random.seed(42)
np.random.seed(42)


if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    file_pattern = sys.argv[3]
    optimize = (sys.argv[4].lower() == "true")
    match_str = r"{}.*\.txt".format(file_pattern)
    instance_files = [file_name for file_name in os.listdir(input_dir)
                      if re.match(match_str, file_name)]
    output_file = os.path.join(output_dir, "results.txt")
    with open(output_file, 'w') as result_file:
        header_str = "num_migrations num_controllers num_groups vff cbf"
        if optimize:
            header_str += " opt"
        result_file.write(header_str + "\n")
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
