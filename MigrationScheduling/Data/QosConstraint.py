"""The `QosConstraint` class stores the information relating to the
constraint for a QoS group.

"""
from MigrationScheduling import exceptions as exc
from MigrationScheduling.Data import ConstraintDict

class QosConstraint:
    """The information relating to the constraint for a QoS group.

    Parameters
    ----------
    group: str
        A string representing the name of the QoS group.
    capacity: int
        An integer representing the maximum number of migrations from the QoS
        group that can take place simultaneously.

    Attributes
    ----------
    _group: str
        The name of the QoS group to which the constraint applies.
    _capacity: int
        The maximum number of concurrent migrations allowed from the group.
    _switches: set
        The collection of switches in the QoS group.

    """
    def __init__(self, group, capacity):
        self._group = group
        self._capacity = capacity
        self._switches = set()

    def get_group(self):
        """The QoS group.

        Returns
        -------
        str
            A string representing the name of the QoS group.

        """
        return self._group

    def get_cap(self):
        """The QoS group capacity.

        Returns
        -------
        int
            An integer representing the maximum number of concurrent
            migrations that can take place within the QoS group.

        """
        return self._capacity

    def get_switches(self):
        """The switches in the QoS group.

        Returns
        -------
        set
            A set representing the name of the switches in the QoS group.

        """
        return self._switches

    def get_group_idx(self):
        """The index of the QoS group.

        Returns
        -------
        int
            An integer representing the index of the QoS group to which the
            constraint applies.

        """
        try:
            return int(self._group[1:])
        except:
            raise exc.InvalidName("Group names should be in the form 'gx' " +
                                  "where 'x' is the group ID")

    def add_switch(self, switch_name):
        """Adds `switch_name` to the QoS group.

        Parameters
        ----------
        switch_name: str
            The name of the string to be added to the QoS group.

        Returns
        -------
        None

        """
        self._switches.add(switch_name)

    def get_constraint_dict(self):
        """A dict representing the constraint information for the QoS group.

        The dictionary is a compact representation of the information needed
        for scheduling while accommodating the QoS constraint.

        Returns
        -------
        ConstraintDict
            A `ConstraintDict` object representing the constraint information
            for the QoS group.

        """
        return ConstraintDict(
            self._capacity, len(self._switches), self._switches)

    def __str__(self):
        """A string representation of the QoS constraint.

        Returns
        -------
        str
            A string representing the QoS constraint.

        """
        return ("QoS Group {0} allowing {1} concurrent migrations.\n" +
                "Switches in QoS group: {2}").format(
                self._group, self._capacity, " ".join(self._switches))
