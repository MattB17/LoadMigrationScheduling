"""The `ControllerConstraint` class contains the information needed to
build the capacity constraints for a controller.

"""

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
