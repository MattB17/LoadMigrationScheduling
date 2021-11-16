"""A module consisting of utility functions used in modeling and heuristic
algorithms.

"""


def get_controller_cap_dict(controller_constraints):
    """Creates a dictionary of controller capacities.

    The keys are strings representing the names of the controllers and the
    corresponding value is a float representing the amount of migration load
    the controller can handle in a single round.

    Parameters
    ----------
    controller_constraints: collection
        A collection of `ControllerConstraint` objects from which the
        dictionary is built.

    Returns
    -------
    dict
        A dictionary of the controller capacities.

    """
    return {constraint.get_controller(): constraint.get_cap()
            for constraint in controller_constraints}


def get_qos_group_cap_dict(qos_constraints):
    """Creates a dictionary of QoS Group capacities.

    The keys are strings representing the names of the QoS groups and the
    corresponding value is an integer representing the maximum amount of
    migrations from the group that can complete in one round.

    Parameters
    ----------
    qos_constraints: collection
        A collection of `QosConstraint` objects from which the dictionary is
        built.

    Returns
    -------
    dict
        A dictionary of the QoS Group capacities.

    """
    return {constraint.get_group(): constraint.get_cap()
            for constraint in qos_constraints}

def get_cap_dicts(instance_data):
    """The dictionaries of controller and QoS group capacities.

    Constructs two dictionaries of controller capacities and QoS group
    capacities for the constraints specified in `instance_data`.

    Parameters
    ----------
    instance_data: InstanceData
        An `InstanceData` object representing the data for a load migration
        scheduling instance, from which the dictionaries are generated.

    Returns
    -------
    dict, dict
        The first dictionary specifies the controller capacities. The keys
        are strings representing the controller names and the corresponding
        value is a float, representing the load that the controller can
        accommodate in each round. The second dictionary specifies QoS
        group capacities. The keys are strings representing the QoS group
        names and the corresponding value is an integer representing the
        number of migrations from that group allowed within a single round.

    """
    controller_caps = get_controller_cap_dict(
        instance_data.get_control_consts())
    qos_caps = get_qos_group_cap_dict(instance_data.get_qos_consts())
    return controller_caps, qos_caps

def get_controller_constraint_dicts(instance_data):
    """The constraint dictionaries for the constraints in `instance_data`.

    Builds a dictionary of `ConstraintDict` objects for the controller
    constraints specified by `instance_data`.

    Parameters
    ----------
    instance_data: InstanceData
        An `InstanceData` object specifying a load migration scheduling
        instance.

    Returns
    -------
    dict
        A dictionary of `ConstraintDict` objects for the controller
        constraints of `instance_data`. The keys are strings representing
        the name of the controllers and the corresponding value is a
        `ConstraintDict` object for the constraint associated with that
        controller.

    """
    migrations = set(instance_data.get_migrations().values())
    return {
        control_const.get_controller() :
        control_const.get_constraint_dict(migrations)
        for control_const in instance_data.get_control_consts()}

def get_qos_constraint_dicts(qos_consts):
    """The constraint dictionaries for the constraints in `qos_consts`.

    Builds a dictionary of `ConstraintDict` objects for the QoS group
    constraints specified by `qos_consts`.

    Parameters
    ----------
    qos_consts: collection
        A collection of `QosConstraint` objects from which the
        `ConstraintDict` objects are retrieved.

    Returns
    -------
    dict
        A dictionary of `ConstraintDict` objects from `qos_consts`. The
        keys are strings representing the name of the QoS groups and the
        corresponding value is a `ConstraintDict` object for the constraint
        associated with that QoS group.

    """
    return {qos_const.get_group(): qos_const.get_constraint_dict()
            for qos_const in qos_consts}

def get_constraint_dicts(instance_data):
    """Dictionaries of the constraints from `instance_data`.

    Dictionaries of the `ConstraintDict` object for the controller
    constraints and QoS constraints are built from `instance_data`.

    Parameters
    ----------
    instance_data: InstanceData
        An `InstanceData` object used to build the dictionaries of
        constraints.

    Returns
    -------
    dict
        Two dictionaries of the constraints from `instance_data`. The first
        is the constraints for the controllers and the second is the
        constraints for the QoS groups. The keys for both are strings
        representing the name of the controller and QoS group, respectively.
        The corresponding value is a `ConstraintDict` object representing the
        constraint.

    """
    control_dict = get_controller_constraint_dicts(instance_data)
    qos_dict = get_qos_constraint_dicts(instance_data.get_qos_consts())
    return control_dict, qos_dict
