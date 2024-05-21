from scipy import optimize

class Model:
    def __init__(self, process):
        # decision amount
        dcn_amnt = len(process.decisions)

        # Para la función objetivo
        # \sum_{i=0}^{m} \sum_{k=1}^{K} c_{ik} y_{ik}
        costs = []
        for state in process.states:
            for cost in process.costs[state][1:]:
                costs.append(cost if cost is not None else float(0))

        # Para las restricciones explícitas
        # Restricciones para cada estado
        # j = 0, 1, …, m
        constraints = [[0 for _ in costs] for _ in process.states]
        for state in process.states:
            # Suma de las y de tomar la decisión k en el estado j
            # \sum_{k=1}^{K} y_{jk}
            for decision in process.decisions:
                constraints[state][dcn_amnt*state + decision -
                                1] += 1 if process.decision_applicability[decision][state] else 0
            # Suma ponderada de las y de tomar la decisión k en algún estado i anterior a j
            # \sum_{i=0}^{m} \sum_{k=1}^{K} y_{ik} p_{ij}(k)
            for origin_state in process.states:
                for decision in process.decisions:
                    if process.transition[decision][origin_state] is not None:
                        constraints[state][dcn_amnt*origin_state + decision -
                                        1] -= process.transition[decision][origin_state][state]

        # Restricción de suma igual a 1 para todas las decisiones aplicables
        # \sum_{i=0}^{m} \sum_{k=1}^{K} y_{ik}
        one_constraint = [0 for _ in costs]
        for state in process.states:
            for decision in process.decisions:
                if process.decision_applicability[decision][state]:
                    one_constraint[dcn_amnt*state + decision-1] = 1

        # Unión de todas las restricciones explícitas
        constraints.insert(0, one_constraint)

        # Vector b
        constraint_vector = [1] + [0 for _ in process.states]

        # Asignar todo lo obtenido como atributos del objeto
        self.states = process.states
        self.decisions = process.decisions
        self.costs = costs
        self.constraints = constraints
        self.constraint_vector = constraint_vector
        self.raw_solution = None
        self.optimal_policy = None
        self.optimal_cost = None
        self.y_sol_matrix = list(list())

    def __str__(self):
        # Encabezado con "", "Y_01", "Y02", ..., "b"
        header = "| {:^3} ".format("")
        separator = "\n| {:-^3} ".format("")
        for state in self.states:
            for decision in self.decisions:
                header += "| {:^9} ".format(f"Y_{state}{decision}")
                separator += "| {:-^9} ".format("")
        else:
            header += "| {:^9} |".format("b")
            separator += "| {:-^9} |".format("")

        # función objetivo con "Z", costos
        objective_func = "\n| {:^3} ".format("Z")
        for cost in self.costs:
            objective_func += "| {:^ 9.6g} ".format(cost)
        else:
            objective_func += "| {:^9} |".format("")

        # Restricciones
        constraint_print = [None for _ in self.constraints]
        for i in range(len(self.constraints)):
            constraint_print[i] = "\n| {:^3} ".format(f"R{i}")
            for coeff in self.constraints[i]:
                constraint_print[i] += "| {:^ 9.6g} ".format(coeff)
            else:
                constraint_print[i] += "| {:^ 9.6g} |".format(self.constraint_vector[i])

        model_string = header + separator + objective_func
        for constraint in constraint_print:
            model_string += constraint

        return model_string

    def solve_model(self):
        # Resolución del PPL mediante scipy.optimize.linprog, que utiliza HiGHS
        solution = optimize.linprog(
            c=self.costs, A_eq=self.constraints, b_eq=self.constraint_vector)

        # solution.fun es la Z óptima (min), el costo esperado para la política óptima
        self.raw_solution = solution
        self.optimal_cost = solution.fun


    def interpret_model_solution(self):
        dcn_amnt = len(self.decisions)

        # optimize.linprog retorna un objeto cuyo atributo x es el vector solución
        raw_sol_vector = self.raw_solution.x
        # Separar el vector solución en una matriz para un manejo simplificado de índices
        y_sol_matrix = [raw_sol_vector[dcn_amnt*state:dcn_amnt*(state+1)] for state in self.states]

        # Sumar las soluciones para cada estado (renglón)
        row_sum = [0 for _ in self.states]
        for state in self.states:
            for value in y_sol_matrix[state]:
                row_sum[state] += value

        # Binarizar la solución dividiendo entre \sum_{k=1}^{K} y_ik
        binary_sol = [[y_sol_matrix[state][decision]/row_sum[state] for decision in range(dcn_amnt)] for state in self.states]

        # La política óptima es la decisión con 1 para cada estado
        optimal_policy = [binary_sol[state].index(float(1))+1 for state in self.states]

        self.optimal_policy = optimal_policy
        self.y_sol_matrix = y_sol_matrix


def main(process):
    # Formular el modelo
    model = Model(process)
    # Imprimir el modelo
    print(f"• El modelo de programación lineal es:\n\n{model}")
    # Resolver el modelo
    model.solve_model()

    model.interpret_model_solution()

    print(model.y_sol_matrix)

    input()
