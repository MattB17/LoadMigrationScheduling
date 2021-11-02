"""The `ControllerConstraint` class contains the information needed to
build the capacity constraints for a controller.

"""
from MigrationScheduling import exceptions as exc

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

    """
    def __init__(self, controller, capacity):
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

    def get_capacity(self):
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
        try:
            return int(self._controller[1:])
        except:
            raise exc.InvalidName("Controller names should be in the form " +
                                  "'cx' where 'x' is the controller ID")

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
