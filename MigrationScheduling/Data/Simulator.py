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

    def run(self, num_migrations, output_file):
        """Simulates and outputs a load migration scheduling instance.

        Parameters
        ----------
        num_migrations: int
            The number of migrations in the simulated instance.
        output_file: str
            A string representing the name of the file to which the instance
            will be output.

        Returns
        -------
        None

        """
        self._num_migrations = num_migrations
        self._initialize(num_migrations)
        self._migrations = [self._create_migration(migration_idx)
                            for migration_idx in range(self._num_migrations)]
        self._output_simulated_instance(output_file)


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
        self._num_controllers = random.randint(1, int(1.5 *num_migrations))
        self._controllers = [[0, 0.0] for _ in range(self._num_controllers)]
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

    def _get_migration_line(self, migration):
        """Constructs the migration line for `migration`.

        The migration line for `migration` consists of the name of the
        switch and the name of the destination controller of the migration.
        This is followed by the load incurred on the controller during the
        migration and the set of QoS groups. All arguments are space
        separated.

        Parameters
        ----------
        migration: Migration
            A `Migration` object representing the migration for which the
            migration line is generated.

        Returns
        -------
        str
            A string representing the migration line.

        """
        return "{0} {1} {2} {3}\n".format(
            migration.get_switch(), migration.get_dst_controller(),
            migration.get_load(), " ".join(migration.get_groups()))

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
        min_cap = self._controllers[controller_idx][1]
        max_cap = (self._controllers[controller_idx][0] *
                   self._controllers[controller_idx][1])
        return "c{0} {1}\n".format(
            controller_idx, min_cap + random.random() * (max_cap - min_cap))

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
        return "g{0} {1}\n".format(
            qos_idx, random.randint(1, self._qos_groups[qos_idx]))

    def _output_simulated_instance(self, output_file):
        """Outputs the simulated load migration scheduling instance.

        The simulated load migration scheduling instance is written to
        `output_file`.

        Parameters
        ----------
        output_file: str
            A string representing the name of the file to which the instance
            will be written.

        Returns
        -------
        None

        """
        with open(output_file, 'w') as migration_file:
            for migration in self._migrations:
                migration_file.write(self._get_migration_line(migration))
            for controller_idx in range(self._num_controllers):
                if self._controllers[controller_idx][0] > 0:
                    migration_file.write(
                        self._get_controller_line(controller_idx))
            for qos_idx in range(self._num_qos_groups):
                if self._qos_groups[qos_idx] > 0:
                    migration_file.write(self._get_qos_line(qos_idx))