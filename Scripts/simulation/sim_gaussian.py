"""Simulates load migration scheduling instances having a random number
of migrations chosen uniformly at random within the supplied bounds. The
simulation is done using the `GaussianSimulator` class.

"""
import sys
import random
from MigrationScheduling import analysis, specs, utils, validation
from MigrationScheduling.Sim import GaussianSimulator

utils.initialize_seeds(specs.SEED_NUM)

if __name__ == "__main__":
    output_path = sys.argv[1]
    num_instances = int(sys.argv[2])
    lb = max(specs.MIN_MIGRATIONS, int(sys.argv[3]))
    ub = max(lb, int(sys.argv[4]))
    bottleneck_setting = sys.argv[5].lower()

    validation.validate_bottleneck_setting(bottleneck_setting)
    sim_args = {'bottleneck_type': bottleneck_setting}

    instance_sizes = random.choices(range(lb, ub + 1), k=num_instances)
    analysis.create_simulated_instances(
        GaussianSimulator, sim_args,
        instance_sizes, specs.SMALL_IDX, output_path)
