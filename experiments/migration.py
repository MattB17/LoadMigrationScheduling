"""Solve a load migrations scheduling instance.

"""
import gurobipy as gp
from gurobipy import GRB

# indices of network objects
switch_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
round_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
controller_ids = [0, 1, 2, 3, 4]
group_ids = [0, 1, 2, 3]

# switch loads
loads = {i: 1 for i in range(10)}

# controller capacities
controller_caps = {i: 1 for i in range(5)}

# group capacities
group_caps = {i: 1 for i in range(4)}

# switches migrating to each destination controller
dst_controllers = {0: {2},
                   1: {0, 7},
                   2: {3, 4},
                   3: {5, 6, 8},
                   4: {1, 9}}

# group membership
groups = {0: {0, 1, 5, 8},
          1: {1, 4, 7},
          2: {3, 6},
          3: {2, 3}}

m = gp.Model('migration')

x_vars = m.addVars(switch_ids, round_ids, vtype=GRB.BINARY, name="x")
lambda_var = m.addVar(name="lambda")

m.addConstrs((x_vars.sum(i, '*') == 1 for i in switch_ids), 'migrate')

m.addConstrs((r * x_vars[i, r] <= lambda_var
              for i in switch_ids for r in round_ids), "bounds")

m.optimize()

if m.status == GRB.OPTIMAL:
    print('Objective value: {0}'.format(m.objVal))
