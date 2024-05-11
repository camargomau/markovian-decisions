"""
Provides functions that handle input with various data types.
"""


def integer(prompt):
    """
    Function for handling the input of an integer.
    """

    while True:
        try:
            answer = int(input(prompt))

            if answer < 1:
                raise IndexError

            break
        except IndexError:
            prompt = "-> Introduzca un número entero mayor o igual que 1: "
        except ValueError:
            prompt = "-> Introduzca un número entero: "

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
