#!/usr/bin/env python3
#---------------------------------------------------------------------------------------------------------------------
# A script to read the contents of a pdb file, and perform 3 operations:
#   -   find the c_alpha-c distance for each residue in the structure
#   -   print the sequence provided in the pdb file with residues that are not included in the structure as lowercase?
#   -   ...TODO: Size of unit cell, type of unit cell, number of molecules per 1cm^3/ equivalent for NMR?
#   -   Draw protein, highlight ss and produce image?
#---------------------------------------------------------------------------------------------------------------------
# Create Action classes for the actions that needs to be performed by the distance and all arguments (see parsing section)
import argparse


# Class is a subclass of the Action class in argparse
class Const_Plus_Args(argparse.Action):
    # define the constructor for the class, with arguments:
    #   -   option_strings - contains the command line option used to call the action
    #   -   dest - contains the name of the destination in which to place the arguments that were written after the command line option
    #   -   perf - contains the name of the destination in which to place the selected constant
    #   -   nargs - specifies the number of arguments that are expected after the option, in this case, any number of arguments can be taken
    #   -   **kwargs - passes the rest of the arguments on to the superclass constructor
    def __init__(self,  option_strings, dest, perf, nargs='*',  **kwargs):
        # Call to the superclass so that variables don't need to be redefined here
        super(Const_Plus_Args, self).__init__(option_strings, dest,  nargs = '*', **kwargs)
        # define the variable that is not in the constructor of the superclass
        self.perf = perf
    # define the what happens when this class is called by the argument parser, with arguments:
    #   -   parser - the parser that called the class
    #   -   namespace - the namespace object to use
    #   -   values - the values of the command line arguments provided

    def __call__(self, parser, namespace, option_string,  values = "A,1",  nargs = '*'):
        # add each command line argument to the variable specfied as dest in the argparser call
        for arg in values:
            # get the current contents of the variable with the name stored in dest
            items = getattr(namespace, self.dest, None)
            # 
            items = argparse._copy_items(items)
            items.append(arg)
            setattr(namespace, self.dest, items)
        if option_string == "-d":
            perform = getattr(namespace, self.perf, None)
            perform = argparse._copy_items(perform)
            perform.append(self.const)
        else:
            perform = [self.const]
        setattr(namespace, self.perf, perform)

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
parser.add_argument("-d", "--distance",  perf = "perform", dest = "residues",   action=Const_Plus_Args, const = 1,  help='''Perform the c_alpha-c distance calculation.
Residues are chosen using arguments of the form '[Chain_Name],[Residue_Number]', where Residue_Number can be a single residue, or a start and end residue separated by a colon.  
Multiple arguments can be provided in this way''')
parser.add_argument("-s", "--sequence",  dest = "perform", action = "append_const",  const = 2,  help="Print the sequence with residues not included in the structure shown as lowercase")
#
# TODO: 3rd function
# -a makes the perform list contain all 3 integers so that it will perform all three tasks
parser.add_argument("-a",  "--all",  dest="residues", perf = "perform",  action = Const_Plus_Args,  const = [1, 2, 3],  help='''Perform all three functions.  
Residues for the distance calculation are specified in the same way as for -d''')
args = parser.parse_args()

# check that the input file exists using checking.py module
from checking import checkInput
input_file = checkInput(args.input)

#---------------------------------------------------------------------------------------------------------------------


if not args.perform:
    import sys
    print("No functions were chosen to be performed!")
    sys.exit(0)

#---------------------------------------------------------------------------------------------------------------------
if 1 in args.perform:
    from distance import find_positions, calculate_distance
    # TODO: check that the residues are correctly formatted
    # TODO: output only specified residues
    with open(input_file) as pdb:
        content = pdb.readlines()
        firstatoms, chains, carbons = find_positions(content)
        firstatom = {}
        for i in range(0,len(firstatoms)):
            firstatom[chains[i]] = firstatoms[i]
        print(firstatom)
        
        for c in carbons:
            print(calculate_distance(int(c) + firstatoms[0], content))
if 2 in args.perform:
    ...#TODO: sequence
if 3 in args.perform:
    ...#TODO: 3rd option 

