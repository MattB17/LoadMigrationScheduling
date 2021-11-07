"""Simulates load migration scheduling instances.

"""
import os
import sys
from MigrationScheduling.Data import Simulator

NUM_MIGRATIONS_LIST = [5, 10, 20, 50, 100, 500, 1000, 5000, 10000]
FILE_IDX = 1

if __name__ == "__main__":
    output_path = sys.argv[1]
    simulator = Simulator()
    curr_idx = FILE_IDX
    for num_migrations in NUM_MIGRATIONS_LIST:
        simulator.run(
            num_migrations,
            os.path.join(output_path, "migrations{}.txt".format(curr_idx)))
        curr_idx += 1
