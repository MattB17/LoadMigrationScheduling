import os
import gurobipy as gp
from gurobipy import GRB
from MigrationScheduling import algorithms
from MigrationScheduling.Model import Optimizer

DIR = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# indices of network objects
SWITCH_IDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
ROUND_IDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
CONTROLLER_IDS = [0, 1, 2]
GROUP_IDS = [0, 1, 2, 3, 4, 5]

# switch loads
LOADS = {0: 5.19,
         1: 2.15,
         2: 13.19,
         3: 1.7,
         4: 1.71,
         5: 3.46,
         6: 0.48,
         7: 0.99,
         8: 1.1,
         9: 11.77}

# controller capacities
CONTROLLER_CAPS = {0: 20.00, 1: 17.27, 2: 35.27}

# group capacities
GROUP_CAPS = {0: 2, 1: 3, 2: 1, 3: 1, 4: 1, 5: 2}

# switches migrating from each source controller
SRC_CONTROLLERS = {0: {3, 6},
                   1: {9},
                   2: {0, 1, 2, 4, 5, 7, 8}}

# switches migrating to each destination controller
DST_CONTROLLERS = {0: {0, 1, 2, 4},
                   1: {5, 6, 7, 8},
                   2: {3, 9}}

# group membership
GROUPS = {0: {0, 2, 3, 7},
          1: {0, 3, 7, 9},
          2: {0},
          3: {2},
          4: {0, 2},
          5: {0, 1, 3}}


def test_optimizer_without_resiliency():
    # direct modelling
    m = gp.Model('test-migration')
    x_vars = m.addVars(SWITCH_IDS, ROUND_IDS, vtype=GRB.BINARY, name="x")
    lambda_var = m.addVar(name="lambda")
    m.setObjective(lambda_var, GRB.MINIMIZE)
    m.addConstrs((x_vars.sum(i, '*') == 1 for i in SWITCH_IDS), "migrate")
    m.addConstrs((r * x_vars[i, r] <= lambda_var
                  for i in SWITCH_IDS for r in ROUND_IDS), "bounds")
    m.addConstrs((sum(LOADS[i] * x_vars[i, r] for i in DST_CONTROLLERS[j])
                  <= CONTROLLER_CAPS[j]
                  for j in CONTROLLER_IDS for r in ROUND_IDS
                  if len(DST_CONTROLLERS[j]) > 0),
                 "controller_cap")
    m.addConstrs((sum(x_vars[i, r] for i in GROUPS[l]) <= GROUP_CAPS[l]
                  for l in GROUP_IDS for r in ROUND_IDS),
                 "group_cap")
    m.optimize()

    # optimizer
    optimizer = Optimizer()
    optimizer.get_model_data(os.path.join(DIR,
        os.path.join("instances", "migrations2.txt")))
    optVal = optimizer.build_ip_model(resiliency=False, verbose=False)
    assert round(optVal, 2) == round(m.objVal, 2)

def test_optimizer_with_resiliency():
    # direct modelling
    m = gp.Model('test-migration')
    x_vars = m.addVars(SWITCH_IDS, ROUND_IDS, vtype=GRB.BINARY, name="x")
    lambda_var = m.addVar(name="lambda")
    m.setObjective(lambda_var, GRB.MINIMIZE)
    m.addConstrs((x_vars.sum(i, '*') == 1 for i in SWITCH_IDS), "migrate")
    m.addConstrs((r * x_vars[i, r] <= lambda_var
                  for i in SWITCH_IDS for r in ROUND_IDS), "bounds")
    m.addConstrs((sum(LOADS[i] * x_vars[i, r]
                  for i in SRC_CONTROLLERS[j].union(DST_CONTROLLERS[j]))
                  <= CONTROLLER_CAPS[j]
                  for j in CONTROLLER_IDS for r in ROUND_IDS
                  if (len(SRC_CONTROLLERS[j]) > 0 or
                      len(DST_CONTROLLERS[j]) > 0)),
                  "controller_cap")
    m.addConstrs((sum(x_vars[i, r] for i in GROUPS[l]) <= GROUP_CAPS[l]
                  for l in GROUP_IDS for r in ROUND_IDS),
                 "group_cap")
    m.optimize()

    # optimizer
    optimizer = Optimizer()
    optimizer.get_model_data(os.path.join(DIR,
        os.path.join("instances", "migrations2.txt")))
    optVal = optimizer.build_ip_model(resiliency=True, verbose=False)
    assert round(optVal, 2) == round(m.objVal, 2)

def test_vff_heuristic():
    optimizer = Optimizer()
    optimizer.get_model_data(os.path.join(DIR,
        os.path.join("instances", "migrations2.txt")))
    vff_val = algorithms.vector_first_fit(optimizer.instance_data())

    # the VFF solution has value 2:
    # - migrations 0, 1, 4, 5, 6, 7, 8, 9 are scheduled in round 1
    # - migrations 2 and 3 are scheduled in round 2
    assert vff_val == 2
