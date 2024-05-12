import auxiliary.input_func as inp


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

        # ¿Posiblemente útil?
        # ¿Posiblemente para guardar todas las políticas viables?
        # ¿Posiblemente para enumeración exhaustiva y mejoramiento de políticas?
        self.policies = []


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
