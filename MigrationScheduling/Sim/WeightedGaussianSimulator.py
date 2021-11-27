"""The `WeightedGaussianSimulator` class is used to simulate load migration
scheduling instances using a set of Gaussian distributions that are sampled
from based on a random number.

Three distributions are used representing a low bottleneck setting, a medium
bottleneck setting, and a high bottleneck setting. Each constraint samples
from one of the 3 distributions in the proportions given by `low_prop` and
`med_prop`.

"""
import random
import numpy as np
from MigrationScheduling import utils
from MigrationScheduling.Data import Migration
from MigrationScheduling.Sim.Simulator import Simulator


class WeightedGaussianSimulator(Simulator):
    """Used to simulate a load migration instance with weighted gaussians.

    Parameters
    ----------
    low_prop: float
        A float in the range [0, 1] representing the proportion of times the
        low bottleneck distribution is sampled from.
    med_prop: float
        A float in the range [0, 1] representing the proportion of times the
        medium bottleneck distribution is sampled from.

    Attributes
    ----------
    _low_prop: float
        The proportion of times the low bottleneck distribution is sampled
        from.
    _med_prop: float
        The proportion of times the medium bottleneck distribution is sampled
        from.
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
    def __init__(self, low_prop=0.6, med_prop=0.3):
        self._low_prop = low_prop
        self._med_prop = med_prop
        super().__init__()

    def _setup_migration(self, migration_idx):
        """Setups a migration for `migration_idx`.

        The setup involves simulating a load for the migration and choosing
        a random destination controller.

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
        dst = self._assign_to_controller(load)
        return Migration("s{}".format(migration_idx), "c{}".format(dst), load)

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
        capacity = utils.weighted_controller_capacity(
            min_cap, max_cap, self._low_prop, self._med_prop)
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
        capacity = utils.weighted_qos_capacity(
            self._qos_groups[qos_idx], self._low_prop, self._med_prop)
        return "g{0} {1}\n".format(qos_idx, capacity)
