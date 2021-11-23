"""Simulates load migration scheduling instances having a random number
of migrations below the threshold of the instances that can be solved by
the optimizer.

"""
import sys
import random
from MigrationScheduling import analysis, specs, utils

utils.initialize_seeds(specs.SEED_NUM)

if __name__ == "__main__":
    output_path = sys.argv[1]
    num_instances = int(sys.argv[2])
    lb = max(specs.MIN_MIGRATIONS, int(sys.argv[3]))
    ub = max(lb, int(sys.argv[4]))
    instance_sizes = random.choices(range(lb, ub + 1), k=num_instances)
    analysis.create_simulated_instances(
        instance_sizes, specs.SMALL_IDX, output_path)
