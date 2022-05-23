import re
from requests import head
from rich.table import Table
from rich import box
from rich.console import Console
import datetime

from constants import Constants
from dbManager import DB
import styles
from utilities import *

CON = Console()
CENTER = 'center'


def _readDate():
    '''
    Reads date from the user.
    '''

    def isValidDate(dt: str):
        '''
        Check if given string is a valid date or not.
        '''

        # Check if string is in a **valid date format**
        if re.fullmatch('[0-9]{4}-([0-9]{2}|[0-9])-([0-9]{2}|[0-9])', dt) == None:
            return False

        # If string is in **valid date format**,
        try:
            # Try creating a "datetime.date" object from given date,
            # to check if the **date is valid**
            dt = dt.split(sep='-')
            datetime.date(
                year=int(dt[0]),
                month=int(dt[1]),
                day=int(dt[2])
            )
        except (TypeError, ValueError):
            # If datetime.date raises an Exception,
            # given date is invalid
            return False
        else:
            # If datetime.date does not raise an Exception,
            # given date is valid
            return True

    # set today's date as default date
    default = str(datetime.date.today())

    # Ask user for a date.
    CON.print(
        f"Enter date (YYYY-MM-DD)",
        style=styles.YELLOW_INSTRUCTION_B, justify=CENTER
    )
    CON.print(
        f"Default: {default} (today)",
        style=styles.INSTRUCTION_B, justify=CENTER
    )

    date = CON.input(f":")  # initial input
    while True:
        if date == '':
            # If user does not enter anything, return default date
            return default

        if isValidDate(date):
            # If user enters valid date, return date
            return date

        CON.print(
            "Invalid date... Please Retry !!",
            style=styles.ERROR, justify=CENTER, end=''
        )
        date = CON.input(f":")


def _readTime():
    '''
    Reads time from the user.
    '''
    def isValidTime(timeStr: str):
        '''
        Check if given string is a valid time or not.
        '''

        # Check if string is in a **valid time format**
        if re.fullmatch('(([0-9]{2})|[0-9]):([0-9]{2}|[0-9])', timeStr) == None:
            return False

        # If string is in **valid time format**,
        try:
            # Try creating a "datetime.time" object from given time,
            # to check if the **time is valid**
            timeStr = timeStr.split(sep=':')
            datetime.time(
                hour=int(timeStr[0]),
                minute=int(timeStr[1])
            )
        except (TypeError, ValueError):
            # If datetime.time raises an Exception,
            # given time is invalid
            return False
        else:
            # If datetime.time does not raise an Exception,
            # given time is valid
            return True

    # set current time as default time
    default = datetime.datetime.now()
    default = str(default.hour) + ':' + str(default.minute)

    # Ask user for a time.
    CON.print(
        f"Enter time (HH:MM)",
        style=styles.YELLOW_INSTRUCTION_B, justify=CENTER
    )
    CON.print(
        f"Default: {default} (now)",
        style=styles.INSTRUCTION_B, justify=CENTER
    )

    time = CON.input(f":")  # initial input
    while True:
        if time == '':
            # If user does not enter anything, return default time
            return default

        if isValidTime(time):
            # If user enters valid time, return time
            return time

        CON.print(
            "Invalid time... Please Retry !!",
            style=styles.ERROR, justify=CENTER, end=''
        )
        time = CON.input(f":")


def startAttendence(
    dbName: str,
    date: str,
    time: str,
    clsType: str,
):
    '''Takes present/absent of each student in given class and stores it in DB'''

    # Creatind a DB object
    currDB = DB(Constants.DATA_DIR, dbName)

    # Table names
    dataTable = 'student_details'
    attendenceTable = 'attendence'

    # get details of all students in a list
    allStudents = currDB.readRows(
        dataTable,
        columns=("enroll_num", "f_name", "l_name")
    )

    # Instruction
    CON.print(
        f"Start marking presence of students:",
        style=styles.YELLOW_INSTRUCTION_B, justify=CENTER
    )
    CON.print(
        f"Press ENTER for Present any other letter for Absent\n",
        style=styles.INSTRUCTION_B, justify=CENTER
    )

    # set clsType to lab/lecture
    clsType = "lab" if clsType == '1' else "lecture"

    # Header row
    header = ['date', 'time', 'type']
    # data row
    values = [date, time, clsType]

    # iterate over each student and mark present/absent
    for num, f_name, l_name in allStudents:
        # add enroll_num to header
        header.append(num)

        # Get present/absent for given student
        CON.print(
            f"{num}: {f_name} {l_name}",
            style=styles.INSTRUCTION_B, justify=CENTER
        )
        inp = CON.input(':')

        # set attendence to 1 if present
        attendence = 1 if inp == '' else 0

        # add attendence to values list
        values.append(attendence)
    
    # Add the row to table
    currDB.addRow(
        attendenceTable,
        tuple(header),
        tuple(values)
    )


def main():
    '''
    Initiate the process of getting attendence.
    '''
    # creating a table to store all present DBs/classes
    table = Table(show_header=False, box=box.HEAVY)

    # Get all availabe classes
    availableClasses = sorted(Constants.AvailableDBs())

    # Asking user to select a class
    CON.print("Select a class: ", style=styles.INSTRUCTION_B, justify=CENTER)

    # Adding columns to the table
    table.add_column(style=styles.NUMBER_B)
    table.add_column()

    for i in range(0, len(availableClasses)):
        # add rows/data to the table
        table.add_row(f'{i+1}', f'{availableClasses[i]}')

    # print the table
    CON.print(table, justify=CENTER)

    # Get input of selected DB/class
    inp = CON.input(":")
    while True:
        if inp.isnumeric():
            inp = int(inp)
            if inp <= len(availableClasses) and inp >= 1:
                selectedDB = availableClasses[inp-1]
                break

        else:
            if inp in availableClasses:
                selectedDB = inp
                break

        CON.print(
            "Invalid option... Please Retry !!",
            style=styles.ERROR, justify=CENTER
        )
        inp = CON.input(":")

    date = _readDate()
    time = _readTime()

    # Get lab or lecture
    CON.print("Select : ", justify=CENTER, style=styles.YELLOW_INSTRUCTION_B)
    CON.print(
        "1 - Lab\n2 - Lecture",
        justify=CENTER, style=styles.INSTRUCTION_B
    )

    clsType = int(getMultipleChoiceInp(
        validInputs=('1', '2'),
        console=CON
    ))

    # Start taking attendence from user
    startAttendence(
        dbName=selectedDB,
        date=date,
        time=time,
        clsType=clsType
    )
