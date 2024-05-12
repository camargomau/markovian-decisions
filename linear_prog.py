from scipy import optimize
from process import Process

def linear_programming(process):
	costs = []
	for state in process.states:
		for decision in process.costs[state][1:]:
			if decision is None:
				costs.append(float(0))
			else:
				costs.append(decision)

	# \sum_{i=0}^{m} \sum_{k=1}^{K} y_{ik}
	one_constraint = [1 for _ in costs]

	constraints = [[] for _ in process.states]
	# para j = 0, 1, …, m
	for state in process.states:
		# \sum_{k=1}^{K} y_{jk}
		for decision in process.decisions:
			if process.decision_applicability[decision][state]:
				constraints[state].append(1)
			else:
				constraints[state].append(0)
		# \sum_{i=0}^{m} \sum_{k=1}^{K} y_{ik} p_{ij}(k)
		for origin_state in process.states:
			for decision in process.decisions:
				if process.transition[decision][origin_state] is None:
					constraints[state].append(0 for _ in process.states)
				else:
					constraints[state].append(process.transition[decision][origin_state][state])

	print(constraints)




ejemplo = Process(
	states = [0, 1, 2, 3],
	decisions = [1, 2, 3],
	decision_applicability = [None,
		 					  [True, True, True, False],
							  [False, False, True, False],
							  [False, True, True, True]],

	costs = [[None, 0.0, None, None],
			 [None, 1000.0, None, 3000.0],
			 [None, 4000.0, 6000.0, 6000.0],
			 [None, None, None, 6000.0]],

	transition = [None,
			      [[0.0, 0.875, 0.0625, 0.0625], [0.0, 0.75, 0.125, 0.125], [0.0, 0.0, 0.5, 0.5], None],
				  [None, None, [0.0, 1.0, 0.0, 0.0], None],
				  [None, [1.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0]]]
)

linear_programming(ejemplo)
