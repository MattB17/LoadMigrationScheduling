"""This module implements the heuristic algorithms used to solve the
load migration scheduling problem.

"""
from MigrationScheduling import utils
from MigrationScheduling.Model import Round


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
        schedule_round = 0
        while schedule_round < num_rounds:
            if rounds[schedule_round].can_schedule_migration(migration):
                rounds[schedule_round].schedule_migration(migration)
                break
            schedule_round += 1
        if schedule_round == num_rounds:
            rounds.append(Round(num_rounds, controller_caps, qos_caps))
            num_rounds += 1
            rounds[schedule_round].schedule_migration(migration)
    return num_rounds
