import sys
import os
sys.path[:0]=[os.getcwd()+'/attendence-manager']
os.chdir(sys.path[0])
print(sys.path)

from main import main

# main()
