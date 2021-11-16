"""This module implements the heuristic algorithms used to solve the
load migration scheduling problem.

"""
import random
from MigrationScheduling import utils
from MigrationScheduling.Model import Round


def find_scheduling_round(existing_rounds, num_rounds, migration):
    """The round in which to schedule `migration` among `existing_rounds`.

    Loops through the rounds in `existing_rounds` to find the first round in
    which `migration` can be scheduled. If `migration` cannot be scheduled in
    any of the rounds then `num_rounds` is returned, signifying that it
    should be scheduled in a new round.

    Parameters
    ----------
    existing_rounds: collection
        A collection of `Round` objects representing the rounds to which
        migrations have already been scheduled.
    num_rounds: int
        An integer representing the number of rounds in `existing_rounds`.
    migration: Migration
        A `Migration` object representing the migration to be scheduled.

    Returns
    -------
    int
        An integer representing the index of the round in `existing_rounds`
        to which `migration` can be scheduled. If this value equals
        `num_rounds` then `migration` cannot be scheduled in any of the
        rounds in `existing_rounds`.

    """
    curr_round = 0
    while curr_round < num_rounds:
        if existing_rounds[curr_round].can_schedule_migration(migration):
            return curr_round
        curr_round += 1
    return curr_round


def get_bottleneck_constraint(controller_consts, qos_consts):
    """The bottleneck constraint of `controller_consts` and `qos_consts`.

    The bottleneck constraint is the most loaded constraint among
    `controller_consts` and `qos_consts`.

    Parameters
    ----------
    controller_consts: dict
        A dictionary of controller constraints. The keys are strings
        representing the names of the controllers and the corresponding value
        is a `ConstraintDict` object representing the constraint.
    qos_consts: dict
        A dictionary of QoS group constraints. The keys are strings
        representing the names of the QoS groups and the corresponding value
        is a `ConstraintDict` object representing the constraint.

    Returns
    -------
    ConstraintDict
        A `ConstraintDict` representing the most loaded constraint among
        `controller_consts` and `qos_consts`.

    """
    max_load = 0
    bottleneck_const = None
    for const_dict in controller_consts.values():
        if const_dict.get_load_factor() > max_load:
            max_load = const_dict.get_load_factor()
            bottleneck_const = const_dict
    for const_dict in qos_consts.values():
        if const_dict.get_load_factor() > max_load:
            max_load = const_dict.get_load_factor()
            bottleneck_const = const_dict
    return bottleneck_const

def select_migration_from_constraint(constraint_dict):
    """Selects a migration from `constraint_dict`.

    Parameters
    ----------
    constraint_dict: ConstraintDict
        The `ConstraintDict` object from which the migration is selected.

    Returns
    -------
    Migration
        A `Migration` object selected from `ConstraintDict`.

    """
    return random.sample(constraint_dict.get_switches(), 1)[0]

def remove_migration_from_constraints(migration, control_consts, qos_consts):
    """Removes `migration` from `control_consts` and `qos_consts`.

    `control_consts` and `qos_consts` are updated to reflect the removal of
    `migration`, signalling that the migration has been scheduled.

    Parameters
    ----------
    control_consts: dict
        A dictionary of controller constraints. The keys are strings
        representing the names of the controllers and the corresponding value
        is a `ConstraintDict` object representing the constraint.
    qos_consts: dict
        A dictionary of QoS group constraints. The keys are strings
        representing the names of the QoS groups and the corresponding value
        is a `ConstraintDict` object representing the constraint.

    Returns
    -------
    dict, dict
        The dictionaries obtained from `control_consts` and `qos_consts`,
        respectively, after removing `migration` from the constraints
        involving that migration.

    """
    control_consts[migration.get_dst_controller()].remove_switch(
        migration.get_switch(), migration.get_load())
    if not len(control_consts[migration.get_dst_controller()].get_switches()):
        del control_consts[migration.get_dst_controller()]
    for group in migration.get_groups():
        qos_consts[group].remove_switch(migration.get_switch(), 1)
        if not len(qos_consts[group].get_switches()):
            del qos_consts[group]
    return control_consts, qos_consts



def vector_first_fit(instance_data):
    """Runs the vectorized version of the first fit algorithm.

    The vectorized first fit algorithm is inspired by the algorithm of the
    same name for vector bin-packing. In this algorithm, we maintain a
    collection of rounds in which migrations are scheduled. For each new
    migration, the migration is scheduled in the first round in which it
    fits.

    A migration fits in a round if the migration's destination controller
    has enough capacity to accomodate the load of the new migration and all
    migrations already scheduled in the round. In addition, for each QoS
    group g containing the migration, g has enough capacity to accomodate
    the new migration and the other migrations of g already scheduled in the
    round.

    If none of the current rounds can handle the new migration, another round
    is added and the migration is added to this new round.

    Parameters
    ----------
    instance_data: InstanceData
        An `InstanceData` object representing the data for a load migration
        scheduling instance, on which the algorithm is run.

    Returns
    -------
    int
        An integer representing the number of rounds used by the algorithm
        to schedule the load migration instance specified by `instance_data`.

    """
    rounds = []
    num_rounds = 0
    controller_caps, qos_caps = utils.get_cap_dicts(instance_data)
    for migration in instance_data.get_migrations().values():
        schedule_round = find_scheduling_round(rounds, num_rounds, migration)
        if schedule_round == num_rounds:
            rounds.append(Round(num_rounds, controller_caps, qos_caps))
            num_rounds += 1
        rounds[schedule_round].schedule_migration(migration)
    return num_rounds


def current_bottleneck_first(instance_data):
    """Runs the current bottleneck first scheduling algorithm.

    The current bottleneck first schedules one migration per iteration in
    the earliest round in which it can fit. If it cannot fit in any existing
    rounds, a new round is created and the migration is scheduled in that
    round. At each iteration the migration selected to be scheduled is chosen
    from the bottleneck constraint. The bottleneck constraint is defined as
    the constraint that is most loaded relative to its capacity. For
    controller constraints this is the sum of the loads of the remaining
    migrations destined to this controller divided by the controller's
    capacity. For QoS group constraints this is the number of remaining
    migrations in the group divided by the group's capacity (the number of
    migrations allowed from the group in a single round).

    Parameters
    ----------
    instance_data: InstanceData
        An `InstanceData` object representing the data for a load migration
        scheduling instance, on which the algorithm is run.

    Returns
    -------
    int
        An integer representing the number of rounds used by the algorithm
        to schedule the load migration instance specified by `instance_data`.

    """
    rounds = []
    num_rounds = 0
    controller_caps, qos_caps = utils.get_cap_dicts(instance_data)
    controller_consts, qos_consts = utils.get_constraint_dicts(instance_data)
    while controller_consts or qos_consts:
        bottleneck_constraint = get_bottleneck_constraint(
            controller_consts, qos_consts)
        switch = select_migration_from_constraint(bottleneck_constraint)
        migration = instance_data.get_migration(switch)
        schedule_round = find_scheduling_round(rounds, num_rounds, migration)
        if schedule_round == num_rounds:
            rounds.append(Round(num_rounds, controller_caps, qos_caps))
            num_rounds += 1
        rounds[schedule_round].schedule_migration(migration)
        controller_consts, qos_consts = remove_migration_from_constraints(
            migration)
    return num_rounds
