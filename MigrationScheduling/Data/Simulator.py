"""The Simulator class is used to simulate load migration scheduling
instances.

"""
import random
from MigrationScheduling.Data import Migration

class Simulator:
    """Used to simulate a load migration scheduling instance.

    Attributes
    ----------
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
    def __init__(self):
        self._migrations = []
        self._num_migrations = 0
        self._controllers = []
        self._num_controllers = 0
        self._qos_groups = []
        self._num_qos_groups = 0

    def _initialize(self, num_migrations):
        """Initializes the simulator.

        The number of controllers and number of qos_groups are selected and
        their parameters are initialized for the simulation.

        Parameters
        ----------
        num_migrations: int
            An integer representing the number of migrations in the
            simulation.

        Returns
        -------
        None

        """
        self._num_controllers = random.randint(1, num_migrations)
        self._controllers = [(0, 0.0) for _ in range(self._num_controllers)]
        self._num_qos_groups = random.randint(1, int(1.3 * num_migrations))
        self._qos_groups = [0 for _ in range(self._num_qos_groups)]

    def _create_migration(self, migration_idx):
        """Simulates a new migration.

        For the simulated migration a random controller is picked as the
        destination controller and a random load is chosen for the migration.

        Parameters
        ----------
        migration_idx: int
            An integer representing the index of the migration being
            simulated.

        Returns
        -------
        Migration
            A `Migration` object representing a simulated migration.

        """
        load = round(random.random() * 400, 2)
        dst = random.randint(1, self._num_controllers) - 1
        migration = Migration(
            "s{}".format(migration_idx), "c{}".format(dst), load)
        self._controllers[dst][0] += 1
        self._controllers[dst][1] = max(load, self._controllers[dst][1])
        num_groups = random.randint(1, self._num_qos_groups) - 1
        group_ids = random.sample(range(self._num_qos_groups), num_groups)
        for group_id in group_ids:
            migration.add_qos_group("g{}".format(group_id))
            self._qos_groups[group_id] += 1
        return migration
