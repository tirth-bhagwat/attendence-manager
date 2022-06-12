import os

from rich.console import Console

import analyser
import createClass
import markAttendence
import styles
from constants import Constants
from utilities import *


def main():
    # Setting up constant variables
    Constants.HOME_DIR = "./"
    Constants.DATA_DIR = "./data"
    Constants.EMPTY_DATA_DIR = './data/empty'
    Constants.LOGGING_DIR = './logs'
    Constants.setupLogger()

    CENTER = 'center'
    CON = Console()

    # Cleanup the "EMPTY_DATA_DIR"
    for file in os.listdir(Constants.EMPTY_DATA_DIR):
        try:
            os.remove(Constants.EMPTY_DATA_DIR+"/"+file)
        except IsADirectoryError:
            # This can be logged as found an unknown folder xyz in empty_data_dir
            pass

    # Print welcome message
    CON.print(("="*36), justify=CENTER, style=styles.HEADING)
    CON.print(
        "|| Welcome to attendence manager. ||",
        style=styles.HEADING_B, justify=CENTER
    )
    CON.print(("="*36)+'\n', style=styles.HEADING, justify=CENTER)

    # Print first instruction
    CON.print(
        "1 - Mark attendence.\n2 - Analyze attendence.\n3 - Create new class.",
        justify=CENTER, style=styles.INSTRUCTION_B
    )

    # Get input for first instruction
    inp = getMultipleChoiceInp(
        validInputs=('1', '2', '3'),
        console=CON
    )

    # Call appropriate function based on user input
    if inp == '1':
        markAttendence.main()
    elif inp == '2':
        analyser.main()
    elif inp == '3':
        createClass.createClass()


main()
