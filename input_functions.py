"""
Provides functions that handle input with various data types.
"""

def number(prompt, type="i", min=None, max=None, size=1, separator=","):
    """
    Function for handling the input of an integer (or an array thereof), with optional min and max constraints.
    """

    if size == 1:
        while True:
            try:
                if type == "i":
                    answer = int(input(prompt))
                elif type == "f":
                    answer = input(prompt)

                    if "/" in answer:
                        num, den = answer.split("/")
                        answer = float(num)/float(den)
                    else:
                        answer = float(answer)

                if min is not None and answer < min:
                    raise ValueError
                elif max is not None and answer > max:
                    raise ValueError
                break

            except ValueError:
                if type == "i":
                    type_string = "entero"
                elif type == "f":
                    type_string = "real"

                if min is not None and max is not None:
                    prompt = f"--> Introduzca un número {type_string} en [{min}, {max}]: "
                elif min is not None:
                    prompt = f"--> Introduzca un número {type_string} mayor o igual que {min}: "
                elif max is not None:
                    prompt = f"--> Introduzca un número {type_string} menor o igual que {min}: "
                else:
                    prompt = f"--> Introduzca un número {type_string}: "
        return answer
    else:
        while True:
            if type == "i":
                type_string = "enteros"
            elif type == "f":
                type_string = "reales"

            answer = input(prompt).strip().split(separator)
            if size != 0 and len(answer) != size:
                prompt = f"--> Introduzca exactamente {size} {type_string}: "
                continue

            try:
                answer_list = []
                for number in answer:
                    if type == "i":
                        number = int(number)
                    elif type == "f":
                        if "/" in number:
                            num, den = number.split("/")
                            number = float(num)/float(den)
                        else:
                            number = float(number)

                    if min is not None and number < min:
                        raise ValueError
                    elif max is not None and number > max:
                        raise ValueError
                    answer_list.append(number)

                break

            except ValueError:
                if min is not None and max is not None:
                    prompt = f"--> Introduzca números {type_string} en [{min}, {max}]: "
                elif min is not None:
                    prompt = f"--> Introduzca números {type_string} mayores o iguales que {min}: "
                elif max is not None:
                    prompt = f"--> Introduzca número {type_string} menores o iguales que {min}: "
                else:
                    prompt = f"--> Introduzca números {type_string}: "

        return answer_list


def boolean(prompt, opt_1, opt_2):
    """
    Function for handling a boolean input;
    opt_1 and opt_2 are single letters each
    """

    answer = input(prompt)
    while answer.upper() != opt_1 and answer.upper() != opt_2:
        answer = input(f"--> Introduzca {opt_1} o {opt_2}: ")

    if answer.upper() == opt_1:
        return True
    else:
        return False
