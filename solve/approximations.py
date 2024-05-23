import auxiliary.input_functions as inp
from prettytable import PrettyTable


def find_v_policy(iter, process, discount, previous_v):
    v_vect = []
    # Esta política óptima corresponde a la iteración; NO es la global
    optimal_policy = []

    # Se obtiene una V por cada estado
    for state in process.states:
        # En la iteración 1 se comparan nada más los costos viables en cada estado
        if iter == 1:
            to_compare = {decision: cost for decision, cost in enumerate(
                process.costs[state]) if cost is not None}
        # En cualquier otra iteración se comparan sumas
        else:
            to_compare = {}
            # Comparar un costo por cada decisión
            for decision in process.decisions:
                if process.decision_applicability[decision][state]:
                    cost = process.costs[state][decision]

                    for target_state in process.states:
                        cost += (discount*process.transition[decision][state]
                                 [target_state])*previous_v[target_state]

                    to_compare[decision] = cost

        # La decisión óptima se guarda en un diccionario con la cifra como valor y la decisión correspondiente como key
        optimal_decision = min(to_compare, key=to_compare.get)
        optimal_policy.append(optimal_decision)
        # Se guarda la cifra como el v correspondiente al estado
        v_vect.append(to_compare[optimal_decision])

    return v_vect, optimal_policy


def successive(process, discount, max_iter, tol):
    iter = 1
    previous_v = None

    while iter <= max_iter:
        current_v, current_policy = find_v_policy(
            iter, process, discount, previous_v)

        # Agregar el renglón para la iteración actual
        row = [iter] + [round(v, 6) for v in current_v] + [current_policy]
        table.add_row(row)

        if iter != 1:
            # Detener si estamos dentro de la tolerancia para todo estado
            all_within_tolerance = all(
                abs(v - previous_v[i]) < tol for i, v in enumerate(current_v))
            if all_within_tolerance:
                return current_policy, True

        previous_v = current_v
        iter += 1

    return current_policy, False


def main(process):
    # Tabla donde ir agregando los resultados de cada iteración
    global table
    table = PrettyTable()
    field_names = ["iter."] + [f"V{i}" for i in process.states] + ["Política"]
    table.field_names = field_names

    discount = inp.number("• Introduzca el descuento (del 0 al 1): ",
                          number_type="f", min_value=0, max_value=1)

    max_iter = inp.number("• Introduzca el número máximo de iteraciones: ",
                          min_value=1)

    tol = inp.number("• Introduzca la tolerancia: ",
                     number_type="f", min_value=0)

    # Obtener una _aproximación_ a la política óptima
    approximated_optimal_policy, within_tolerance = successive(
        process, discount, max_iter, tol)

    print(f"\n{table}")

    print("\n(tolerancia alcanzada)") if within_tolerance else print(
        "\n(número máximo de iteraciones alcanzado)")
    print(f"\nLa aproximación obtenida a la política óptima es {
          approximated_optimal_policy}")

    input("\nPresione enter para regresar el menú de métodos.")
