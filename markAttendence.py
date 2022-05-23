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
    def isValidDate(dt: str):
        if re.fullmatch('[0-9]{4}-([0-9]{2}|[0-9])-([0-9]{2}|[0-9])', dt) == None:
            return False

        try:
            dt = dt.split(sep='-')
            datetime.date(
                year=int(dt[0]),
                month=int(dt[1]),
                day=int(dt[2])
            )
        except (TypeError, ValueError):
            return False
        else:
            return True

    default = str(datetime.date.today())
    CON.print(
        f"Enter date (YYYY-MM-DD)",
        style=styles.YELLOW_INSTRUCTION_B, justify=CENTER
    )
    CON.print(
        f"Default: {default} (today)",
        style=styles.INSTRUCTION_B, justify=CENTER
    )
    date = CON.input(f":")
    while True:
        if date == '':
            date = default
            return date

        if isValidDate(date):
            return date

        CON.print(
            "Invalid date... Please Retry !!",
            style=styles.ERROR, justify=CENTER, end=''
        )
        date = CON.input(f":")


def _readTime():
    def isValidTime(timeStr: str):

        if re.fullmatch('(([0-9]{2})|[0-9]):([0-9]{2}|[0-9])', timeStr) == None:
            return False

        try:
            timeStr = timeStr.split(sep=':')
            datetime.time(
                hour=int(timeStr[0]),
                minute=int(timeStr[1])
            )
        except (TypeError, ValueError):
            return False
        else:
            return True

    default = datetime.datetime.now()
    default = str(default.hour) + ':' + str(default.minute)
    CON.print(
        f"Enter time (HH:MM)",
        style=styles.YELLOW_INSTRUCTION_B, justify=CENTER
    )
    CON.print(
        f"Default: {default} (now)",
        style=styles.INSTRUCTION_B, justify=CENTER
    )
    time = CON.input(f":")
    while True:
        if time == '':
            time = default
            return time

        if isValidTime(time):
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
    currDB = DB(Constants.DATA_DIR, dbName)
    dataTable = 'student_details'
    attendenceTable = 'attendence'

    allStudents = currDB.readRows(
        dataTable,
        columns=("enroll_num", "f_name", "l_name")
    )
    print(allStudents)
    CON.print(
        f"Start marking presence of students:",
        style=styles.YELLOW_INSTRUCTION_B, justify=CENTER
    )
    CON.print(
        f"Press ENTER for Present any other letter for Absent\n",
        style=styles.INSTRUCTION_B, justify=CENTER
    )
    clsType = "lab" if clsType == '1' else "lecture"
    header = ['date', 'time', 'type']
    values = [date, time, clsType]
    for num, f_name, l_name in allStudents:
        header.append(num)
        CON.print(
            f"{num}: {f_name} {l_name}",
            style=styles.INSTRUCTION_B, justify=CENTER
        )
        inp = CON.input(':')
        attendence = 1 if inp == '' else 0

        values.append(str(attendence))
    currDB.addRow(
        attendenceTable,
        tuple(header),
        tuple(values)
    )


def main():
    table = Table(show_header=False, box=box.HEAVY)
    availableClasses = sorted(Constants.AvailableDBs())
    CON.print("Select a class: ", style=styles.INSTRUCTION_B, justify=CENTER)

    table.add_column(style=styles.NUMBER_B)
    table.add_column()
    for i in range(0, len(availableClasses)):
        table.add_row(f'{i+1}', f'{availableClasses[i]}')

    CON.print(table, justify=CENTER)

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

    CON.print("Select : ", justify=CENTER, style=styles.YELLOW_INSTRUCTION_B)
    CON.print(
        "1 - Lab\n2 - Lecture",
        justify=CENTER, style=styles.INSTRUCTION_B
    )

    clsType = int(getMultipleChoiceInp(('1', '2'), CON))

    CON.print("Select default value: ", justify=CENTER,
              style=styles.YELLOW_INSTRUCTION_B)
    CON.print(
        "1 - Present (default)\n2 - Absent",
        justify=CENTER, style=styles.INSTRUCTION_B
    )

    startAttendence(
        dbName=selectedDB,
        date=date,
        time=time,
        clsType=clsType
    )

    # CON.print(selectedDB)
    # CON.print(date)
    # CON.print(time)
    # CON.print(clsType)
    # CON.print(defaultVal)


# main()
