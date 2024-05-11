import input_types

class Process:
	def __init__(self):
		# Estados y decisiones
		self.states_amount = input_types.integer("• Introduzca la cantidad de estados que tiene el proceso (empiezan en 0): ")
		self.decisions_amount = input_types.integer("• Introduzca la cantidad de decisiones que se pueden tomar (empiezan en 1): ")

		self.states = [state for state in range(self.states_amount)]
		self.decisions = [decision+1 for decision in range(self.decisions_amount)]

		# Aplicabilidad de decisiones
		all_decisions = input_types.boolean("\n• ¿Todas las decisiones son aplicables para todos los estados? [S]í, [N]o: ", "S", "N")
		if all_decisions == "S":
			self.decision_applicability = [None] + [[True for _ in self.states] for _ in self.decisions]
		else:
			self.decision_applicability = [None] + [self.define_decision_applicability(decision) for decision in self.decisions]

		self.costs = [[None] + [self.define_costs(decision, state) for decision in self.decisions] for state in self.states]

		self.transition_pr = [None] + [[[] if self.decision_applicability[decision][state] else None for state in self.states] for decision in self.decisions]
		for decision in self.decisions:
			print(f"Matriz de probabilidades de transición correspondiente a la decisión {decision}")
			for state in self.states:
				if self.decision_applicability[decision][state]:
					self.transition_pr[decision][state] = input(f"Columna que parte del estado {state} (separe con comas): ").split(",")

		self.policies = []

	def define_decision_applicability(self, decision):
		state_list = input(f"--> Introduzca la lista de estados aplicables para la decisión {decision} (separe con comas): ").split(",")
		state_list = [int(state) for state in state_list]

		return [True if state in state_list else False for state in self.states]

	def define_costs(self, decision, state):
		if self.decision_applicability[decision][state]:
			return input(f"• Introduzca el costo de tomar la decisión {decision} en el estado {state}: ")
		else:
			return None




ejemplo = Process()
