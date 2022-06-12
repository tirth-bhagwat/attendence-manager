import re
from typing import Dict

import matplotlib.pyplot as plt
from rich.console import Console

import styles
from dbManager import DB
from utilities import *

# Declaring constants
CON = Console()
CENTER = 'center'


def _searchStudent(
    console: Console,
    students: Dict[int, str],
) -> int:
    '''
    Searches for a student in given dict by taking input string from user.\n
    Parameters\n
    : : console : : rich.console.Console \n
    : : students : :  dict{roll_no : other_details,...}\n\n
    -----
    : : return : :  roll_no of selected student\n
    '''

    while True:
        # Initial input
        inp = console.input(":")

        # If input is a number,
        if inp.isnumeric():
            inp = int(inp)

            # Check if input is a key of given dict
            if inp not in students.keys():
                console.print(
                    'Roll number not found...',
                    style=styles.ERROR, justify=CENTER
                )
                continue
            else:
                console.print(
                    f'Selected : ',
                    style=styles.YELLOW_INSTRUCTION_B, justify=CENTER
                )
                console.print(
                    students[inp]+"\n",
                    style=styles.INSTRUCTION_B, justify=CENTER
                )
                return inp

        else:
            matches = []

            # Add all keys of dict to a list where search pattern matches value/string
            for key, val in students.items():
                if re.search(inp, val) is not None:
                    matches.append(key)

            # If no match is found
            if len(matches) == 0:
                console.print(
                    'No match found...',
                    style=styles.ERROR, justify=CENTER
                )
                continue

            # If only one match is found
            elif len(matches) == 1:
                console.print(
                    f'Selected : ',
                    style=styles.YELLOW_INSTRUCTION_B, justify=CENTER
                )
                console.print(
                    students[matches[0]]+"\n",
                    style=styles.INSTRUCTION_B, justify=CENTER
                )
                return matches[0]

            # Print all found matches and ask user to select one of them
            else:
                # creating a string to print
                match_str = [f'{i} - {students[i]}' for i in matches]
                match_str = '\n'.join(match_str)

                console.print(
                    f'Found : ', style=styles.YELLOW_INSTRUCTION_B, justify=CENTER)
                console.print(
                    match_str, style=styles.INSTRUCTION_B, justify=CENTER)

                return int(
                    getMultipleChoiceInp(
                        validInputs=[str(i) for i in matches],
                        console=CON
                    )
                )


def _percentAttn(
    data: Iterable[Tuple[str, int]],
) -> Tuple[int, int, int]:
    '''
    Gives the attendence of given student in percentage.\n
    : : data : :  list of tuples : [( "lab"/"lecture", 0/1 ), ...]\n
    ---
    : : return : : tuple containing attendence of  lab, lecture & total.\n
    '''

    attn = {'lab': 0, 'lab_total': 0, 'lecture': 0, 'lecture_total': 0}

    # Stores total attendence and atudent's in attn dict
    for col in data:
        if col[0] == 'lab':
            if col[1] == 1:
                attn['lab'] += 1
            attn['lab_total'] += 1

        elif col[0] == 'lecture':
            if col[1] == 1:
                attn['lecture'] += 1
            attn['lecture_total'] += 1

    # claculate attendence in percentage for lab,lect and tootal
    attn_lab = (attn["lab"]/attn["lab_total"])*100
    attn_lecture = (
        attn["lecture"]/attn["lecture_total"])*100
    attn_total = 100*((attn["lab"]+attn["lecture"])/(
        attn["lab_total"]+attn["lecture_total"]))

    return (round(attn_lab, 2), round(attn_lecture, 2), round(attn_total, 2))


