"""The `ControllerConstraint` class contains the information needed to
build the capacity constraints for a controller.

"""
from MigrationScheduling import validation as val
from MigrationScheduling import exceptions as exc
from MigrationScheduling.Data import ConstraintDict

class ControllerConstraint:
    """Stores the information of the constraints for a controller.

    Parameters
    ----------
    controller: str
        A string representing the name of the controller.
    capacity: float
        A float representing the capacity of the controller.

    Attributes
    ----------
    _controller: str
        The name of the controller to which the constraints apply.
    _capacity: float
        The capacity value used in the constraint.
    _switches: set
        The collection of switches to be migrated to the controller.

    Raises
    ------
    InvalidName
        If `controller` is not a valid name for a controller object. A
        valid name has the form `cx` where `x` is an integer representing the
        controller ID.

    """
    def __init__(self, controller, capacity):
        val.validate_name(controller, 'c', "Controller")
        self._controller = controller
        self._capacity = capacity
        self._switches = set()

    def get_controller(self):
        """The name of the controller to which the constraints apply.

        Returns
        -------
        str
            A string representing the name of the controller.

        """
        return self._controller

    def get_cap(self):
        """The controller's capacity value for the constraint.

        Returns
        -------
        float
            A float representing the controller's capacity.

        """
        return self._capacity

    def get_switches(self):
        """The collection of switches to be migrated to the controller.

        Returns
        -------
        set
            A set representing the switches to be migrated to the controller.

        """
        return self._switches

    def get_controller_idx(self):
        """The index of the controller corresponding to the constraint.

        Returns
        -------
        int
            An integer representing the index of the controller used in
            the constraint.

        """
        return int(self._controller[1:])

    def add_switch(self, switch_name):
        """Adds `switch_name` as a switch to be migrated to the controller.

        Parameters
        ----------
        switch_name: str
            The name of a switch to be migrated to the controller.

        Returns
        -------
        None

        """
        self._switches.add(switch_name)

    def get_total_load(self, migrations):
        """The total load on the controller based on `migrations`.

        The total load is the cumulative load of all migrations in
        `migrations` that are destined for the controller. It represents the
        total load incurred on the controller across all rounds.

        Parameters
        ----------
        migrations: collection
            A collection of `Migration` objects representing the migrations
            to be completed. Used to calculate the load on the controller
            for the given migrations.

        Returns
        -------
        float
            A float representing the total cumulative load that will be
            incurred on the controller based on `migrations`.

        """
        total_load = 0
        for migration in migrations:
            if migration.get_dst_controller() == self._controller:
                total_load += migration.get_load()
        return total_load

    def get_constraint_dict(self, migrations):
        """A dict representing the constraint information for the controller.

        The dictionary is a compact representation of the information needed
        for scheduling while accommodating the controller constraint.

        Parameters
        ----------
        migrations: collection
            A collection of `Migration` object representing all migrations,
            used to calculate the cumulative load on the controller across
            all rounds.

        Returns
        -------
        ConstraintDict
            A `ConstraintDict` object representing the constraint information
            for the controller.

        """
        return ConstraintDict(
            self._capacity, self.get_total_load(migrations), self._switches)

    def __str__(self):
        """A string representation of the controller constraint.

        Returns
        -------
        str
            A string representing the constraint for the controller.

        """
        return ("Constraint for controller {0} with a capacity of {1}.\n" +
                "Destination for switches: {2}").format(
                self._controller, self._capacity, " ".join(self._switches))
