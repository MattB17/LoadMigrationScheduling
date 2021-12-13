"""The `BoundedParetoSimulator` class is used to simulate load migration
scheduling instances using the Bounded Pareto distribution.

"""
import random
import sympy.stats as syms
from MigrationScheduling import utils
from MigrationScheduling.Data import Migration
from MigrationScheduling.Sim.Simulator import Simulator

class BoundedParetoSimulator(Simulator):
    """Used to simulate a load migration scheduling instance.

    Parameters
    ----------
    alpha: float
        A positive float representing the alpha value for the Pareto
        distribution.

    Attributes
    ----------
    _alpha: float
        The alpha value (shape parameter) for the Pareto distribution.
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
    def __init__(self, alpha):
        self._alpha = alpha
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
        load = syms.sample(syms.BoundedPareto('load', self._alpha, 1, 100))
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
        min_cap, _ = self._get_controller_cap_bounds(controller_idx)
        if round(min_cap, 1) == 100.0:
            capacity = min_cap
        else:
            capacity = 100.0 + min_cap- syms.sample(syms.BoundedPareto(
                'alpha', self._alpha, min_cap, 100.0))
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
        group_size = self._qos_groups[qos_idx]
        if group_size == 1:
            capacity = 1
        else:
            capacity = min(group_size, max(int(group_size + 1 - syms.sample(
                syms.BoundedPareto('beta', self._alpha, 1, group_size))), 1))
        return "g{0} {1}\n".format(qos_idx, capacity)
