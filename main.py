import os
from rich.console import Console

from constants import Constants
import styles
import markAttendence
from utilities import *
import createClass


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
        "1 - Mark attendence.\n2 - Create new class.",
        justify=CENTER, style=styles.INSTRUCTION_B
    )

    # Get input for first instruction
    inp = getMultipleChoiceInp(('1', '2'), CON)

    # If user selects '1' call markAttendence
    if inp == '1':
        markAttendence.main()
    elif inp == '2':
        createClass.createClass()

main()
