"""
Provides functions that handle input with various data types.
"""


def integer(prompt, min=None, max=None, size=1, separator=","):
    """
    Function for handling the input of an integer (or an array thereof), with optional min and max constraints.
    """

    if size == 1:
        while True:
            try:
                answer = int(input(prompt))
                if min is not None and answer < min:
                    raise ValueError
                elif max is not None and answer > max:
                    raise ValueError
                break

            except ValueError:
                if min is not None and max is not None:
                    prompt = f"-> Introduzca un número entero en [{min}, {max}]: "
                elif min is not None:
                    prompt = f"-> Introduzca un número entero mayor o igual que{min}: "
                elif max is not None:
                    prompt = f"-> Introduzca un número entero menor o igual que {min}: "
                else:
                    prompt = "-> Introduzca un número entero: "
        return answer
    else:
        while True:
            answer = input(prompt).strip().split(separator)
            if size != 0 and len(answer) != size:
                prompt = f"-> Introduzca exactamente {size} enteros: "
                continue

            try:
                answer_list = []
                for num in answer:
                    num = int(num)
                    if min is not None and num < min:
                        raise ValueError
                    elif max is not None and num > max:
                        raise ValueError
                    answer_list.append(num)

                break

            except ValueError:
                if min is not None and max is not None:
                    prompt = f"-> Introduzca números enteros en [{min}, {max}]: "
                elif min is not None:
                    prompt = f"-> Introduzca números enteros mayores o iguales que{min}: "
                elif max is not None:
                    prompt = f"-> Introduzca número enteros menores o iguales que {min}: "
                else:
                    prompt = "-> Introduzca números enteros: "

        return answer_list



def floating(prompt):
    """
    Function for handling the input of a float.
    """

    while True:
        try:
            answer = float(input(prompt))
            break

        except ValueError:
            prompt = "-> Introduzca un número real: "

    return answer


def boolean(prompt, opt_1, opt_2):
    """
    Function for handling a boolean input;
    opt_1 and opt_2 are single letters each
    """

    answer = input(prompt)
    while answer.upper() != opt_1 and answer.upper() != opt_2:
        answer = input(f"-> Introduzca {opt_1} o {opt_2}: ")

    if answer.upper() == opt_1:
        return True
    else:
        return False
