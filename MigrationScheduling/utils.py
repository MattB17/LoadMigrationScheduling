"""A module consisting of utility functions used in modeling and heuristic
algorithms.

"""

def upper_bound_rounds(num_migrations):
    """Gets an upper bound on the number of rounds based on `num_migrations`.

    Parameters
    ----------
    num_migrations: int
        An integer denoting the number of transitions.

    Returns
    -------
    int
        An integer representing an upper bound on the number of rounds to
        complete `num_migrations`.

    """
    return num_migrations

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
