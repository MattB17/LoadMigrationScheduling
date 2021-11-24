"""A module consisting of utility functions used in modeling and heuristic
algorithms.

"""
import os
import re
import random
import numpy as np
from MigrationScheduling import specs
from MigrationScheduling.Data import ConstraintDict


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

def calculate_load_on_controller(controller_name, migrations):
    """Calculates the load that `migrations` impose on `controller_name`.

    The load imposed by `migrations` on `controller_name` is the sum of the
    migration loads for the subset of migrations that are destined to
    `controller_name`.

    Parameters
    ----------
    controller_name: str
        The name of the controller for which the load is calculated.
    migrations: collection
        A collection of `Migration` objects used to calculate the load.

    Returns
    -------
    float
        A float representing the load imposed on `controller_name` by the
        migrations of `migrations`.

    """
    total_load = 0
    for migration in migrations:
        if migration.get_dst_controller() == controller_name:
            total_load += migration.get_load()
    return total_load

def get_constraint_dict_for_controller(control_const, migrations):
    """Builds a constraint dict for `control_consts`.

    Parameters
    ----------
    control_const: ControllerConstraint
        The `ControllerConstraint` from which the constraint dict is built.
    migrations: collection
        A collection of `Migration` objects representing the migrations
        used to build the constraint dict.

    Returns
    -------
    ConstraintDict
        A `ConstraintDict` object representing the constraint dict for
        `control_const` based on `migrations`.

    """
    return ConstraintDict(
        control_const.get_cap(),
        calculate_load_on_controller(control_const.get_controller(),
                                     migrations),
        control_const.get_switches())

def get_constraint_dict_for_qos_group(qos_const):
    """Builds a constraint dict for `qos_const`.

    Parameters
    ----------
    qos_const: QosConstraint
        The `QosConstraint` from which the constraint dict is built.

    Returns
    -------
    ConstraintDict
        A `ConstraintDict` object representing the constraint dict for
        `QosConstraint`.

    """
    switches = qos_const.get_switches()
    return ConstraintDict(qos_const.get_cap(), len(switches), switches)

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
        get_constraint_dict_for_controller(control_const, migrations)
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
    return {qos_const.get_group():
            get_constraint_dict_for_qos_group(qos_const)
            for qos_const in qos_consts}

def get_constraints_dict(instance_data):
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
        A dictionary of the constraints from `instance_data`. The dictionary
        contains both controller and QoS group constraints. The keys are
        strings representing the name of the constraintz and the
        corresponding values is the associated `ConstraintDict` object.

    """
    control_dict = get_controller_constraint_dicts(instance_data)
    qos_dict = get_qos_constraint_dicts(instance_data.get_qos_consts())
    return {**control_dict, **qos_dict}


def generate_controller_capacity(min_cap, max_cap, bottleneck_type):
    """Generates the capacity for a controller in [`min_cap`, `max_cap`].

    The controller capacity is picked from the range [`min_cap`, `max_cap`]
    based on `bottleneck_type`.

    Parameters
    ----------
    min_cap: float
        A float representing the minimum controller capacity.
    max_cap: float
        A float representing the maximum controller capacity.
    bottleneck_type: str
        A string representing the bottleneck setting used to generate the
        group capacity. Accepted values are 'high', 'medium', and 'low'.
        The capacity is calculated relative to the group size.

    Returns
    -------
    float
        A float representing the capacity for the controller.

    """
    if bottleneck_type == "high":
        return min_cap
    cap_mean = 0.2
    if bottleneck_type == "low":
        cap_mean = 0.5
    return min(max_cap, min_cap + max(0,
        np.random.normal(cap_mean, 0.3, 1)[0] * (max_cap - min_cap)))


def generate_qos_capacity(group_size, bottleneck_type):
    """Generates the capacity for a QoS group of size `group_size`.

    The capacity is a factor of `group_size` and `bottleneck_type`.

    Parameters
    ----------
    group_size: int
        An integer representing the number of migrations in the QoS group.
    bottleneck_type: str
        A string representing the bottleneck setting used to generate the
        group capacity. Accepted values are 'high', 'medium', and 'low'.
        The capacity is calculated relative to the group size.

    Returns
    -------
    int
        An integer representing the capacity for the QoS group.

    """
    if bottleneck_type == "high":
        return 1
    cap_mean = 0.2
    if bottleneck_type == "low":
        cap_mean = 0.5
    return int(min(group_size, max(1.0,
        np.random.normal(cap_mean, 0.3, 1)[0] * group_size)))


def get_all_files_by_pattern(file_dir, file_pattern):
    """Gets all files in `file_dir` matching `file_pattern`.

    Searches through `file_dir` for all files that have a pattern matching
    the one specified by `file_pattern`.

    Parameters
    ----------
    file_dir: str
        A string representing the name of the directory that is searched.
    file_pattern: str
        A string identifying the file pattern to be searched for.

    Returns
    -------
    list
        A list of strings representing the names of the files in `file_dir`
        that match the pattern specified by `file_pattern`.

    """
    match_str = r"{}.*\.txt".format(file_pattern)
    return [file_name for file_name in os.listdir(file_dir)
            if re.match(match_str, file_name)]

def get_results_header(run_optimizer=True):
    """The header for the file storing the results of solved instances.

    The header is a space-separated string identifying the column names in
    the results file.

    Parameters
    ----------
    run_optimizer: bool
        A boolean value indicating whether the optimizer is run to solve the
        instances exactly. The default value is True. If True, columns
        indicating results for the optimal solution are added to the header.

    Returns
    -------
    str
        A string representing the header for the results file.

    """
    header_str = ("num_migrations num_controllers num_groups " +
                  "vff vff_time cbf cbf_time")
    if run_optimizer:
        header_str += " opt opt_time"
    return header_str + "\n"

def initialize_seeds(seed_num):
    """Initializes the random seeds for reproducibility of experiments.

    Parameters
    ----------
    seed_num: int
        An integer representing the seed used.

    Returns
    -------
    None

    """
    random.seed(seed_num)
    np.random.seed(seed_num)
