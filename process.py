import input_types

class Process:
	def __init__(self, states, decisions, decision_applicability, costs):
		self.states = states
		self.decisions = decisions

		self.decision_applicability = decision_applicability
		self.costs = costs

		self.transition_pr = [None] + [[[] if self.decision_applicability[decision][state] else None for state in self.states] for decision in self.decisions]
		for decision in self.decisions:
			print(f"Matriz de probabilidades de transición correspondiente a la decisión {decision}")
			for state in self.states:
				if self.decision_applicability[decision][state]:
					self.transition_pr[decision][state] = input(f"Columna que parte del estado {state} (separe con comas): ").split(",")

		self.policies = []



def create_process():
	# Estados y decisiones
	states_amount = input_types.integer("• Introduzca la cantidad de estados que tiene el proceso (empiezan en 0): ")
	decisions_amount = input_types.integer("• Introduzca la cantidad de decisiones que se pueden tomar (empiezan en 1): ")
	states = [state for state in range(states_amount)]
	decisions = [decision+1 for decision in range(decisions_amount)]

	# Aplicabilidad de decisiones
	all_decisions = input_types.boolean("\n• ¿Todas las decisiones son aplicables para todos los estados? [S]í, [N]o: ", "S", "N")
	if all_decisions:
		decision_applicability = [None] + [[True for _ in states] for _ in decisions]
	else:
		decision_applicability = [None] + [define_decision_applicability(decision, states) for decision in decisions]

	# Costos
	costs = [[None] + [define_costs(decision, state) if decision_applicability[decision][state] else None for decision in decisions] for state in states]

	return Process(states, decisions, decision_applicability, costs)

def define_decision_applicability(decision, states):
	state_list = input(f"--> Introduzca la lista de estados aplicables para la decisión {decision} (separe con comas): ").split(",")
	state_list = [int(state) for state in state_list]

	return [True if state in state_list else False for state in states]

def define_costs(decision, state):
	return input(f"• Introduzca el costo de tomar la decisión {decision} en el estado {state}: ")

process = create_process()
