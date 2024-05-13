from auxiliary.misc import clear_screen, cover
from auxiliary.process_def import Process
from solve.linear_prog import solve_linear_prog, interpret_linear_sol

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

solucion_lineal = solve_linear_prog(ejemplo)
print(interpret_linear_sol(ejemplo, solucion_lineal))

"""
def menu():
    global eleccion_metodo
    opciones_metodos = {
        1: "Método de Lagrange",
        2: "Método de Hermite",
        3: "Método de Splines",
        4: "Método de Simpson 1/3",
        5: "Método de Simpson 3/8",

        0: "Salir"
    }

    while True:
        clear_screen()
        print("Métodos disponibles:\n")
        for opcion in opciones_metodos.keys():
            print(f"{opcion} --- {opciones_metodos[opcion]}")

        while True:
            try:
                eleccion_metodo = int(input("\n¿Qué método desea utilizar? "))
            except:
                print("\nIntroduzca un número entero.")
                continue

            if (eleccion_metodo >= 0) and (eleccion_metodo < len(opciones_metodos.keys())):
                break
            else:
                print(
                    f"\nIntroduzca un número entre 0 y {len(opciones_metodos.keys())-1}.")

        if eleccion_metodo == 1:
            clear_screen()
            lagrange.main()
            continue
        elif eleccion_metodo == 2:
            clear_screen()
            hermite.main()
            continue
        elif eleccion_metodo == 3:
            clear_screen()
            splines.main()
            continue
        elif eleccion_metodo == 4:
            clear_screen()
            simpson_13.main()
            continue
        elif eleccion_metodo == 5:
            clear_screen()
            simpson_38.main()
            continue
        elif eleccion_metodo == 0:
            break

if __name__ == "__main__":
    cover()
    menu()
"""
