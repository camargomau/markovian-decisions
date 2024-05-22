import auxiliary.input_func as inp
from auxiliary.misc import clear_screen, cover
from auxiliary.process_def import Process, create_process

import solve.enumeration as enumeration
import solve.linear_prog as linear_prog

def menu(process):
    global method_choice
    method_options = {
        1: "Enumeración Exhaustiva",
        2: "Programación Lineal",
        3: "Mejoramiento de Políticas",
        4: "Mejoramiento de Políticas con Descuento",
        5: "Aproximaciones Sucesivas",

        0: "Salir"
    }

    while True:
        clear_screen()
        print("Métodos disponibles:\n")
        for opcion in method_options.keys():
            print(f"{opcion} --- {method_options[opcion]}")

        while True:
            method_choice = inp.number("\n¿Qué método desea utilizar? ", min_value=0, max_value=5)
            break

        if method_choice == 1:
            clear_screen()
            enumeration.main(process)
            continue
        elif method_choice == 2:
            clear_screen()
            linear_prog.main(process)
            continue
        elif method_choice == 3:
            clear_screen()
            # improvement.main()
            continue
        elif method_choice == 4:
            clear_screen()
            # improvement_disc.main()
            continue
        elif method_choice == 5:
            clear_screen()
            # approximations.main()
            continue
        elif method_choice == 0:
            break

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

    cover()

    # Descomenta estas dos lineas para introducir cualquier otro systema
    # process = create_process()
    # menu(process)
    # y comenta esta de abajo
    menu(ejemplo)
