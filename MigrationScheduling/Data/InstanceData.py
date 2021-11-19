"""The `InstanceData` class contains all the data of a migration scheduling
instance used to construct an optimization model.

"""

class InstanceData:
    """Stores the data of a migration scheduling instance.

    Parameters
    ----------
    migrations: dict
        A dictionary specifying the migrations. The keys are strings denoting
        the name of the switch involved in the migration and the
        corresponding value is a `Migration` object specifying the migration.
    controller_consts: set
        A set of `ControllerConstraint` objects specifying the controller
        constraints for the migrations.
    qos_consts: set
        A set of `QosConstraint` objects specifying the QoS constraints.
    switch_ids: list
        A list of IDs of the switches involved in the migrations.
    round_ids: list
        A list of rounds in which migrations can be scheduled.
    controller_ids: list
        A list of IDs of the controllers in the controller constraints.
    qos_ids: list
        A list of IDs of the QoS groups.

    Attributes
    ----------
    _migrations: dict
        The migrations to be scheduled
    _controller_consts: set
        The controller constraints.
    _qos_consts: set
        The constraints for QoS groups.
    _switch_ids: list
        The IDs of the switches involved in the migrations.
    _round_ids: list
        The IDs of rounds in which migrations can be scheduled.
    _controller_ids: list
        The IDs of the destination controllers for migrations.
    _qos_ids: list
        The IDs of the QoS groups.

    """
    def __init__(self, migrations, controller_consts, qos_consts,
                 switch_ids, round_ids, controller_ids, qos_ids):
        self._migrations = migrations
        self._controller_consts = controller_consts
        self._qos_consts = qos_consts
        self._switch_ids = switch_ids
        self._round_ids = round_ids
        self._controller_ids = controller_ids
        self._qos_ids = qos_ids

    def get_migrations(self):
        """The migrations for the scheduling instance.

        Returns
        -------
        dict
            A dictionary of the migrations for the scheduling instance. The
            keys are strings representing the names of the switches being
            migrated and the corresponding value is a `Migration` object
            for the corresponding migration.

        """
        return self._migrations

    def get_migration(self, switch_name):
        """Retrieves the migration for `switch_name`.

        Returns
        -------
        Migration
            The `Migration` object representing the migration for
            `switch_name`.

        """
        return self._migrations[switch_name]

    def get_control_consts(self):
        """The controller constraints for the scheduling instance.

        Returns
        -------
        set
            A set of `ControllerConstraint` objects representing the
            controller constraints of the load migration scheduling instance.

        """
        return self._controller_consts

    def get_qos_consts(self):
        """The QoS constraints for the scheduling instance.

        Returns
        -------
        set
            A set of `QosConstraint` objects representing the QoS constraints
            of the load migration scheduling instance.

        """
        return self._qos_consts

    def get_switch_ids(self):
        """The IDs of the switches being migrated.

        Returns
        -------
        list
            A list of integers representing the IDs of switches being
            migrated in the scheduling instance.

        """
        return self._switch_ids

    def get_round_ids(self):
        """The IDs of the scheduling rounds.

        Returns
        -------
        list
            A list of integers indicating the IDs of the rounds in which
            migrations can be scheduled.

        """
        return self._round_ids

    def get_controller_ids(self):
        """The IDs of the destination controllers of migrations.

        Returns
        -------
        list
            A list of integers representing the IDs of controllers which are
            destinations for migrations.

        """
        return self._controller_ids

    def get_qos_ids(self):
        """The IDs of the QoS groups for the migrations.

        Returns
        -------
        list
            A list of integers representing the IDs of the QoS groups in the
            migration scheduling instance.

        """
        return self._qos_ids

    def get_load(self, switch_name):
        """The load incurred by the migration of `switch_name`.

        Parameters
        ----------
        switch_name: str
            A string representing the name of the switch for which the
            migration load is retrieved.

        Returns
        -------
        float
            A float representing the load incurred during the migration of
            `switch_name`.

        """
        return self._migrations[switch_name].get_load()

    def get_switch_id(self, switch_name):
        """The switch ID corresponding to `switch_name`.

        Parameters
        ----------
        switch_name: str
            A string representing the name of the switch for which the ID
            is retrieved.

        Returns
        -------
        int
            An integer representing the ID for the switch `switch_name`.

        """
        return self._migrations[switch_name].get_switch_idx()

    def get_size_string(self):
        """A string representing the parameters of the instance.

        The size string is a space separated string with the number of
        migrations followed by the number of controllers and then the
        number of QoS groups.

        Returns
        -------
        str
            A string representing the parameters of the instance.

        """
        return "{0} {1} {2}".format(
            len(self._switch_ids),
            len(self._controller_ids),
            len(self._qos_ids))
