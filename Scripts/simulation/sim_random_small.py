"""Simulates load migration scheduling instances having a random number
of migrations below the threshold of the instances that can be solved by
the optimizer.

"""
import os
import sys
import random
from MigrationScheduling import specs
from MigrationScheduling.Data import Simulator

if __name__ == __main__:
    output_path = sys.argv[1]
    num_instances = int(sys.argv[2])
    curr_idx = specs.SMALL_IDX
    instance_sizes = random.choices(
        range(specs.MIN_MIGRATIONS, specs.SMALL_CUTOFF + 1), k=num_instances)
    for instance_size in instance_sizes:
        output_file = os.path.join(
            output_path, "migrations{}.txt".format(curr_idx))
        curr_idx += 1
        simulator.run(instance_size, output_file)
