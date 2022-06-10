import os
import csv
from rich import print
from rich.table import Table
from rich.console import Console

from dbManager import DB
import styles
from constants import Constants
from utilities import *

# Defining some constants
CENTER = 'center'
CON = Console()


def importFromCSV(newDB: DB):
    '''
    Reads a given CSV file and feeds its data into appropriate tables of given database.
    '''

    # Print instructions about formatting of the CSV file
    CON.print(
        "Enter complete path of the csv file.",
        style=styles.YELLOW_INSTRUCTION_B, justify=CENTER, end=""
    )
    msg = '''The file should be formatted in the following way:\n["enrollment num", "last_name first_name middle_name"]'''
    CON.print(msg, style=styles.INSTRUCTION_B, justify=CENTER, end="")

    path = CON.input(":")   # Get path of CSV file.
    while not os.path.isfile(path):
        # Loop until a valid path is entered.
        CON.print(
            "Invalid path... Please Retry !!",
            style=styles.ERROR, justify=CENTER, end=''
        )
        path = CON.input(':')

    with open(path) as file:
        # Open and read the csv file.
        reader = csv.reader(file)
        next(reader)    # Skips the first line i.e. column names

        for i in reader:    # Loops over each line in the csv file.

            # Add a cloumn with name same as enroll_num to "attendence" table
            newDB.addCol('attendence', '\"'+i[0]+'\"', "INTEGER")

            # Add details of student from csv to the "student_details" table
            #
            #   Student details in csv will be in the format :
            #           enrollment_num, last_name first_name middle_name
            #
            #   Student details in "student_details" table will be in the format :
            #           enrollment_num, first_name middle_name last_name

            rowVal = i[1].split()
            rowVal += [""]*(3-len(rowVal))
            newDB.addRow(
                'student_details',
                ('enroll_num', 'f_name', 'm_name', 'l_name'),
                (i[0], rowVal[1], rowVal[2], rowVal[0])
            )

    # Move the DB file from EMPTY_DATA_DIR to DATA_DIR
    # Because thr DB now has some data
    newDB.isNotEmpty()


def dataEntry():
    pass


def createClass():
    '''
    Creates a new database for a new class by taking required inputs from the user.
    '''

    CON.print(
        "Enter class name",
        style=styles.YELLOW_INSTRUCTION_B, justify=CENTER, end=""
    )

    inp = CON.input(':')   # Initial input

    while '/' in inp or inp in Constants.AvailableDBs():
        # Loop till a valid input is entered.
        if inp in inp in Constants.AvailableDBs():
            # If a class name already exists, print already exists
            CON.print(
                f'''Class "{inp}" already exists... Please Retry !!''',
                style=styles.ERROR, justify=CENTER, end=''
            )
        else:
            # If invalid characters are found in class name:
            CON.print(
                "Invalid class name... Please Retry !!",
                style=styles.ERROR, justify=CENTER, end=''
            )
        inp = CON.input(':')

    # Create a new sqlite database with given name
    newDB = DB(Constants.EMPTY_DATA_DIR, inp)

    # Creating 2 tables
    newDB.createTable('student_details')
    newDB.createTable('attendence')

    # Adding columns to newly created tables.
    newDB.addCol('attendence', 'date')
    newDB.addCol('attendence', 'time')
    newDB.addCol('attendence', 'type')
    newDB.addCol('student_details', 'enroll_num')
    newDB.addCol('student_details', 'f_name')
    newDB.addCol('student_details', 'm_name')
    newDB.addCol('student_details', 'l_name')

    # Ask for a how the data will be entered.
    CON.print(
        "How would you like to enter the data :",
        style=styles.YELLOW_INSTRUCTION_B, justify=CENTER, end=""
    )
    CON.print(
        "1 - Import CSV\n 2 - Enter manually",
        style=styles.INSTRUCTION_B, justify=CENTER, end=""
    )

    inp = getMultipleChoiceInp(('1', '2'), CON)

    # Call appropriate functions based on the input.
    if inp == '1':
        importFromCSV(newDB)

    elif inp == '2':
        dataEntry()
