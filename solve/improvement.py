import auxiliary.input_func as inp
from numpy import linalg
from prettytable import PrettyTable


# Resolver los sistemas de ecuaciones de las V_j (y g, sin descuento)
def solve_system(process, current_policy):
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

        # En el método estándar, g (costo a largo plazo) está en el sistema
        if discount == 1:
            # el último corresponde al coeficiente de g
            equation.append(-1)

        solve_equations.append(equation)
        # Los costos son escalares y van en b
        solve_vector.append(-process.costs[state][decision_in_state])

    # En el método estándar, se tiene la condición de que la última V_m = 0
    if discount == 1:
        v_m_zero = [0 for _ in process.states[:-1]] + [1, 0]
        solve_equations.append(v_m_zero)
        solve_vector.append(0)

    # Resolver el sistema con linalg.solve
    return linalg.solve(solve_equations, solve_vector)


# Encontrar una política alternativa
def find_alt_policy(process, system_solution):
    alt_policy = []

    # Definir la nueva decisión para cada estado
    for state in process.states:
        costs_to_compare = {}

        # Comparar un costo por cada decisión
        for decision in process.decisions:
            if process.decision_applicability[decision][state]:
                cost = process.costs[state][decision]

                for target_state in process.states:
                    # Sin descuento se suma -V_i
                    if discount == 1:
                        if target_state == state:
                            cost += (process.transition[decision][state][target_state]-1)*system_solution[target_state]
                        else:
                            cost += (process.transition[decision][state][target_state])*system_solution[target_state]
                    else:
                        cost += (discount*process.transition[decision][state][target_state])*system_solution[target_state]

                costs_to_compare[decision] = cost

        # La decisión óptima se guarda en un diccionario con el costo como valor y la decisión correspondiente como key
        optimal_decision = min(costs_to_compare, key=costs_to_compare.get)
        alt_policy.append(optimal_decision)

    return alt_policy


# Llevar el funcionamiento del método; resolver sistema, mejorar si es necesario, etc.
def improve(iter, process, current_policy):
    # Resolver el sistema de las V_j (y g, sin descuento)
    system_solution = solve_system(process, current_policy)

    # Agregar el renglón para la iteración actual
    row = [iter] + [round(value, 6) for value in system_solution] + [current_policy]
    table.add_row(row)

    # Encontrar una política alternativa a partir de los resultados
    alt_policy = find_alt_policy(process, system_solution)

    # Si la política alternativa es distinta a la actual, continuar
    if alt_policy != current_policy:
        return improve(iter+1, process, alt_policy)

    # Si son iguales, entonces terminar
    # Cuando es sin descuento, se imprime también g (costo a largo plazo)
    if discount == 1:
            row = [iter+1] + ["N/A" for _ in process.states] + [round(system_solution[-1], 6), current_policy]
    else:
        if alt_policy == current_policy:
            row = [iter+1] + ["N/A" for _ in process.states] + [current_policy]

    table.add_row(row)
    return alt_policy


def main(process, discounted):
    print("Mejoramiento de políticas con descuento\n" if discounted else "Mejoramiento de políticas\n")

    # Solicitar la política inicial
    initial_policy = inp.number("• Introduzca la política inicial (separe con comas): ", min_value=1, max_value=process.decisions[-1], size=len(process.states))

    # discount es 1 si se eligió el método estándar
    global discount
    discount = 1
    if discounted:
        discount = inp.number("• Introduzca el descuento (del 0 al 1): ", number_type="f", min_value=0, max_value=1)
        if discount == 1:
            print("\n(descuento de 1: utilizando mejoramiento sin descuento)")

    # Tabla donde ir agregando los resultados de cada iteración
    global table
    table = PrettyTable()
    field_names = ["iter."] + [f"V{i}" for i in process.states] + (["g (costo)"] if discount == 1 else []) + ["Política"]
    table.field_names = field_names

    optimal_policy = improve(1, process, initial_policy)

    print(f"\n{table}")
    print(f"\nLa política óptima es {optimal_policy}.")

    input("\nPresione cualquier tecla para regresar el menú de métodos.")
