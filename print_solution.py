import numpy as np


def printSolution(M, solution_d, solution_x, solution_y, m, n, t, df, df_n, q, f):
    var_d, var_x, var_y = np.empty([n]), np.empty([m, n]), np.empty([m, n + 1, t])
    for i in range(m):
        for j in range(n):
            var_d[j] = solution_d[j]
            var_x[i, j] = solution_x[i, j]
    for i in range(m):
        for j in range(n + 1):
            for k in range(t):
                var_y[i, j, k] = solution_y[i, j, k]
    print('\nnodes\n', df.head(),'\nnurses\n', df_n.head())
    np.set_printoptions(formatter={'float': '{: 0.0f}'.format})
    print(
          '\nq\n', q,
          '\nf\n', f,
          '\nd\n', var_d,
          '\nx\n', var_x,
          '\ny\n', var_y,
          '\nobj\n', int(M.objVal)
          )
