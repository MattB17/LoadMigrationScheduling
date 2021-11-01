#!/usr/bin/env python3.6

"""Solve a multi-commodity flow problem. Two product ('Pencils' and 'Pens')
are produced in 2 cities ('Detroit' and 'Denver') and must be sent to
warehouses in 3 cities ('Boston', 'New York', and 'Seattle') to satisfy demand
(`inflow[h, i]`).

Flows on the transportation network must respect arc capacity constrains
(`capacity[i, j]`). The objective is to minimize the sum of the arc
transportation costs (`cost[i, j]`).

"""
import gurobipy as gp
from gurobipy import GRB

# Setting up graph
commodities = ['Pencils', 'Pens']
nodes = ['Detroit', 'Denver', 'Boston', 'New York', 'Seattle']
arcs, capacity = gp.multidict({('Detroit', 'Boston'): 100,
                               ('Detroit', 'New York'): 80,
                               ('Detroit', 'Seattle'): 120,
                               ('Denver', 'Boston'): 120,
                               ('Denver', 'New York'): 120,
                               ('Denver', 'Seattle'): 120})

# costs to send commodity from source to destination.
cost = {('Pencils', 'Detroit', 'Boston'): 10,
        ('Pencils', 'Detroit', 'New York'): 20,
        ('Pencils', 'Detroit', 'Seattle'): 60,
        ('Pencils', 'Denver', 'Boston'): 40,
        ('Pencils', 'Denver', 'New York'): 40,
        ('Pencils', 'Denver', 'Seattle'): 30,
        ('Pens', 'Detroit', 'Boston'): 20,
        ('Pens', 'Detroit', 'New York'): 20,
        ('Pens', 'Detroit', 'Seattle'): 90,
        ('Pens', 'Denver', 'Boston'): 60,
        ('Pens', 'Denver', 'New York'): 70,
        ('Pens', 'Denver', 'Seattle'): 30}

# city demands for the commodities
inflow = {('Pencils', 'Detroit'): 50,
          ('Pencils', 'Denver'): 60,
          ('Pencils', 'Boston'): -50,
          ('Pencils', 'New York'): -50,
          ('Pencils', 'Seattle'): -10,
          ('Pens', 'Detroit'): 60,
          ('Pens', 'Denver'): 40,
          ('Pens', 'Boston'): -40,
          ('Pens', 'New York'): -30,
          ('Pens', 'Seattle'): -30}

# create optimization model
m = gp.Model('netflow')

# create variables
flow = m.addVars(commodities, arcs, obj=cost, name='flow')

# arc-capacity constraints
# the sum of flows on an arc must be less than the capacity of that arc
m.addConstrs((flow.sum('*', i, j) <= capacity[i, j] for i, j in arcs), 'cap')

# could also do
# for i, j in arcs:
#   m.addConstr(sum(flow[h, i, j] for h in commodities) <= capacity[i, j],
#               "cap[{0}, {1}]".format(i, j))
#
# ie. loop over every arc and sum all commodities on arc

# flow-conservation constraints
# sum of flow in plus demand equals sum of flow out
m.addConstrs((flow.sum(h, '*', j) + inflow[h, j] == flow.sum(h, j, '*')
                for h in commodities for j in nodes), 'node')

m.optimize()

if m.status == GRB.OPTIMAL:
    solution = m.getAttr('x', flow)
    for h in commodities:
        print('\nOptimal flows for {}:'.format(h))
        for i, j in arcs:
            if solution[h, i, j] > 0:
                print("{0} -> {1}: {2}".format(i, j, solution[h, i, j]))
