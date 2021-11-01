"""The `Migration` class is used to store the information relating to the
migration of a switch in an SDN.

"""

class Migration:
    """Stores the details of a switch migration.

    Parameters
    ----------
    switch: str
        A string identifying the switch to be migrated.
    dst_controller: str
        A string identifying the destination controller.
    load: float
        A float identifying the load used during the migration.

    Attributes
    ----------
    _switch: str
        The name of the switch.
    _dst_controller: str
        The name of the destination controller.
    _load: float
        The load used during the migration
    _groups: set
        The collection of QoS groups to which the switch belongs.

    """
    def __init__(self, switch, dst_controller, load):
        self._switch = switch
        self._dst_controller = dst_controller
        self._load = load
        self._groups = set()

    def get_switch(self):
        """The switch being migrated.

        Returns
        -------
        str
            A string representing the name of the switch being migrated.

        """
        return self._switch

    def get_dst_controller(self):
        """The controller to which the switch should be migrated.

        Returns
        -------
        str
            A string representing the name of the destination controller for
            the migration.

        """
        return self._dst_controller

    def get_load(self):
        """The load incurred when performing the migration.

        Returns
        -------
        float
            A float representing the load incurred on the destination
            controller when performing the migration.

        """
        return self._load

    def add_qos_group(self, group_name):
        """Adds `group_name` to the collection of QoS groups for the switch.

        This signifies that the switch is part of the QoS group `group_name`.

        Parameters
        ----------
        group_name: str
            The name of the QoS group being added.

        Returns
        -------
        None

        """
        self._groups.add(group_name)

    def get_groups(self):
        """The collection of QoS groups to which the switch belongs.

        Returns
        -------
        set
            A set of strings representing the names of the QoS groups of which
            the switch is a member.

        """
        return self._groups

    def is_in_group(self, group_name):
        """Identifies if the switch belongs to the QoS group `group_name`.

        Parameters
        ----------
        group_name: str
            A string representing the name of the QoS group being checked.

        Returns
        -------
        bool
            True if the switch is in the QoS group `group_name`. Otherwise,
            False.

        """
        return group_name in self._groups

    def __str__(self):
        """A string representation of the migration.

        Returns
        -------
        str
            A string representing the migration.

        """
        return ("Migrate switch {0} to controller {1} with load of {2}.\n" +
                "QoS groups: {3}").format(
                    self._switch, self._dst_controller,
                    self._load, " ".join(self._groups))
