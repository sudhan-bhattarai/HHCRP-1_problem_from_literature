'''objective funtion - 1'''
def objectiveFunction(M,gb,d,n):
    M.setObjective(gb.quicksum(d[j] for j in range(n)), gb.GRB.MAXIMIZE)
    M.update()
