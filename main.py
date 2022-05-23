from rich.console import Console

from constants import Constants
import styles
from markAttendence import markAttendence

# Setting up constant variables
Constants.HOME_DIR="./"
Constants.DATA_DIR="./data"
Constants.LOGGING_DIR='./logs'
Constants.setupLogger()

# Creating an console object
CON = Console()

# Print welcome message
CON.print(("="*36), justify="center", style=styles.HEADING)
CON.print("|| Welcome to attendence manager. ||", style=styles.HEADING_B, justify="center")
CON.print(("="*36)+'\n', style=styles.HEADING, justify="center")

# Print first instruction
instruction = '''1 - Mark attendence.\n2 - Create new class.'''
CON.print(instruction, justify="center", style=styles.INSTRUCTION_B)

validInps = ('1', '2')  # Tuple of valid inputs
inp = input()   # Initial input

while inp not in validInps:
    # Loop till a valid input is given.
    CON.print("Invalid Option. Please Retry !!", style=styles.ERROR, justify='center')
    inp = input()

# If user selects '1' call markAttendence 
if inp == '1':
    markAttendence()
