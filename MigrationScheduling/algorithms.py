"""This module implements the heuristic algorithms used to solve the
load migration scheduling problem.

"""
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
