from scipy import optimize


def solve_linear_prog(process):
    # decision amount
    dcn_amnt = len(process.decisions)

    # Para la función objetivo
    # \sum_{i=0}^{m} \sum_{k=1}^{K} c_{ik} y_{ik}
    costs = []
    for state in process.states:
        for cost in process.costs[state][1:]:
            costs.append(cost if cost is not None else float(0))

    # Para las restricciones explícitas
    # Restricciones para cada estado
    # j = 0, 1, …, m
    constraints = [[0 for _ in costs] for _ in process.states]
    for state in process.states:
        # Suma de las y de tomar la decisión k en el estado j
        # \sum_{k=1}^{K} y_{jk}
        for decision in process.decisions:
            constraints[state][dcn_amnt*state + decision -
                               1] += 1 if process.decision_applicability[decision][state] else 0
        # Suma ponderada de las y de tomar la decisión k en algún estado i anterior a j
        # \sum_{i=0}^{m} \sum_{k=1}^{K} y_{ik} p_{ij}(k)
        for origin_state in process.states:
            for decision in process.decisions:
                if process.transition[decision][origin_state] is not None:
                    constraints[state][dcn_amnt*origin_state + decision -
                                       1] -= process.transition[decision][origin_state][state]

    # Restricción de suma igual a 1 para todas las decisiones aplicables
    # \sum_{i=0}^{m} \sum_{k=1}^{K} y_{ik}
    one_constraint = [0 for _ in costs]
    for state in process.states:
        for decision in process.decisions:
            if process.decision_applicability[decision][state]:
                one_constraint[dcn_amnt*state + decision-1] = 1

    # Unión de todas las restricciones explícitas
    constraints.insert(0, one_constraint)

    # Vector b
    constraint_vector = [1] + [0 for _ in process.states]

    # Resolución del PPL mediante scipy.optimize.linprog, que utiliza HiGHS
    solved = optimize.linprog(
        c=costs, A_eq=constraints, b_eq=constraint_vector)

    # Falta binarizar los valores de solved.x dividéndolos entre \sum_{k=1}^{K} y_ik
    # solved.fun es Z óptima
    return solved.x, solved.fun