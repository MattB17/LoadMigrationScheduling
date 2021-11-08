"""Simulates load migration scheduling instances.

"""
import os
import sys
from MigrationScheduling import specs
from MigrationScheduling.Data import Simulator

NUM_MIGRATIONS_LIST = [5, 10, 20, 50, 100, 250, 500, 1000, 5000, 10000]

if __name__ == "__main__":
    output_path = sys.argv[1]
    simulator = Simulator()
    curr_idx_small = specs.SMALL_IDX
    curr_idx_large = specs.LARGE_IDX
    for num_migrations in NUM_MIGRATIONS_LIST:
        if num_migrations <= specs.SMALL_CUTOFF:
            output_file = os.path.join(
                output_path, "migrations{}.txt".format(curr_idx_small))
            curr_idx_small += 1
        else:
            output_file = os.path.join(
                output_path, "migrations_large{}.txt".format(curr_idx_large))
            curr_idx_large += 1
        simulator.run(num_migrations, output_file)
