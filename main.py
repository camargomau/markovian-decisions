from auxiliary.process_def import Process
from solve.linear_prog import solve_linear_prog

if __name__ == "__main__":
    # Ejemplo de las máquinas con deterioro visto durante el curso
    ejemplo = Process(
        states=[0, 1, 2, 3],
        decisions=[1, 2, 3],

        decision_applicability=[None,
                                [True, True, True, False],
                                [False, False, True, False],
                                [False, True, True, True]],

        costs=[[None, 0.0, None, None],
               [None, 1000.0, None, 6000.0],
               [None, 3000.0, 4000.0, 6000.0],
               [None, None, None, 6000.0]],

        transition=[None,

                    [[0.0, 0.875, 0.0625, 0.0625],
                     [0.0, 0.75, 0.125, 0.125],
                     [0.0, 0.0, 0.5, 0.5],
                     None],

                    [None,
                     None,
                     [0.0, 1.0, 0.0, 0.0],
                     None],

                    [None,
                     [1.0, 0.0, 0.0, 0.0],
                     [1.0, 0.0, 0.0, 0.0],
                     [1.0, 0.0, 0.0, 0.0]]]
    )

    print(solve_linear_prog(ejemplo))
