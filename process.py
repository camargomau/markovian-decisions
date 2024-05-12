import input_types

class Process:
	def __init__(self, states, decisions, decision_applicability, costs):
		self.states = states
		self.decisions = decisions

		self.decision_applicability = decision_applicability
		self.costs = costs

		self.transition = [None] + [[[] if self.decision_applicability[decision][state] else None for state in self.states] for decision in self.decisions]
		for decision in self.decisions:
			print(f"Matriz de probabilidades de transición correspondiente a la decisión {decision}")
			for state in self.states:
				if self.decision_applicability[decision][state]:
					self.transition[decision][state] = input(f"Columna que parte del estado {state} (separe con comas): ").split(",")

		self.policies = []


def create_process():
	# Estados y decisiones
	states_amount = input_types.number("• Introduzca la cantidad de estados que tiene el proceso (empiezan en 0): ", min=0)
	decisions_amount = input_types.integer("• Introduzca la cantidad de decisiones que se pueden tomar (empiezan en 1): ", min=0)
	states = [state for state in range(states_amount)]
	decisions = [decision+1 for decision in range(decisions_amount)]

	# Aplicabilidad de decisiones
	decision_applicability = define_decision_applicability(decisions, states)

	# Costos
	costs = define_costs(decisions, states, decision_applicability)

	return Process(states, decisions, decision_applicability, costs)


def define_decision_applicability(decisions, states):
	all_decisions = input_types.boolean("\n• ¿Todas las decisiones son aplicables para todos los estados? [S]í, [N]o: ", "S", "N")

	# Si todas las decisiones son aplicables, todo es True
	if all_decisions:
		return [None] + [[True for _ in states] for _ in decisions]
	# Si no, poner True donde son aplicables y False donde no
	else:
		decision_applicability = [None]
		for decision in decisions:
			state_list = input_types.number(f"--> Introduzca la lista de estados aplicables para la decisión {decision} (separe con comas): ", min=0, size=0)
			decision_applicability.append([True if state in state_list else False for state in states])
		return decision_applicability


def define_costs(decisions, states, decision_applicability):
	costs = [[None] + [None for _ in decisions] for _ in states]

	# Donde no hay un costo, hay None. Nótese que un costo de 0 != None
	for state in states:
		print(f"• Costos estando en el estado {state}")
		for decision in decisions:
			if decision_applicability[decision][state]:
				costs[state][decision] = input_types.number(f"-> Introduzca el costo de la decisión {decision}: ", type="f")

	return costs

def define_transition(decisions, states, decision_applicability):
	transition = [None] + [[[] if decision_applicability[decision][state] else None for state in states] for decision in decisions]

	for decision in decisions:
		print(f"• Matriz de probabilidades de transición correspondiente a la decisión {decision}")
		for state in states:
			if decision_applicability[decision][state]:
				transition[decision][state] = input(f"Columna que parte del estado {state} (separe con comas): ").split(",")



process = create_process()
