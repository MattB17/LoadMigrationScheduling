"""The `Parser` class is used to parse a file containing data specifying a
migration instance.

"""
from MigrationScheduling.Data import (Migration,
                                      ControllerConstraint,
                                      QosConstraint)

class Parser:
    """Used to parse files containing a migration instance.

    Attributes
    ----------
    _migrations: dict
        A dictionary of migrations. The keys are strings specifying the
        name of the switch involved in the migration and the keys are
        `Migration` objects representing the migrations.
    _controller_constraints: set
        A set of `ControllerConstraint` objects.
    _qos_constraints: set
        A set of `QosConstraint` objects.

    """
    def __init__(self):
        self._migrations = {}
        self._controller_constraints = set()
        self._qos_constraints = set()

    def get_migrations(self):
        """The migrations built by the parser.

        Returns
        -------
        dict
            A dictionary of the migrations built by the parser. The keys are
            strings representing the names of the switches and the
            corresponding value is a `Migration` object representing the
            migration.

        """
        return self._migrations

    def get_controller_constraints(self):
        """The controller constraints built by the parser.

        Returns
        -------
        set
            A set of `ControllerConstraint` objects representing the
            controller constraints built by the parser.

        """
        return self._controller_constraints

    def get_qos_constraints(self):
        """The QoS constraints built by the parser.

        Returns
        -------
        set
            A set of `QoSContraint` objects representing the constraints for
            the QoS groups built by the parser.

        """
        return self._qos_constraints

    def get_switch_ids(self):
        """The collection of switch IDs for the migrations.

        Returns
        -------
        list
            A list of integers representing the IDs of the switches involved
            in the migrations.

        """
        ids = [migration.get_switch_idx()
               for migration in self._migrations.values()]
        ids.sort()
        return ids

    def get_controller_ids(self):
        """The collection of controller IDs for controller constraints.

        Returns
        -------
        list
            A list of integers representing the IDs of the controllers that
            are destinations of the migrations.

        """
        ids = [controller_const.get_controller_idx()
               for controller_const in self._controller_constraints]
        ids.sort()
        return ids

    def get_group_ids(self):
        """The collection of IDs of the QoS groups.

        Returns
        -------
        list
            A list of integers representing the IDs of the QoS groups.

        """
        ids = [group_const.get_group_idx()
               for group_const in self._qos_constraints]
        ids.sort()
        return ids

    def parse_migrations(self, migration_file):
        """Parses `migration_file` for the data of a migration instance.

        The object is updated with the data for the migration instance.

        Parameters
        ----------
        migration_file: str
            The name of the file containing the data of a migration instance.

        Returns
        -------
        None

        """
        with open(migration_file, 'r') as data_file:
            for line in data_file:
                if (line[0] == "s"):
                    self._add_migration(line.strip().split(" "))
                elif (line[0] == "c"):
                    self._add_controller_constraint(line.strip().split(" "))
                elif (line[0] == "g"):
                    self._add_qos_constraint(line.strip().split(" "))
        return

    def to_data(self):
        """Creates a `InstanceData` object from the parsed data.

        Returns
        -------
        InstanceData
            An `InstanceData` object containing the data parsed for the
            migration instance.

        """
        return InstanceData(
            self._migrations,
            self._controller_constraints,
            self._qos_constraints,
            self.get_switch_ids(),
            list(range(utils.upper_bound_rounds(len(self._migrations)))),
            self.get_controller_ids(),
            self.get_group_ids())

    def _add_migration(self, migration_data):
        """Adds a migration to the parser based on `migration_data`.

        A `Migration` object is created and added to `_migrations`. The key
        is a string representing the name of the switch in the migration.

        Parameters
        ----------
        migration_data: list
            A list of strings specifying the data for the migrations. The
            first three elements identify the switch, destination controller,
            and the load of the migration. All subsequent elements identify
            the QoS groups to which the migration belongs.

        Returns
        -------
        None

        """
        migration = Migration(
            migration_data[0], migration_data[1], float(migration_data[2]))
        curr_idx = 3
        n = len(migration_data)
        while (curr_idx < n):
            migration.add_qos_group(migration_data[curr_idx])
            curr_idx += 1
        self._migrations[migration_data[0]] = migration

    def _add_controller_constraint(self, controller_data):
        """Adds a new controller constraint based on `controller_data`.

        A new `ControllerConstraint` object is constructed and added to
        `_controller_constraints`.

        Parameter
        ---------
        controller_data: list
            A two element list containing the data for a controller
            constraint. The first is a string representing the name of the
            controller and the second is a string representing the
            controller's capacity.

        Returns
        -------
        None

        """
        constraint = ControllerConstraint(
            controller_data[0], float(controller_data[1]))
        for migration in self._migrations.values():
            if migration.get_dst_controller() == controller_data[0]:
                constraint.add_switch(migration.get_switch())
        self._controller_constraints.add(constraint)

    def _add_qos_constraint(self, qos_data):
        """Adds a QoS constraint based on `qos_data`.

        A new `QoSConstraint` is added to `_qos_constraints`.

        Parameters
        ----------
        qos_data: list
            A two element list specifying the data for a QoS constraint. The
            first element is a string representing the name of the QoS group
            and the second is a string representing the number of concurrent
            migrations allowed within the QoS group.

        Returns
        -------
        None

        """
        constraint = QosConstraint(qos_data[0], int(qos_data[1]))
        for migration in self._migrations.values():
            if migration.is_in_group(qos_data[0]):
                constraint.add_switch(migration.get_switch())
        self._qos_constraints.add(constraint)
