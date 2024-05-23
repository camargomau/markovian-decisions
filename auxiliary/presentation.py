def clear_screen():
    import os
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


def cover():
    clear_screen()
    data = ["Universidad Nacional Autónoma de México",
            "Facultad de Estudios Superiores Acatlán",
            "Matemáticas Aplicadas y Computación\n",
            "{:-^47}\n".format(""),
            "Proyecto Final",
            "Procesos Markovianos de Decisión\n",
            "Burciaga Piña Erick Osvaldo",
            "Camargo Badillo Luis Mauricio",
            "Gudiño Romero Miguel Ángel",
            "Gutiérrez Flores Daniel\n",
            "Procesos Estocásticos",
            "Grupo 2602\n",
            "{:-^47}\n".format(""),
            "Presiona enter para continuar"]

    for datum in data:
        print(" {:^47} ".format(datum))

    input()
    clear_screen()
