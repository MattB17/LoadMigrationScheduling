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


def get_bottleneck_constraint(constraints_dict):
    """The bottleneck constraint among the constraints of `constraints_dict`.

    The bottleneck constraint is the most loaded constraint among the
    constraints of `constraints_dict`.

    Parameters
    ----------
    constraints_dict: dict
        A dictionary of the constraints. The keys are strings representing
        the name of the constraint and the corresponding value is a
        `ConstraintDict` object representing the constraint.

    Returns
    -------
    str, ConstraintDict
        A string representing the name of a bottleneck constraint and the
        associated `ConstraintDict` object.

    """
    max_load = 0
    bottleneck_const = None
    bottleneck_const_name = None
    for const_name, const_dict in constraints_dict.items():
        load_factor = const_dict.get_load_factor()
        if not bottleneck_const or load_factor > max_load:
            max_load = load_factor
            bottleneck_const = const_dict
            bottleneck_const_name = const_name
    return bottleneck_const_name, bottleneck_const

def select_candidate_migrations(constraint_dict, num_candidates):
    """Selects `num_candidates` from `constraint_dict`.

    `num_candidates` migrations are selected from `constraint_dict` among
    all the migrations associated with the constraint.

    Parameters
    ----------
    constraint_dict: ConstraintDict
        The `ConstraintDict` object from which the migration is selected.
    num_candidates: int
        The number of candidate migrations to sample from `constraint_dict`
        among which a migration is chosen. A value of -1 indicates that all
        migrations are considered as candidates.

    Returns
    -------
    collection
        A collection of `Migration` objects representing the candidate
        migrations.

    """
    if (num_candidates == -1 or
        num_candidates >= len(constraint_dict.get_switches())):
        return constraint_dict.get_switches()
    else:
        return random.sample(constraint_dict.get_switches(), num_candidates)

def remove_migration_from_constraints(migration, consts_dict):
    """Removes `migration` from `consts_dict`.

    `consts_dict` is updated to reflect the removal of `migration`,
    signalling that the migration has been scheduled.

    Parameters
    ----------
    consts_dict: dict
        A dictionary of constraints. The keys are strings representing the
        names of the constraints and the corresponding value is a
        `ConstraintDict` object representing the constraint.

    Returns
    -------
    dict
        The dictionary obtained from `consts_dict` after removing
        `migration` from all the constraints involving the migration.

    """
    consts_dict[migration.get_dst_controller()].remove_switch(
        migration.get_switch(), migration.get_load())
    if not len(consts_dict[migration.get_dst_controller()].get_switches()):
        del consts_dict[migration.get_dst_controller()]
    for group in migration.get_groups():
        consts_dict[group].remove_switch(migration.get_switch(), 1)
        if not len(consts_dict[group].get_switches()):
            del consts_dict[group]
    return consts_dict


def schedule_migration_in_earliest_round(rounds, num_rounds, migration,
                                         controller_caps, qos_caps):
    """Schedules `migration` in the earliest round possible given `rounds`.

    `migration` is scheduled in the earliest round in `rounds` in which the
    migration fits. If it does not fit in any of the rounds, a new round is
    created and migration is scheduled in that round.

    Parameters
    ----------
    rounds: collection
        A collection of `Round` objects representing the rounds to which
        migrations have already been scheduled.
    num_rounds: int
        An integer representing the number of rounds in `existing_rounds`.
    migration: Migration
        A `Migration` object representing the migration to be scheduled.
    controller_caps: dict
        A dictionary of controller capacities. The keys are strings
        representing the names of the controllers and the corresponding value
        is a float representing the capacity for that controller.
    qos_caps: dict
        A dictionary of QoS group capacities. The keys are strings
        representing the names of the controllers and the corresponding value
        is an integer representing the capacity for that QoS group.

    Returns
    -------
    list, int
        A list obtained from `rounds` after scheduling migration in the
        first available round and an integer representing the number of
        active rounds.

    """
    round_count = num_rounds
    curr_rounds = [round for round in rounds]
    schedule_round = find_scheduling_round(rounds, round_count, migration)
    if schedule_round == round_count:
        curr_rounds.append(Round(round_count, controller_caps, qos_caps))
        round_count += 1
    curr_rounds[schedule_round].schedule_migration(migration)
    return curr_rounds, round_count


