#!/usr/bin/env python3
#---------------------------------------------------------------------------------------------------------------------
# A script to read the contents of a pdb file, and perform 3 operations:
#   -   find the c_alpha-c distance for each residue in the structure
#   -   print the sequence provided in the pdb file with residues that are not included in the structure as lowercase
#   -   ...TODO:
#---------------------------------------------------------------------------------------------------------------------
# Function to check that the input file exists - copied from my solution to the previous assignment
def checkInput(input_file):
    #check that file exists
    try:
        # open the file to check that it exists
        test = open(input_file)
        # close the file
        test.close()
        # if the file opened properly, return it
        return input_file
    # if the file wasn't in the stated place, do the following
    except FileNotFoundError:
        # ask the user for another file name, and check that that one exists
        return checkInput(input("The specified input file cannot be found, please provide another path:\n"))

#---------------------------------------------------------------------------------------------------------------------
# Create Action class for the action that needs to be performed by the distance and all arguments (see parsing section)
import argparse

class distanceAction(argparse.Action):
    def __init__(self,  option_strings, dest, nargs=2*'*',  **kwargs):
        super(distanceAction,  self).__init__(option_strings,  dest,  **kwargs)
    def __call__(self, parser, namespace, values, option_string = "A 1".split()):
        print (option_string)
#---------------------------------------------------------------------------------------------------------------------
# Parse command line arguments
# add an ArgumentParser object
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, 
description ='''A script to read the contents of a pdb file, and perform 3 operations:
\n\t-\tfind the c_alpha-c distance for each residue in the structure
\n\t-\tprint the sequence provided in the pdb file with residues that are not included in the structure as lowercase
\n\t-\t...''')#TODO:
# add each argument to the parser, along with the help line, for if the script is run with the -h argument, and the type of the argument
# the input argument must be a string
parser.add_argument("-i","--input",  help = "Path to input pdb file", type = str,  required = True)
# -d, -s, and - TODO: append the correct integer to the perform list, which tell the program which of its functions to perform  
parser.add_argument("-d", "--distance",  dest = "perform",  action="append_const", const = 1,  help="Perform the c_alpha-c distance calculation")
parser.add_argument("-s", "--sequence",  dest = "perform", action = "append_const",  const = 2,  help="Print the sequence with residues not included in the structure shown as lowercase")
#TODO: 3rd function
# -a makes the perform list contain all 3 integers so that it will perform all three tasks
parser.add_argument("-a",  "--all",  dest = "perform",  action = "store_const",  const = [1, 2, 3],  help="Perform all three functions",)
args = parser.parse_args()

# check that the input file exists 
input_file = checkInput(args.input)

#---------------------------------------------------------------------------------------------------------------------
from distance import * 
if 1 in args.perform:
    with open(input_file) as pdb:
        content = pdb.readlines()
        pos = find_positions(content)
        firstatom = pos[0]
        carbons = pos[1]
        for c in carbons:
            print(calculate_distance(int(c) + firstatom, content))
if 2 in args.perform:
    ...#TODO: sequence
if 3 in args.perform:
    ...#TODO: 3rd option 
