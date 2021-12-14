"""Simulates a single load migration scheduling instance using the
`GaussianSimulator`.

"""
import sys
import random
from MigrationScheduling import analysis, specs, utils, validation
from MigrationScheduling.Sim import GaussianSimulator


utils.initialize_seeds(specs.SEED_NUM)


if __name__ == "__main__":
    output_file = sys.argv[1]
    num_migrations = int(sys.argv[2])
    bottleneck_setting = sys.argv[3].lower()

    validation.validate_bottleneck_setting(bottleneck_setting)

    simulator = GaussianSimulator(bottleneck_setting)
    simulator.run(num_migrations, output_file)
