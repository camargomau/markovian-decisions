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
    solution = optimize.linprog(
        c=costs, A_eq=constraints, b_eq=constraint_vector)

    return solution


def interpret_linear_sol(process, raw_solution):
    dcn_amnt = len(process.decisions)

    # optimize.linprog retorna un objeto cuyo atributo x es el vector solución
    raw_sol_vector = raw_solution.x
    # Separar el vector solución en una matriz para un manejo simplificado de índices
    raw_sol_matrix = [raw_sol_vector[dcn_amnt*state:dcn_amnt*(state+1)] for state in process.states]

    # Sumar las soluciones para cada estado (renglón)
    row_sum = [0 for _ in process.states]
    for state in process.states:
        for value in raw_sol_matrix[state]:
            row_sum[state] += value

    # Binarizar la solución dividiendo entre \sum_{k=1}^{K} y_ik
    binary_sol = [[raw_sol_matrix[state][decision]/row_sum[state] for decision in range(dcn_amnt)] for state in process.states]

    # La política óptima es la decisión con 1 para cada estado
    optimal_policy = [binary_sol[state].index(float(1))+1 for state in process.states]
    optimal_cost = 0
    for state in process.states:
        for decision in process.decisions:
            # Sumar los costos de las decisiones óptimas
            if optimal_policy[state] == decision:
                optimal_cost += process.costs[state][decision]

    return optimal_policy, optimal_cost
