import pandas as pd
import gurobipy as gb
import numpy as np
import matplotlib.pyplot as plt
import math


df = pd.DataFrame(pd.read_excel(r'sample_data.xlsx', 'patients'))
df_n = pd.DataFrame(pd.read_excel(r'sample_data.xlsx', 'nurses'))
df


'''number of nurses, patients, days, frequency of visit, service duration & qualification'''
m = 3  # number of nurses
t = 5  # number of days in planning horizon
n = df.shape[0] - 1  # number of patients
f = list(df["f"][1:].astype('int'))  # frequency of visit for every patients
et = list(df["et"].astype('int'))
lt = list(df["lt"].astype('int'))
sd = list(df["sd"].astype('int'))
q = list(df["Q'"][1:].astype('int'))
Q = list(df_n["Q"].astype('int'))


''' coordinates X and Y of each patient and depot'''
X, Y = list(df["x"]), list(df["y"])
depot = [X[0], Y[0]]


'''distance grid'''


def dist(x=[], y=[]):
    dist_grid = np.empty([len(x), len(y)])
    for i in range(len(x)):
        for j in range(len(y)):
            if i == j:
                dist_grid[i, j] = 1000
            else:
                dist_grid[i, j] = math.sqrt(
                    (x[i] - x[j])**2 + (y[i] - y[j])**2)
    return dist_grid


grid = dist(X, Y)
grid


'''Initialize the model'''
M = gb.Model("master_problem")


''' decision variable: delta '''
d = {}
for i in range(n):
    d[i] = M.addVar(vtype=gb.GRB.BINARY, name="d%d" % (i))
M.update()


'''decision variable x'''
x = {}
for i in range(m):
    for j in range(n):
        x[i, j] = M.addVar(vtype=gb.GRB.BINARY, name='x%d,%d' % (i, j))
M.update()


'''decision variable y'''
y = {}
for i in range(m):
    for j in range(n + 1):  # +1 is for depot
        for k in range(t):
            y[i, j, k] = M.addVar(vtype=gb.GRB.BINARY,
                                  name='y%d,%d,%d' % (i, j, k))
M.update()


'''variable z'''
z = {}
for i in range(m):
    for j in range(n + 1):
        for l in range(n + 1):
            for k in range(t):
                z[i, j, l, k] = M.addVar(
                    vtype=gb.GRB.BINARY, name="z%d,%d,%d,%d" % (i, j, l, k))
M.update()


'''variable s'''
s = {}
for i in range(m):
    for j in range(n + 1):
        for k in range(t):
            s[i, j, k] = M.addVar(vtype=gb.GRB.CONTINUOUS,
                                  name="s%d,%d,%d" % (i, j, k))
M.update()


'''objective funtion - 1'''
M.setObjective(gb.quicksum(d[j] for j in range(n)), gb.GRB.MAXIMIZE)
M.update()


'''constraint 2'''
for j in range(n):
    M.addConstr(gb.quicksum(x[i, j] for i in range(m)) == d[j])
M.update()


'''constraint 2'''
for j in range(n):
    M.addConstr(gb.quicksum(gb.quicksum(
        y[i, j + 1, k] for k in range(t)) for i in range(m)) == f[j] * d[j])
M.update()


'''constraint 3'''
for i in range(m):
    for j in range(n):
        for k in range(t):
            M.addConstr(y[i, j + 1, k] <= x[i, j])
M.update()


'''constraint 4'''
for i in range(m):
    for j in range(n):
        if q[j] != Q[i]:
            M.addConstr(x[i, j] == 0)
M.update()


'''constraint 5'''
for i in range(m):
    for k in range(t):
        M.addConstr(y[i, 0, k] == 1)  # j = n for depot location
        M.addConstr(y[i, 0, k] == 1)
M.update()


'''constraint 6'''
for i in range(m):
    for j in range(n):
        for k in range(t):
            for p in range(1, (4 - (f[j]) + 1)):
                if (k + p) <= 4:
                    M.addConstr(y[i, j + 1, k] + y[i, j + 1, k + p] <= 1)
M.update()

'''run optimizer'''
M.optimize()


'''print solution'''
solution_d, solution_x, solution_y = M.getAttr('x', d), M.getAttr('x', x), M.getAttr('x', y)
var_d, var_x, var_y = np.empty([n]), np.empty([m,n]), np.empty([m,n,t])
for i in range(m):
    for j in range(n):
        var_d[j] = solution_d[j]
        var_x[i,j] = solution_x[i,j]
for i in range(m):
    for j in range(n):
        for k in range(t):
            var_y[i,j,k] = solution_y[i,j,k]
print('\nnodes\n',df.head(), '\nnurses\n',df_n.head(),'\nobj\n',int(M.objVal),\
'\nq\n',q,'\nf\n',f,'\nd\n',var_d, '\nx\n', var_x, '\ny\n',var_y)
