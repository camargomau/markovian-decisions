def solve_steady_state(process, policy):
	spliced_matrix = [process.transition[decision][origin_state] for origin_state, decision in enumerate(policy)]
	print(spliced_matrix)

def main(process):
	process.generate_policies()
	print(process.policies)

	solve_steady_state(process, process.policies[1])
	input()
