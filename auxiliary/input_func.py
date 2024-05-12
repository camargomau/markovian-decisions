"""
Provides functions that handle input with various data types.
"""


def number(prompt, number_type="i", min_value=None, max_value=None, size=1, separator=","):
    """
    Function for handling the input of an integer (or an array thereof), with optional min and max constraints.
    """

    if size == 1:
        while True:
            try:
                if number_type == "i":
                    answer = int(input(prompt))
                elif number_type == "f":
                    answer = input(prompt)

                    if "/" in answer:
                        num, den = answer.split("/")
                        answer = float(num)/float(den)
                    else:
                        answer = float(answer)

                if min_value is not None and answer < min_value:
                    raise ValueError
                elif max_value is not None and answer > max_value:
                    raise ValueError
                break

            except ValueError:
                if number_type == "i":
                    type_string = "entero"
                elif number_type == "f":
                    type_string = "real"

                if min_value is not None and max_value is not None:
                    prompt = f"--> Introduzca un número {
                        type_string} en [{min_value}, {max_value}]: "
                elif min_value is not None:
                    prompt = f"--> Introduzca un número {
                        type_string} mayor o igual que {min_value}: "
                elif max_value is not None:
                    prompt = f"--> Introduzca un número {
                        type_string} menor o igual que {min_value}: "
                else:
                    prompt = f"--> Introduzca un número {type_string}: "
        return answer
    else:
        while True:
            if number_type == "i":
                type_string = "enteros"
            elif number_type == "f":
                type_string = "reales"

            answer = input(prompt).strip().split(separator)
            if size != 0 and len(answer) != size:
                prompt = f"--> Introduzca exactamente {size} {type_string}: "
                continue

            try:
                answer_list = []
                for number in answer:
                    if number_type == "i":
                        number = int(number)
                    elif number_type == "f":
                        if "/" in number:
                            num, den = number.split("/")
                            number = float(num)/float(den)
                        else:
                            number = float(number)

                    if min_value is not None and number < min_value:
                        raise ValueError
                    elif max_value is not None and number > max_value:
                        raise ValueError
                    answer_list.append(number)

                break

            except ValueError:
                if min_value is not None and max_value is not None:
                    prompt = f"--> Introduzca números {
                        type_string} en [{min_value}, {max_value}]: "
                elif min_value is not None:
                    prompt = f"--> Introduzca números {
                        type_string} mayores o iguales que {min_value}: "
                elif max_value is not None:
                    prompt = f"--> Introduzca número {
                        type_string} menores o iguales que {min_value}: "
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
