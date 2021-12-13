"""The GaussianSimulator class is used to simulate load migration
scheduling instances using the Gaussian distribution.

"""
import random
import numpy as np
from MigrationScheduling import utils
from MigrationScheduling.Data import Migration
from MigrationScheduling.Sim.Simulator import Simulator

class GaussianSimulator(Simulator):
    """Used to simulate a load migration scheduling instance.

    Parameters
    ----------
    bottleneck_type: str
        A string representing the bottleneck setting used to generate the
        capacities for the constraints in the simulated instance. Accepted
        values are 'high', 'medium', and 'low'. The capacity of the
        constraints are then calculated using this setting and the individual
        load on the constraint.

    Attributes
    ----------
    _bottleneck_type: str
        Represents the bottleneck setting used to generate the capacity of
        constraints for the simulated instance.
    _migrations: list
        A list of `Migration` objects specifying the simulated migrations.
    _num_migrations: int
        An integer representing the number of migrations.
    _controllers: list
        A list of two element tuples specifying the simulated controllers.
        The first element is an integer representing the number of migrations
        with this controller as destination and the second is a float
        representing the maximum load incurred for a migration to this
        controller.
    _num_controllers: int
        An integer representing the number of controllers.
    _qos_groups: list
        A list of integers representing the number of migrations belonging
        to each QoS group.
    _num_qos_groups: int
        An integer representing the number of QoS groups.

    """
    def __init__(self, bottleneck_type="low"):
        self._bottleneck_type = bottleneck_type
        super().__init__()

    def _setup_migration(self, migration_idx):
        """Setups a migration for `migration_idx`.

        The setup involves simulating a load for the migration and choosing
        a random source and destination controller.

        Parameters
        ----------
        migration_idx: int
            An integer representing the index of the migration being set up.

        Returns
        -------
        Migration
            A created `Migration` object.

        """
        load = max(1.00, round(np.random.normal(10, 5), 2))
        return self._construct_migration_from_load(migration_idx, load)

    def _get_controller_line(self, controller_idx):
        """Constructs that controller line for `controller_idx`.

        The controller line for `controller_idx` consists of the name of the
        controller and its capacity. This capacity is the amount of load the
        controller can accomodate from migrations in a single round. All
        arguments are space separated.

        Parameters
        ----------
        controller_idx: int
            An integer representing the index of the controller for which
            the line is generated.

        Returns
        -------
        str
            A string representing the controller line.

        """
        min_cap, max_cap = self._get_controller_cap_bounds(controller_idx)
        capacity = utils.gaussian_controller_capacity(
            min_cap, max_cap, self._bottleneck_type)
        return "c{0} {1:.2f}\n".format(controller_idx, capacity)

    def _get_qos_line(self, qos_idx):
        """Constructs the QoS line for `qos_idx`.

        The QoS line for `qos_idx` consists of the name of the QoS
        group and its capacity.This capacity is the maximum amount of
        migrations within this group that can be completed in a single round.
        All arguments are space separated.

        Parameters
        ----------
        qos_idx: int
            An integer representing the index of the QoS group for which the
            line is generated.

        Returns
        -------
        str
            A string representing the QoS line.

        """
        capacity = utils.gaussian_qos_capacity(
            self._qos_groups[qos_idx], self._bottleneck_type)
        return "g{0} {1}\n".format(qos_idx, capacity)
