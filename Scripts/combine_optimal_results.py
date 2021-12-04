"""Combines the optimal results from all files located in the input
directory. Each file stores the results for one instance.

"""
import os
import sys
from MigrationScheduling import analysis, utils


if __name__ == "__main__":
    input_dir = sys.argv[1]
    file_pattern = sys.argv[2]
    output_dir = sys.argv[3]

    result_files = utils.get_all_files_by_pattern(input_dir, file_pattern)
    output_file = os.path.join(output_dir, "results.txt")

    analysis.combine_optimal_results_files(
        input_dir, result_files, output_file)
