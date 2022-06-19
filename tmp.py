import re


def isValid(string):
    '''
    Checks if given string is in the format "2 cond1 cond2"\n
    e.g. \n
        cond1 = "a<3","2<a<=90","*" \n
        cond2 = "2:3"\n
    returns True or False
    '''

    # list of regex patterns for 2, cond1 & cond2 respectively
    ptrns = [
        r"2",
        r"(^((((((\d+(<|(<=)))a((<|(<=))\d+))|(a((<|(<=))\d+))))|((((\d+(>|(>=)))a((>|(>=))\d+))|(a((>|(>=))\d+)))))))|(\*)",
        r"^((\d+)|(\d+:)|(:\d+)|(\d+:\d+))"
    ]

    # sepreate 2, cond1 & cond2 and store them in a list
    inps = string.strip().split(sep=" ")

    # Check for all 3 conditions with corresponding regex 
    # and retuen True if all are matching else False
    for ind, val in enumerate(inps):
        match = re.fullmatch(ptrns[ind], val)

        if match is None:
            return False
    else:
        return True


def doesSatisfy(num: float, condition: str):
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

    if condition.startswith('a'): # => binary condition

        # stores the first number
        n1 = float(numLst[-1])
        # stores the relavant function from the operators list
        op1 = operators[oprLst[0]] 

        # calls the func stored in op1 & returns its result
        return op1(num, n1)

    else: # => ternary condition
        # stores the first & second number
        n1 = float(numLst[0])
        n2 = float(numLst[1])

        # stores the relavant functions from the operators list
        op1 = operators[oprLst[0]]
        op2 = operators[oprLst[1]]

        # calls the funcs stored in op1 & op2 returns True only if both are True
        return (op1(num, n1) and op2(num, n2))
