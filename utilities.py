from typing import Callable, Iterable, Tuple

import matplotlib.pyplot as plt
from rich import box
from rich.console import Console
from rich.table import Table

import styles
from constants import Constants


def getMultipleChoiceInp(
    validInputs: tuple,
    console: Console,
    default: int = None,
    help: Tuple[int, Callable or str] = None,
    errMsg: str = "Invalid input... Please Retry !!"
):
    if console is None:
        inp = input(":")
    else:
        inp = console.input(":")

    while (inp not in validInputs) or (help is not None and inp == validInputs[help[0]]):
        if default is not None and inp == '':
            return validInputs[default]

        if help is not None and inp == validInputs[help[0]]:
            console.print(help[1], style=styles.INSTRUCTION, justify="center")

        else:
            console.print(
                errMsg,
                style=styles.ERROR, justify="center"
            )

        inp = console.input(":")

    return inp


def classSelector(
    console: Console
) -> str:
    '''
    Displays a table of all available DBs/classes and returns name of class selected by user.
    '''
    CENTER = 'center'
    # creating a table to store all present DBs/classes
    table = Table(show_header=False, box=box.HEAVY)

    # Get all availabe classes
    availableClasses = sorted(Constants.AvailableDBs())

    # Asking user to select a class
    console.print("Select a class: ",
                  style=styles.YELLOW_INSTRUCTION_B, justify=CENTER)

    # Adding columns to the table
    table.add_column(style=styles.NUMBER_B)
    table.add_column()

    for i in range(0, len(availableClasses)):
        # add rows/data to the table
        table.add_row(f'{i+1}', f'{availableClasses[i]}')

    # print the table
    console.print(table, justify=CENTER)

    # Get input of selected DB/class
    inp = console.input(":")
    while True:
        if inp.isnumeric():
            inp = int(inp)
            if inp <= len(availableClasses) and inp >= 1:
                return availableClasses[inp-1]

        else:
            if inp in availableClasses:
                return inp

        console.print(
            "Invalid option... Please Retry !!",
            style=styles.ERROR, justify=CENTER
        )
        inp = console.input(":")


def showTable(
    data: Iterable
):
    '''Displays given nested list in form of table.'''
    # Code copied from:
    # https://www.delftstack.com/howto/matplotlib/plot-table-using-matplotlib/#examples-plot-a-table-in-matplotlib-using-the-matplotlib-pyplot-table-method
    fig, ax = plt.subplots(1, 1)
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=data[1:], colLabels=data[0], loc="center")

    plt.show()
