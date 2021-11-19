"""Simulates load migration scheduling instances having a random number
of migrations below the threshold of the instances that can be solved by
the optimizer.

"""
import os
import sys
import random
import numpy as np
from MigrationScheduling import specs, utils
from MigrationScheduling.Data import Simulator

utils.initialize_seeds()

if __name__ == "__main__":
    output_path = sys.argv[1]
    num_instances = int(sys.argv[2])
    lb = max(specs.MIN_MIGRATIONS, int(sys.argv[3]))
    ub = max(lb, int(sys.argv[4]))
    curr_idx = specs.SMALL_IDX
    simulator = Simulator()
    instance_sizes = random.choices(range(lb, ub + 1), k=num_instances)
    for instance_size in instance_sizes:
        output_file = os.path.join(
            output_path, "migrations{}.txt".format(curr_idx))
        curr_idx += 1
        simulator.run(instance_size, output_file)
