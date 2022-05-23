import os
import styles
from constants import *
try:
    from rich import print
    from rich.table import Table
    from rich import box
except ImportError:
    pass

t1 = Table(show_header=False, box=box.HEAVY)

#######################################################
#####################   pending #######################
#######################################################

def markAttendence():
    availableClasses = sorted(Constants.AvailableDBs())
    # for i in os.listdir(Constants.DATA_DIR):
    #     if i.endswith('.attendence.db'):
    #         availableClasses.append(i[:-14])
    # availableClasses.sort()
    print("Select a class: ")
    t1.add_column()
    t1.add_column()
    for i in range(0, len(availableClasses), 2):
        try:
            t1.add_row(
                f'{i} - {availableClasses[i]}', f'{i+1} - {availableClasses[i+1]}')
        except IndexError:
            t1.add_row(f'{i} - {availableClasses[i]}')
        # print(f'{i} - {val}')
    print(t1)

    print(availableClasses)
    

# markAttendence()
