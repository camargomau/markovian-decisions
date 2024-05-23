import auxiliary.input_func as inp
from numpy import linalg
from prettytable import PrettyTable
import solve.enumeration as enumeration
from auxiliary.steady_state import calculate_policy_cost

# Para mejoramiento sin descuento, resolver los sistemas de ecuaciones
def solve_system_standard(process, current_policy):
    solve_equations = []
    solve_vector = []

    # Lado izquiredo de las ecuaciones y vector b
    for state in process.states:
        decision_in_state = current_policy[state]
        equation = []

        # los primeros m+1 elementos corresponden a los coeficientes de las V_j para todo estado (j = target_state)
        for target_state in process.states:
            if target_state == state:
                equation.append(process.transition[decision_in_state][state][target_state]-1)
            else:
                equation.append(process.transition[decision_in_state][state][target_state])

        # el último corresponde al coeficiente de g
        equation.append(-1)
        solve_equations.append(equation)
        # Los costos son escalares y van en b
        solve_vector.append(-process.costs[state][decision_in_state])

    # Se tiene la condición que la última V_m = 0
    v_m_zero = [0 for _ in process.states[:-1]] + [1, 0]
    solve_equations.append(v_m_zero)
    solve_vector.append(0)

    # Resolver el sistema con linalg.solve
    return linalg.solve(solve_equations, solve_vector)


# Para mejoramiento sin descuento, resolver los sistemas de ecuaciones
def solve_system_discounted(process, current_policy, discount):
    solve_equations = []
    solve_vector = []

    # Lado izquiredo de las ecuaciones y vector b
    for state in process.states:
        decision_in_state = current_policy[state]
        equation = []

        # los primeros m+1 elementos corresponden a los coeficientes de las V_j para todo estado (j = target_state)
        for target_state in process.states:
            if target_state == state:
                equation.append(discount*process.transition[decision_in_state][state][target_state]-1)
            else:
                equation.append(discount*process.transition[decision_in_state][state][target_state])

        solve_equations.append(equation)
        # Los costos son escalares y van en b
        solve_vector.append(-process.costs[state][decision_in_state])

    # Resolver el sistema con linalg.solve
    return linalg.solve(solve_equations, solve_vector)


# Encontrar una política alternativa sin descuento
def find_alternative_standard(process, system_solution):
    alt_policy = []

    # Definir la nueva decisión para cada estado
    for state in process.states:
        costs_to_compare = {}

        # Comparar un costo por cada decisión
        for decision in process.decisions:
            if process.decision_applicability[decision][state]:
                cost = process.costs[state][decision]
                for target_state in process.states:
                    if target_state == state:
                        cost += (process.transition[decision][state][target_state]-1)*system_solution[target_state]
                    else:
                        cost += (process.transition[decision][state][target_state])*system_solution[target_state]
                costs_to_compare[decision] = cost

        # La decisión óptima se guarda en un diccionario con el costo como valor y la decisión correspondiente como key
        optimal_decision = min(costs_to_compare, key=costs_to_compare.get)
        alt_policy.append(optimal_decision)

    return alt_policy


# Encontrar una política alternativa con descuento
def find_alternative_discounted(process, system_solution, discount):
    alt_policy = []

    # Definir la nueva decisión para cada estado
    for state in process.states:
        costs_to_compare = {}

        # Comparar un costo por cada decisión
        for decision in process.decisions:
            if process.decision_applicability[decision][state]:
                cost = process.costs[state][decision]
                for target_state in process.states:
                    cost += (discount*process.transition[decision][state][target_state])*system_solution[target_state]
                costs_to_compare[decision] = cost

        # La decisión óptima se guarda en un diccionario con el costo como valor y la decisión correspondiente como key
        optimal_decision = min(costs_to_compare, key=costs_to_compare.get)
        alt_policy.append(optimal_decision)

    return alt_policy


def improve(iter, process, current_policy, discount):
    if discount is None:
        system_solution = solve_system_standard(process, current_policy)

        row = [iter] + [round(value, 6) for value in system_solution] + [current_policy, round(system_solution[-1], 6)]
        table.add_row(row)

        alt_policy = find_alternative_standard(process, system_solution)

        if alt_policy == current_policy:
            row = [iter+1] + ["N/A" for _ in range(len(process.states)+1)] + [current_policy, round(system_solution[-1], 6)]
            table.add_row(row)
            return alt_policy
        else:
            return improve(iter+1, process, alt_policy, discount)
    else:
        # current_cost = calculate_policy_cost(process, current_policy)


        system_solution = solve_system_discounted(process, current_policy, discount)

        state = 0
        decision = current_policy[state]
        current_cost = process.costs[state][decision]
        for target_state in process.states:
            if target_state == state:
                current_cost += discount*process.transition[decision][state][target_state]*system_solution[target_state]-1
            else:
                current_cost += discount*process.transition[decision][state][target_state]*system_solution[target_state]

        row = [iter] + [round(value, 6) for value in system_solution] + [current_policy, round(current_cost, 6)]
        table.add_row(row)

        alt_policy = find_alternative_discounted(process, system_solution, discount)

        if alt_policy == current_policy:
            row = [iter+1] + ["N/A" for _ in range(len(process.states))] + [current_policy, round(current_cost, 6)]
            table.add_row(row)
            return alt_policy
        else:
            return improve(iter+1, process, alt_policy, discount)


def main(process, discounted):
    print("Mejoramiento de políticas con descuento\n" if discounted else "Mejoramiento de políticas\n")

    # Solicitar la política inicial
    initial_policy = inp.number("• Introduzca la política inicial (separe con comas): ", min_value=1, max_value=process.decisions[-1], size=len(process.states))

    # Tabla donde ir agregando los resultados de cada iteración
    global table
    table = PrettyTable()
    if not discounted:
        field_names = ["iter."] + [f"V{i}" for i in process.states] + ["g", "Política", "Costo"]
    else:
        field_names = ["iter."] + [f"V{i}" for i in process.states] + ["Política", "Costo"]
    table.field_names = field_names


    discount = None
    if discounted:
        discount = inp.number("• Introduzca el descuento (del 0 al 1): ", number_type="f", min_value=0, max_value=1)

    optimal_policy = improve(1, process, initial_policy, discount)

    print(table)
    input()