def _oneStudent(
    console: Console,
    dbName: str
):
    '''
    Handles input/output when data for single student is required
    '''
    dbHandler = DB(Constants.DATA_DIR, dbName)

    # Fetch data from DB
    studentsRaw = dbHandler.readRows(
        "student_details",
        ('id', 'enroll_num', 'f_name', 'm_name', 'l_name')
    )

    # Process raw-data
    students = {i[0]: f'{i[1]} {i[2]} {i[3]} {i[4]}' for i in studentsRaw}

    console.print(
        "Search student by roll no. , enroll no. OR name :",
        style=styles.YELLOW_INSTRUCTION_B, justify=CENTER
    )

    # Get roll num of student selected by user
    targRollNo = _searchStudent(CON, students)

    # Get enroll num of selected student
    targEnrollNo = dbHandler.readRows(
        tableName='student_details',
        columns=('id', 'enroll_num'),
        where=f'''id = {targRollNo}'''
    )
    targEnrollNo = targEnrollNo[0][1]

    # Read attendence data of selected enroll num
    data = dbHandler.readRows(
        tableName='attendence',
        columns=('date', 'time', 'type', targEnrollNo)
    )
    data = [list(i) for i in data]

    # Calc attendence at lab, lecture and total for the student
    attn_lab, attn_lecture, attn_total = _percentAttn(
        [(i[2], i[-1]) for i in data]
    )

    # In the data,convert "0 -> A" and "1 -> P" for user readability.
    for i in data:
        if i[-1] == 0:
            i[-1] = 'A'
        elif i[-1] == 1:
            i[-1] = 'P'

    console.print(
        'Attendence : ',
        style=styles.YELLOW_INSTRUCTION_B, justify=CENTER
    )
    console.print(
        f'Lab : {round(attn_lab,2)} %',
        style=styles.INSTRUCTION_B, justify=CENTER
    )
    console.print(
        f'Lecture : {round(attn_lecture,2)} %',
        style=styles.INSTRUCTION_B, justify=CENTER
    )
    console.print(
        f'Total : {round(attn_total,2)} %',
        style=styles.INSTRUCTION_B, justify=CENTER
    )

    # Header for the table to be printed
    header = ['Date', 'Time', 'Lecture / Lab', 'P or A']

    # Show the table
    showTable([header]+data)


def _wholeClass(
    console: Console,
    dbName: str
):
    '''
    Handles input/output when data for multiple students is required
    '''
    # Function to be improved in next commit
    fig, ax = plt.subplots()

    dbHandler = DB(Constants.DATA_DIR, dbName)

    enrollNos = dbHandler.readRows(
        'student_details',
        ('enroll_num',),
    )
    enrollNos = [i[0] for i in enrollNos]

    final_attn = {
        'lab': [],
        'lecture': [],
        'total': []
    }
    for num in enrollNos:

        attn_raw = dbHandler.readRows(
            'attendence',
            ('type', num)
        )

        attn_lab, attn_lecture, attn_total = _percentAttn(attn_raw)

        final_attn['lab'].append(attn_lab)
        final_attn['lecture'].append(attn_lecture)
        final_attn['total'].append(attn_total)

    for key, val in final_attn.items():
        if key == 'lab':
            incr = 0.75
        elif key == 'lecture':
            incr = 1
        elif key == 'total':
            incr = 1.25

        bar = ax.bar(
            [i+incr for i in range(len(val))],
            val,
            width=0.25,
        )
        plt.bar_label(bar)

    plt.legend(['Lab', 'Lecture', 'Total'])
    plt.show()


def main():
    '''main function of the analyser class'''
    # Ask user to select a DB/class whoose data is requirred
    selectedDB = classSelector(CON)

    # Ask user for an action to be performed
    CON.print(
        "Select an option : \n",
        style=styles.YELLOW_INSTRUCTION_B, justify=CENTER
    )
    CON.print(
        '''1 - Get attendence of one student. \n2 - Get attendence of all students.\n'h' - For help.''',
        style=styles.INSTRUCTION_B, justify=CENTER
    )

    inp = getMultipleChoiceInp(
        validInputs=('1', '2', 'h'),
        console=CON,
        help=(2, 'hwlpppppp')   # To be added in next commit
    )

    # Call appropriate function based on user's selection
    if inp == '1':
        _oneStudent(CON, selectedDB)
    elif inp == '2':
        _wholeClass(CON, selectedDB)


# _oneStudent(CON, 'cse2')
# _wholeClass(CON, 'cse1')
# _wholeClass(CON, 'cse1-short')
# main()
