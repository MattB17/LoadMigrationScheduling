"""Solve all load migration scheduling instances in a specified directory
and write the results to a file.

"""
import os
import sys
import random
import numpy as np
from MigrationScheduling.Model import Optimizer
from MigrationScheduling import algorithms, analysis, specs, utils


utils.initialize_seeds(specs.SEED_NUM)


if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    file_pattern = sys.argv[3]
    resiliency = (sys.argv[4].lower() == "true")
    optimize = (sys.argv[5].lower() == "true")
    instance_files = utils.get_all_files_by_pattern(input_dir, file_pattern)
    output_file = os.path.join(output_dir, "results.txt")
    if optimize:
        analysis.calculate_optimal_results_for_instances(
            input_dir, file_pattern, instance_files, output_dir, resiliency)
    else:
        output_file = os.path.join(output_dir, "results.txt")
        analysis.calculate_heuristic_results_for_instances(
            input_dir, file_pattern, instance_files, output_file, resiliency)
