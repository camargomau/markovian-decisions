from numpy import linalg
from prettytable import PrettyTable


def solve_steady_state(process, policy):
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


def calculate_costs(process):
    """
    Calculates the costs for all policies of a process
    """
    # Generar todas las políticas viables
    process.generate_policies()

    # Lista de listas que guardan las probabilidades de estado estable
    steady_state_probs = []
    # Lista de costos esperados para cada política
    expected_costs = [0 for _ in process.policies]

    for policy_i, policy in enumerate(process.policies):
        # Obtener las soluciones a las probabilidades de estado estable para cada política
        steady_state_probs.append(solve_steady_state(process, policy))
        # Calcular el costo esperado para cada política
        for state in process.states:
            cost = process.costs[state][policy[state]]
            if cost is not None:
                expected_costs[policy_i] += cost * \
                    steady_state_probs[policy_i][state]

    return expected_costs


def print_policies_costs(process, optimal_policy, expected_costs):
    table = PrettyTable()
    # Encabezado
    table.field_names = ["", "Política", "Costo", "Óptima"]
    # i, política, costo, (óptima)
    for policy_i, policy in enumerate(process.policies):
        if policy == optimal_policy:
            table.add_row([policy_i, policy, round(
                expected_costs[policy_i], 6), "Óptima"])
        else:
            table.add_row([policy_i, policy, round(
                expected_costs[policy_i], 6), ""])

    print(table)


def main(process):
    expected_costs = calculate_costs(process)

    optimal_cost = min(expected_costs)
    optimal_policy = process.policies[expected_costs.index(optimal_cost)]

    print("Enumeración Exhaustiva\n")
    print_policies_costs(process, optimal_policy, expected_costs)

    print(f"\nLa política óptima es R{process.policies.index(optimal_policy)} {
          optimal_policy} con un costo de {round(optimal_cost, 6)}")

    input("\nPresione cualquier tecla para regresar el menú de métodos.")
