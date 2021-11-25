"""The LogNormalSimulator class is used to simulate load migration
scheduling instances using the LogNormal distribution.

"""
import numpy as np
from MigrationScheduling import utils
from MigrationScheduling.Data import Migration
from MigrationScheduling.Sim.Simulator import Simulator


class LogNormalSimulator(Simulator):
    """Used to simulate a load migration scheduling instance.

    Parameters
    ----------
    mu: float
        A float representing the underlying mean for the normal distribution.
    sigma: float
        A float representing the underlying standard deviation for the normal
        distribution.

    Attributes
    ----------
    _mu: float
        The underlying mean for the normal distribution.
    _sigma: float
        The underlying standard deviation for the normal distribution.
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
    def __init__(self, mu, sigma):
        self._mu = utils.get_log_mean(mu, sigma)
        self._sigma = utils.get_log_std(mu, sigma)
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
        load = max(1.00, round(utils.sample_with_log_op(10, 5), 2))
        dst = self._assign_to_controller(load)
        return Migration("s{}".format(migration_idx), "c{}".format(dst), load)

    def _get_controller_line(self, controller_idx):
        """Constructs the controller line for `controller_idx`.

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
        capacity = min(max_cap, min_cap + max(0,
            (1 - np.random.lognormal(self._mu, self._sigma)) *
            (max_cap - min_cap)))

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
        group_size = self._qos_groups[qos_idx]
        capacity = int(min(group_size, 1.00 + max(0.00,
            (1 - np.random.lognormal(self._mu, self._sigma)) *
            (group_size - 1))))
        return "g{0} {1}\n".format(qos_idx, capacity)
