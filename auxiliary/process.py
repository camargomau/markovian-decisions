import auxiliary.input_functions as inp
from itertools import product
from prettytable import PrettyTable


class Process:
    """
    Class for a Markovian decision process, with states, decisions, costs, etc.
    """

    def __init__(self, states, decisions, decision_applicability, costs, transition):
        # Listas con los números de estados y decisiones
        # Estados inicia en 0, decisiones en 1
        self.states = states
        self.decisions = decisions

        # Lista de listas binarias que indican si una decisión es aplicable en un estado en concreto
        # decision_applicability[decision][state]
        self.decision_applicability = decision_applicability

        # Matriz de costos; costs[state][decision]
        self.costs = costs

        # Lista de matrices de transición para cada decisión
        # transition[decision][origin_state][target_state]
        self.transition = transition

        # Lista de todas las políticas viables; utilizada por enumeración exhaustiva
        self.policies = []

    def __str__(self):
        # Tabla de estados
        state_table = PrettyTable()
        state_table.add_column("Estado", self.states)
        process_str = f"• Los estados son:\n\n{state_table}\n"

        # Tabla de decisiones
        decision_table = PrettyTable()
        decision_table.field_names = ["Decisión", "Estados donde aplica"]
        for decision in self.decisions:
            decision_table.add_row([decision, [state for state, applicable in enumerate(self.decision_applicability[decision]) if applicable]])
        process_str += f"\n• Las decisiones son:\n\n{decision_table}\n"

        # Matriz de costos
        cost_matrix = PrettyTable(header=False)
        cost_matrix.add_rows([[round(cost, 6) if cost is not None else "N/A" for cost in state[1:]] for state in self.costs])
        process_str += f"\n• Los costos son:\n\n{cost_matrix}\n\n"

        transition_matrices = [None] + [PrettyTable(header=False) for decision in self.decisions]
        for decision in self.decisions:
            transition_matrices[decision].add_rows([row for row in self.transition[decision] if row is not None])

        process_str += "\n• Las matrices de transición son:\n\n"
        for decision in self.decisions:
            process_str += f"-> k = {decision}\n{transition_matrices[decision]}\n\n"

        return process_str

    def generate_policies(self):
        # Transponer la matriz decision_applicability para la aplicabilidad de decisiones por estado
        # (originalmente da los estados aplicables para cada decisión)
        # [1:] ya que la decisión 0 no existe
        transposed_applicability = list(
            map(list, zip(*self.decision_applicability[1:])))

        # Generar una matriz con _solo_ las decisiones aplicables en cada estado
        applicable_decisions = []
        for state_applicability in transposed_applicability:
            applicable_decisions.append([decision for decision, applicable in enumerate(
                state_applicability, start=1) if applicable])

        # Generar todas las políticas posibles con el producto cartesiano
        policies = list(product(*applicable_decisions))

        self.policies = policies


def create_process():
    """
    CLI creation of a Process object
    """

    # Estados y decisiones
    states_amount = inp.number(
        "• Introduzca la cantidad de estados que tiene el proceso (empiezan en 0): ", min_value=0)
    decisions_amount = inp.number(
        "• Introduzca la cantidad de decisiones que se pueden tomar (empiezan en 1): ", min_value=0)
    states = [state for state in range(states_amount)]
    decisions = [decision+1 for decision in range(decisions_amount)]

    # Aplicabilidad de decisiones
    decision_applicability = define_decision_applicability(decisions, states)

    # Costos
    costs = define_costs(decisions, states, decision_applicability)

    # Matrices de transición
    transition = define_transition(decisions, states, decision_applicability)

    return Process(states, decisions, decision_applicability, costs, transition)


def define_decision_applicability(decisions, states):
    """
    CLI definition of Process.decision_applicability
    """

    all_decisions = inp.boolean(
        "\n• ¿Todas las decisiones son aplicables para todos los estados? [S]í, [N]o: ", "S", "N")

    # Si todas las decisiones son aplicables, todo es True
    if all_decisions:
        return [None] + [[True for _ in states] for _ in decisions]
    # Si no, poner True donde son aplicables y False donde no
    else:
        decision_applicability = [None]
        for decision in decisions:
            state_list = inp.number(f"-> Introduzca la lista de estados aplicables para la decisión {
                                    decision} (separe con comas): ", min_value=0, size=0)
            decision_applicability.append(
                [True if state in state_list else False for state in states])
        return decision_applicability


def define_costs(decisions, states, decision_applicability):
    """
    CLI definition of Process.costs
    """

    costs = [[None] + [None for _ in decisions] for _ in states]

    # Donde no hay un costo aplicable, hay None. Nótese que un costo de 0 != None
    for state in states:
        print(f"\n• Costos en el estado {state}")
        for decision in decisions:
            if decision_applicability[decision][state]:
                costs[state][decision] = inp.number(
                    f"-> Introduzca el costo de la decisión {decision}: ", number_type="f")

    return costs


def define_transition(decisions, states, decision_applicability):
    """
    CLI definition of Process.transition
    """

    transition = [None] + [[[] if decision_applicability[decision]
                            [state] else None for state in states] for decision in decisions]

    # Si una decisión no es aplicable en un estado, la matriz tiene renglón None
    for decision in decisions:
        print(f"\n• Matriz de probabilidades de transición correspondiente a la decisión {
              decision}")
        for state in states:
            if decision_applicability[decision][state]:
                transition[decision][state] = inp.number(f"-> Columna que parte del estado {
                                                         state} (separe con comas): ", number_type="f", min_value=0,
                                                         max_value=1, size=len(states))

    return transition


if __name__ == "__main__":
    process = create_process()
