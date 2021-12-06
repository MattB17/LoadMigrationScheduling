import os
import gurobipy as gp
from gurobipy import GRB
from MigrationScheduling import algorithms
from MigrationScheduling.Model import Optimizer

DIR = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# indices of network objects
SWITCH_IDS = [0, 1, 2, 3, 4]
ROUND_IDS = [0, 1, 2, 3, 4]
CONTROLLER_IDS = [0, 2, 3]
GROUP_IDS = [0, 2]

# switch loads
LOADS = {0: 354.32, 1: 334.94, 2: 36.31, 3: 14.9, 4: 73.56}

# controller capacities
CONTROLLER_CAPS = {0: 354.32, 2: 14.9, 3: 810.15}

# group capacities
GROUP_CAPS = {0: 1, 2: 1}

# switches migrating to each destination controller
DST_CONTROLLERS = {0: {0}, 2: {3}, 3: {1, 2, 4}}

# group membership
GROUPS = {0: {2, 3}, 2: {3}}

def test_optimizer():
    # direct modelling
    m = gp.Model('test-migration')
    x_vars = m.addVars(SWITCH_IDS, ROUND_IDS, vtype=GRB.BINARY, name="x")
    lambda_var = m.addVar(name="lambda")
    m.setObjective(lambda_var, GRB.MINIMIZE)
    m.addConstrs((x_vars.sum(i, '*') == 1 for i in SWITCH_IDS), 'migrate')
    m.addConstrs((r * x_vars[i, r] <= lambda_var
                  for i in SWITCH_IDS for r in ROUND_IDS), "bounds")
    m.addConstrs((sum(LOADS[i] * x_vars[i, r] for i in DST_CONTROLLERS[j])
                  <= CONTROLLER_CAPS[j]
                  for j in CONTROLLER_IDS for r in ROUND_IDS),
                  "controller_cap")
    m.addConstrs((sum(x_vars[i, r] for i in GROUPS[l]) <= GROUP_CAPS[l]
                  for l in GROUP_IDS for r in ROUND_IDS),
                  "group_cap")
    m.optimize()

    # optimizer
    optimizer = Optimizer()
    optimizer.get_model_data(os.path.join(DIR,
        os.path.join("instances", "migrations1.txt")))
    optVal = optimizer.build_ip_model(verbose=False)
    assert round(optVal, 2) == round(m.objVal, 2)

def test_vff_heuristic():
    optimizer = Optimizer()
    optimizer.get_model_data(os.path.join(DIR,
        os.path.join("instances", "migrations1.txt")))
    vff_val = algorithms.vector_first_fit(optimizer.instance_data())

    # vff solution value is 2:
    # - migrations 0, 1, 2, and 4 are scheduled in round 1
    # - migration 3 is scheduled in round 2
    assert vff_val == 2
