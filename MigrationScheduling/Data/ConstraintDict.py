"""The `ConstraintDict` class is a container class used to hold the
information for a constraint of the load migration scheduling problem.

"""
from MigrationScheduling import exceptions as exc


class ConstraintDict:
    """Holds the info for a constraint of the load migration problem.

    Parameters
    ----------
    capacity: float
        A float representing the constraint capacity. This is the RHS of the
        constraint.
    load: float
        A float representing the total load on the constraint across all
        rounds. That is, it would be the total load if all migrations
        associated with the constraint were scheduled in a single round.
    switches: collection
        A collection of strings representing the names of the switches
        associated with the constraint. This identifies the migrations that
        appear on the LHS of the constraint.

    Attributes
    ----------
    _capacity: float
        The constraint capacity.
    _load: float
        The load on the constraint.
    _switches: set
        A set of strings representing the names of switches associated with
        the constraint.

    """
    def __init__(self, capacity, load, switches):
        self._capacity = capacity
        self._load = load
        self._switches = {switch for switch in switches}

    def get_capacity(self):
        """The capacity of the constraint.

        Returns
        -------
        float
            A float representing the capacity of the constraint.

        """
        return self._capacity

    def get_load(self):
        """The load on the constraint.

        Returns
        -------
        float
            A float representing the load on the constraint.

        """
        return self._load

    def get_switches(self):
        """The switches associated with the constraint.

        Returns
        -------
        set
            A set of strings representing the names of the switches
            associated with the constraint.

        """
        return self._switches

    def remove_switch(self, switch_name, switch_load):
        """Removes `switch_name` from the constraint.

        The switch with name `switch_name` is removed and the load on the
        constraint is reduced by `switch_load`.

        Parameters
        ----------
        switch_name: str
            A string representing the name of the switch being removed.
        switch_load: float
            A float representing the load incurred by the constraint for
            `switch_name`.

        Raises
        ------
        SwitchNotFound
            If there is no switch named `switch_name` in the set of switches
            for the constraint.

        Returns
        -------
        None

        """
        if switch_name not in self._switches:
            raise exc.SwitchNotFound(switch_name)
        self._load -= switch_load
        self._switches.remove(switch_name)

    def get_load_factor(self):
        """The load factor on the constraint.

        The load factor is defined as the load on the constraint divided by
        the capacity of the constraint. It represents the degree to which the
        constraint is overloaded.

        Returns
        -------
        float
            A float representing the load factor on the constraint.

        """
        return self._load / self._capacity
