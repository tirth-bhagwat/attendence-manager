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


def _convertToTuple(limits: str):
    if limits in ["", "*"]:
        return (None, None)

    limits = limits.split(":")
    arg1 = None if limits[0] == "" else int(limits[0])+1
    arg2 = None if limits[1] == "" else int(limits[1])+1
    return (arg1, arg2)


def isValid(string):
    '''
    Checks if given string is in the format "2 cond1 cond2"\n
    e.g. \n
        cond1 = "a<3","2<a<=90","*" \n
        cond2 = "2:3"\n
    returns False if invalid string,
            dict of {'limits':"",'total':"",'lab':"",'lecture':""} if valid string
    '''

    # list of regex patterns for all conditions
    ptrns = [
        r"2",
        r"^(((\d+:)|(:\d+)|(\d+:\d+))|(\*))",
        r"(^((((((\d+(<|(<=)))a((<|(<=))\d+))|(a((<|(<=))\d+))))|((((\d+(>|(>=)))a((>|(>=))\d+))|(a((>|(>=))\d+)))))))|(\*)",
        r"(^((((((\d+(<|(<=)))a((<|(<=))\d+))|(a((<|(<=))\d+))))|((((\d+(>|(>=)))a((>|(>=))\d+))|(a((>|(>=))\d+)))))))|(\*)",
        r"(^((((((\d+(<|(<=)))a((<|(<=))\d+))|(a((<|(<=))\d+))))|((((\d+(>|(>=)))a((>|(>=))\d+))|(a((>|(>=))\d+)))))))|(\*)",
    ]

    # sepreate all conditions and store them in a list
    inps = string.strip().split(sep=" ")

    # Check for all 3 conditions with corresponding regex
    # and retuen True if all are matching else False
    for ind, val in enumerate(inps):
        match = re.fullmatch(ptrns[ind], val)

        if match is None:
            return False
    else:
        # Add required number of "" at end of list inps[1:3] if its length < 2
        inps[1:5] += (4-len(inps[1:5]))*['']

        return {
            'limits': inps[1],
            'total': inps[2],
            'lab': inps[3],
            'lecture': inps[4]
        }


def _doesSatisfy(num: float, condition: str):
    '''
    Checks if the given number satisfies the given condition\n
    : num : number in float\n
    : condition : a valid condition like : 23<a<89, a>9, etc\n
    :: return :: None if invalid condition, True / False if condition is satisfied or not\n
    '''

    num = float(num)

    # dict of functions related to a given operator
    operators = {
        '<': float.__lt__,
        '<=': float.__le__,
        '>': float.__gt__,
        '>=': float.__ge__
    }

    # list to store numbers and conditionaloperators from given string/condition
    numLst, oprLst = ['', ''], ['', '']
    # A variable to store the position where in the numLst/oprLst the
    # character selected by for loop (i.e. val) will be stored.
    i = 0
    for ind, val in enumerate(condition):

        # ignore "="
        if val == '=':
            continue

        # If zeroth char is a number => ternary condition (12<a<=30)
        #                            => else binary condition (a<12)
        if ind == 0 and val.isnumeric():
            numLst[i] += val

        else:
            tmp = ''
            if val.isnumeric():
                # if val is a number stores it in numLst[i]
                numLst[i] += val

            elif val in ['<', '>']:
                # if val is < or > stores it in oprLst[i] along with the succeeding "=" if present
                tmp += val
                if condition[ind+1] == '=':
                    tmp += '='
                oprLst[i] += tmp

                i = 1 if i == 0 else 1

    if condition.startswith('a'):  # => binary condition

        # stores the first number
        n1 = float(numLst[-1])
        # stores the relavant function from the operators list
        op1 = operators[oprLst[0]]

        # calls the func stored in op1 & returns its result
        return op1(num, n1)

    else:  # => ternary condition
        # stores the first & second number
        n1 = float(numLst[0])
        n2 = float(numLst[1])

        # stores the relavant functions from the operators list
        op1 = operators[oprLst[0]]
        op2 = operators[oprLst[1]]

        # calls the funcs stored in op1 & op2 returns True only if both are True
        return (op1(num, n1) and op2(num, n2))


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
    dbName: str,
    conditions: dict,
):
    '''
    Handles input/output when data for multiple students is required
    '''
    # Function to be improved in next commit
    fig, ax = plt.subplots()

    dbHandler = DB(Constants.DATA_DIR, dbName)
    # reads data of all students from db
    students = dbHandler.readRows(
        'student_details',
        ('enroll_num',),
    )

    # get only enroll nums from "students" list
    enrollNos = [i[0] for i in students]

    # a dict to store attendence data of students
    final_attn = {
        'roll_nos': [],
        'lab': [],
        'lecture': [],
        'total': []
    }
    for ind, num in enumerate(enrollNos):
        # this for loop adds data to the "final_attn" dict
        attn_raw = dbHandler.readRows(
            'attendence',
            ('type', num)
        )

        attn_lab, attn_lecture, attn_total = _percentAttn(attn_raw)
        final_attn['roll_nos'].append(ind+1)
        final_attn['lab'].append(attn_lab)
        final_attn['lecture'].append(attn_lecture)
        final_attn['total'].append(attn_total)

    # Keep data of only students specified in the "limits" condition
    limits = _convertToTuple(conditions['limits'])
    for typ in final_attn:
        final_attn[typ] = final_attn[typ][limits[0]:limits[1]]

    # Iterate over each roll num of final_attn['roll_nos']
    for i in range(len(final_attn['roll_nos'])):
        targKeys = ['total', 'lab', 'lecture']

        flag = True
        for key in targKeys:
            if conditions[key] not in (' ', '', '*'):
                if not _doesSatisfy(final_attn[key][i], conditions[key]):
                    flag = False
                    break
        
        if flag == False:
            for k in final_attn.keys():
                final_attn[k][i] = None

    for key in final_attn.keys():
        final_attn[key] = list(
            filter(lambda x: x is not None, final_attn[key]))

    for key, val in final_attn.items():

        if key == 'roll_nos':
            continue

        if key == 'lab':
            incr = -0.25
        elif key == 'lecture':
            incr = 0
        elif key == 'total':
            incr = +0.25

        bar = ax.bar(
            [i+incr for i in final_attn['roll_nos']],
            val,
            width=0.25,
        )
        plt.bar_label(bar)

    plt.legend(['Lab', 'Lecture', 'Total'])
    plt.xticks(final_attn['roll_nos'])
    plt.xlabel("Roll Number")
    plt.ylabel("Percentage attendence")
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

    help_text = '''Enter 1 to get info of one student\n "2 numOfStudents total lab lect" to filter students by conditions.'''
    while True:

        inp = CON.input(":")
        if inp.strip() == 1:
            _oneStudent(CON, selectedDB)
            break

        elif inp.strip().lower() == 'h':
            CON.print(
                help_text,
                style=styles.INSTRUCTION, justify="center"
            )

        elif isValid(inp.strip().lower()) != False:
            validInps = isValid(inp.strip().lower())
            _wholeClass(CON, selectedDB, validInps)
            break

        else:
            CON.print(
                "Invalid input... Please Retry !!",
                style=styles.ERROR, justify="center"
            )

# main()
# _oneStudent(CON, 'cse2')
# _wholeClass(CON, 'cse1-short', 'a<70', '*')
# _wholeClass(CON, 'cse1', '', '*')
# print(_doesSatisfy(10,'a<50'))
# _wholeClass(CON, 'cse1-short')
# main()
