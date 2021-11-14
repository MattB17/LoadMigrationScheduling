"""The `Round` class is a container class used to represent information
about a round for the load migration scheduling problem.

"""
import copy

class Round:
    """Stores the information related to a scheduling round.

    Parameters
    ----------
    round_num: int
        An integer representing the round number.
    controller_caps: dict
        A dictionary of controller capacities. The keys are strings
        representing the names of the destination controllers and the
        corresponding value is a float representing the amount of migration
        load that the destination controller can handle in a single round.
    qos_caps: dict
        A dictionary of QoS group capacities. The keys are strings
        representing the names of the QoS groups and the corresponding value
        is an integer representing the maximum amount of migrations from the
        group that can be scheduled in a single round.

    Attributes
    ----------
    _round_num: int
        The round number.
    _rem_controller_caps: dict
        A dictionary representing the remaining capacity of the destination
        controllers in the round, after accounting for the current migrations.
    _rem_qos_caps: dict
        A dictionary representing the remaining capcity of the QoS groups in
        the round, after accounting for the current migrations.
    _migrations: set
        A set of strings representing the name of the migrations completed
        in the round.

    """
    def __init__(self, round_num, controller_caps, qos_caps):
        self._round_num = round_num
        self._rem_controller_caps = copy.deepcopy(controller_caps)
        self._rem_qos_caps = copy.deepcopy(qos_caps)
        self._migrations = set()

    def can_schedule_migration(self, migration):
        """Indicates if `migration` can be scheduled in the round.

        Determines whether `migration` can be scheduled in the round given
        the remaining capacity of the controllers and QoS groups.

        Parameters
        ----------
        migration: Migration
            A `Migration` object representing the migration to be scheduled.

        Returns
        -------
        bool
            True if `migration` can be scheduled in the round without
            exceeding the remaining capacities of the controllers and QoS
            groups. Otherwise, False.

        """
        within_controller = self._within_controller_cap(
            migration.get_dst_controller(), migration.get_load())
        within_groups = self._within_qos_caps(migration.get_groups())
        return within_controller and within_groups

    def schedule_migration(self, migration):
        """Schedules `migration` in the round.

        Parameters
        ----------
        migration: Migration
            A `Migration` object representing the migration being scheduled
            in the round.

        Returns
        -------
        None

        """
        self._migrations.add(migration.get_switch())
        self._reduce_controller_cap(migration.get_dst_controller(),
                                    migration.get_load())
        self._reduce_qos_caps(migration.get_groups())

    def _within_controller_cap(self, controller, migration_load):
        """Whether `migration_load` is within the capacity of `controller`.

        Determines if a migration with load `migration_load` can be scheduled
        in the round without exceeding the remaining capacity of
        `controller`.

        Parameters
        ----------
        controller: str
            A string representing the name of the controller to which the
            migration is destined.
        migration_load: float
            A float representing the load incurred on `controller_name` to
            complete the migration.

        Returns
        -------
        bool
            True if the migration can be scheduled in the round without
            exceeding the controller capacity.

        """
        if (controller in self._rem_controller_caps):
            return self._rem_controller_caps[controller] >= migration_load
        return False

    def _within_qos_caps(self, qos_groups):
        """Whether another migration in `qos_groups` can be scheduled.

        Determines if a migration that belongs to each QoS group in
        `qos_groups` can be scheduled without exceeding the capacity of any
        QoS group.

        Parameters
        ----------
        qos_groups: collection
            A collection of strings representing the names of the QoS groups
            to which the migration belongs.

        Returns
        -------
        bool
            True if a migration belonging to the groups of `qos_groups` can
            be scheduled without exceeding the capacity of any QoS group.

        """
        for qos_group in qos_groups:
            if (qos_group not in self._rem_qos_caps or
                self._rem_qos_caps[qos_group] < 1):
                return False
        return True

    def _reduce_controller_cap(self, controller, load):
        """Reduces the controller capacity for `controller` by `load`.

        The remaining capacity of `controller` is reduced by `load` to
        reflect the scheduling of a migration requiring `load` controller
        resources.

        Parameters
        ----------
        controller: str
            The name of the controller for which the capacity is reduced.
        load: float
            A float representing the additional load assigned to the
            controller in the round.

        Returns
        -------
        None

        """
        self._rem_controller_caps[controller] -= load

    def _reduce_qos_caps(self, qos_groups):
        """Reduces the QoS group capacities for `qos_groups` by 1.

        The remaining capacity for each QoS group in `qos_groups` is reduced
        by 1 to accomodate a migration belonging to all the QoS groups in
        `qos_groups`.

        Parameters
        ----------
        qos_groups: collection
            A collection of strings representing the QoS groups for which
            the capacities are reduced.

        Returns
        -------
        None

        """
        for qos_group in qos_groups:
            self._rem_qos_caps[qos_group] -= 1

    def print_migrations(self):
        """Prints the migrations completed in the round.

        Returns
        -------
        None

        """
        print("Migrations completed in round {0}: {1}".format(
            self._round_num, " ".join(self._migrations)))
