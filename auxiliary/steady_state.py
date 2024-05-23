from numpy import linalg


def solve(process, policy):
    """
    Solves for the steady state distributions given a process
    and a specific policy
    """
    # Matriz resultanto de la política, obtenida luego de combinar columnas
    # de las matrices de transición correspondientes a cada decisión
    spliced_matrix = [process.transition[decision][origin_state]
                      for origin_state, decision in enumerate(policy)]

    # Matriz correspondiente a los coeficentes del lado izquierdo de las ecuaciones
    solve_equations = []
    for state in process.states[:-1]:
        solve_equations.append([spliced_matrix[origin_state][state] if origin_state !=
                               state else spliced_matrix[origin_state][state]-1 for origin_state in process.states])
    solve_equations.append([1 for _ in process.states])

    # Lado derecho de las ecuaciones
    solve_vector = [0 for _ in process.states[:-1]] + [1]

    # Resolver con numpy.linalg.solve
    return linalg.solve(solve_equations, solve_vector)

def calculate_policy_cost(process, policy):
    steady_state = solve(process, policy)

    total_cost = 0
    for state in process.states:
        cost = process.costs[state][policy[state]]
        total_cost += cost * \
            steady_state[state]

    return total_cost