def calculate_migration_load(migration, exclude_const, consts_dict):
    """The load of `migration` from `consts_dict`, excluding `exclude_const`.

    The maximum load among the constraints of `consts_dict` to which
    `migration` is associated is calculated. The constraint with name
    `exclude_const` is ignored in the calculation.

    Parameters
    ----------
    migration: Migration
        The `Migration` object for which the load is calculated.
    exclude_const: str
        A string representing the name of the constraint excluded from the
        load calculation.
    consts_dict: dict
        A dictionary of constraints. The keys are strings representing the
        names of the constraints and the corresponding value is a
        `ConstraintDict` object for the constraint.

    """
    load = 0
    migration_consts = migration.get_groups().union(
        {migration.get_dst_controller()})
    for const_name in migration_consts:
        if const_name != exclude_const:
            load = max(load, consts_dict[const_name].get_load_factor())
    return load


def get_bottleneck_migration(migrations, bottleneck_const_name,
                             instance_data, consts_dict):
    """Selects the bottleneck migration among `migrations`.

    The bottleneck migration among `migrations` is the migration belonging
    to the constraint with the highest load among `consts_dict`, excluding
    the constraint for `bottleneck_const_name`.

    Parameters
    ----------
    migrations: collection
        A collection of strings representing the names of the switches for
        the set of migrations from which the bottleneck migration is chosen.
    bottleneck_const_name: str
        A string representing the name of the bottleneck constraint to which
        `migrations` are associated.
    instance_data: InstanceData
        An `InstanceData` object specifying the data for a load migration
        scheduling instance.
    consts_dict: dict
        A dictionary of the constraints. The keys are strings representing
        the names of the constraints and the corresponding value is a
        `ConstraintDict` object for that constraint.

    Returns
    -------
    Migration
        A `Migration` object representing the bottleneck migration chosen
        from `migrations`.

    """
    if isinstance(migrations, list) and len(migrations) == 1:
        return instance_data.get_migration(migrations[0])
    bottleneck_migration = None
    max_load = 0
    for migration_name in migrations:
        curr_migration = instance_data.get_migration(migration_name)
        curr_load = calculate_migration_load(
            curr_migration, bottleneck_const_name, consts_dict)
        if ((not bottleneck_migration) or (curr_load > max_load)):
            bottleneck_migration = curr_migration
            max_load = curr_load
    return bottleneck_migration


def select_bottleneck_migration(instance_data, num_candidates, consts_dict):
    """Selects a bottleneck migration from `consts_dict`.

    A migration is selected from a bottleneck constraint among
    `consts_dict`. `num_candidates` candidate migrations
    are considered in the bottleneck constraint and the best is chosen.

    Parameters
    ----------
    instance_data: InstanceData
        An `InstanceData` object specifying a load migration scheduling
        instance.
    num_candidates: int
        The number of candidate migrations to consider among the migrations
        of the bottleneck constraint. A value of -1 indicates that all
        migrations from the bottleneck constraint are considered.
    consts_dict: dict
        A dictionary of the constraints. The keys are strings representing
        the names of the constraints and the corresponding value is a
        `ConstraintDict` object for the constraint.

    Returns
    -------
    Migration
        A `Migration` object representing a migration associated with a
        bottleneck constraint among `consts_dict`.

    """
    const_name, const = get_bottleneck_constraint(consts_dict)
    candidate_migrations = select_candidate_migrations(const, num_candidates)
    return get_bottleneck_migration(
        candidate_migrations, const_name, instance_data, consts_dict)


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
        rounds, num_rounds = schedule_migration_in_earliest_round(
            rounds, num_rounds, migration, controller_caps, qos_caps)
    return num_rounds


def current_bottleneck_first(instance_data, num_choices):
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
    num_choices: int
        An integer denoting the number of candidate migrations considered
        when selecting a migration from the bottleneck constraint. The most
        loaded migration among the candidates will be selected. A value of
        -1 signifies to consider all migrations of the bottleneck constraint.

    Returns
    -------
    int
        An integer representing the number of rounds used by the algorithm
        to schedule the load migration instance specified by `instance_data`.

    """
    rounds = []
    num_rounds = 0
    controller_caps, qos_caps = utils.get_cap_dicts(instance_data)
    constraints_dict = utils.get_constraints_dict(instance_data)
    while constraints_dict:
        migration = select_bottleneck_migration(
            instance_data, num_choices, constraints_dict)
        rounds, num_rounds = schedule_migration_in_earliest_round(
            rounds, num_rounds, migration, controller_caps, qos_caps)
        constraints_dict = remove_migration_from_constraints(
            migration, constraints_dict)
    return num_rounds
