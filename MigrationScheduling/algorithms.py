"""This module implements the heuristic algorithms used to solve the
load migration scheduling problem.

"""
from MigrationScheduling import utils


def vector_first_fit(instance_data):
    rounds = []
    num_rounds = 0
    controller_caps, qos_caps = utils.get_cap_dicts(instance_data)
    for migration in instance_data.get_migrations():
        schedule_round = 0
        while schedule_round < num_rounds:
            if rounds[schedule_round].can_schedule_migration(migration):
                rounds[schedule_round].schedule_migration(migration)
                break
            schedule_round += 1
        if schedule_round == num_rounds
        rounds.append(Round(controller_caps, qos_caps))
        num_rounds += 1
        rounds[schedule_round].schedule_migration(migration)
    return num_rounds
