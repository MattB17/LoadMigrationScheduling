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
    _in_switches: set
        The collection of switches to be migrated to the controller.
    _out_switches: set
        The collection of switches to be migrated from the controller.

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
        self._in_switches = set()
        self._out_switches = set()

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

    def get_in_switches(self):
        """The collection of switches to be migrated to the controller.

        Returns
        -------
        set
            A set representing the switches to be migrated to the controller.

        """
        return self._in_switches

    def get_out_switches(self):
        """The collection of switches to be migrated from the controller.

        Returns
        -------
        set
            A set representing the switches to be migrated from the
            controller.

        """
        return self._out_switches

    def get_constraint_switches(self, resiliency=False):
        """The switches that appear in the controller constraint.

        The collection of constraint switches depends on the value of
        `resiliency`. A value of False indicates that the constraint switches
        are only switches that are part of migrations destined to the
        controller. A value of True also adds the switches that are being
        migrated away from the controller

        Returns
        -------
        set
            A set representing the switches that appear in the controller
            constraint.

        """
        if resiliency:
            return self._in_switches.union(self._out_switches)
        return self._in_switches

    def get_controller_idx(self):
        """The index of the controller corresponding to the constraint.

        Returns
        -------
        int
            An integer representing the index of the controller used in
            the constraint.

        """
        return int(self._controller[1:])

    def add_in_switch(self, switch_name):
        """Adds `switch_name` as a switch to be migrated to the controller.

        Parameters
        ----------
        switch_name: str
            The name of a switch to be migrated to the controller.

        Returns
        -------
        None

        """
        self._in_switches.add(switch_name)

    def add_out_switch(self, switch_name):
        """Adds `switch_name` as a switch to be migrated from the controller.

        Parameters
        ----------
        switch_name: str
            The name of a switch to be migrated from the controller.

        Returns
        -------
        None

        """
        self._out_switches.add(switch_name)

    def __str__(self):
        """A string representation of the controller constraint.

        Returns
        -------
        str
            A string representing the constraint for the controller.

        """
        cont_str = ("Constraint for controller {0} " +
                    "with a capacity of {1:.2f}.\n").format(
                    self._controller, self._capacity)
        if self._out_switches:
            cont_str += "Source for switches: {}\n".format(
                " ".join(self._out_switches))
        if self._in_switches:
            cont_str += "Destination for switches: {}\n".format(
                " ".join(self._in_switches))
        return cont_str
