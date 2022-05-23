import rich

import styles


def getMultipleChoiceInp(
    validInputs: tuple,
    console: rich.console.Console = None,
    default=None,
    errMsg: str = "Invalid input... Please Retry !!"
):
    if console is None:
        inp = input(":")
    else:
        inp = console.input(":")

    while inp not in validInputs:
        if default is not None and inp == '':
            return default

        if console is None:
            print(errMsg)
        else:
            console.print(
                errMsg,
                style=styles.ERROR, justify="center"
            )

        if console is None:
            inp = input(":")
        else:
            inp = console.input(":")

    return inp
