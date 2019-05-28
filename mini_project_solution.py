#!/usr/bin/env python3
#---------------------------------------------------------------------------------------------------------------------
# A script to read the contents of a pdb file, and perform 3 operations:
#   -   Find the distance between stated atoms in the structure
#   -   Draw the protein using pymol, highlight secondary structure and produce images of the cartoon and stick representations
#   -   Print the sequence of the accession number for stated chains in the pdb file with residues that are not included in the
#       structure as lowercase and output to file
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
        super(Const_Plus_Args, self).__init__(option_strings, dest,  nargs, **kwargs)
        # define the variable that is not in the constructor of the superclass
        self.perf = perf

    # define what happens when this class is called by the argument parser, with arguments:
    #   -   parser - the parser that called the class
    #   -   namespace - the namespace object to use
    #   -   values - the values of the command line arguments provided - default is A,1,1:A,1,2
    def __call__(self, parser, namespace, values=["A,1,1:A,1,2"], option_string=None,  nargs='*'):
        # add each command line argument to the variable specfied as dest in the argparser call
        for arg in values:
            # get the current contents of the variable with the name stored in dest
            items = getattr(namespace, self.dest, None)
            items = argparse._copy_items(items)
            items.append(arg)
            setattr(namespace, self.dest, items)
        perform = getattr(namespace, self.perf, None)
        perform = argparse._copy_items(perform)
        perform.append(self.const)
        setattr(namespace, self.perf, perform)


#---------------------------------------------------------------------------------------------------------------------
# Parse command line arguments
# add an ArgumentParser object

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description ='''A script to read the contents of a pdb file, and perform 3 operations:
\n\t-\tFind the distance between stated atoms in the structure,
\n\t-\tDraw the molecule in pymol, highlighting secondary structure, then produce images of the cartoon and stick structures,
\n\t-\t...''')#TODO:

# add each argument to the parser, along with the help line, for if the script is run with the -h argument, and the type of the argument
# the input argument must be a string
parser.add_argument("-i", "--input",  help="Path to input pdb file", type=str,  required=True)
parser.add_argument("-c", "--calculate",  perf="perform", dest="atoms", action=Const_Plus_Args, const=1,  help='''Perform distance calculation 
for specified atoms.  Atoms are chosen using arguments of the form '[Chain_Name],[Residue_Number],[Atom_Number]', 
where Atom_Number can be a single atom or a start and end atom separated by a colon - the default argument is A,1,1.  
Multiple arguments can be provided in this way''')
parser.add_argument("-d", "--draw", perf="perform", dest="outputpng", action=Const_Plus_Args, nargs="?", const=2, help='''Draw the molecule in pymol, highlighting secondary structure
the output pngs of the cartoon and ball and stick representations.  The files will be named after the input pdb file unless specified with an argument.
To use this option, you will need the pymol module installed.''')
parser.add_argument("-s", "--sequence", perf="perform", dest="chain", action=Const_Plus_Args, const=3, help='''Produce a fasta file containing the NCBI sequence
of the protein with the amino acids that are not present in the structure shown in lower case. The file will be named after the input file.  
If no argument is provided, the first chain in the file will be chosen.''')
args = parser.parse_args()

# check that the input file exists using checking.py module
from checking import checkInput
input_file = checkInput(args.input)

#---------------------------------------------------------------------------------------------------------------------


if not args.perform:
    import sys
    print("No functions were chosen to be performed!")
    sys.exit(0)

if not args.atoms:
    args.atoms = ["A,1,1"]
#---------------------------------------------------------------------------------------------------------------------
if 1 in args.perform:
    print ("Distance calculation\n____________________")
    from distance import find_position, calculate_distance
    import re
    with open(input_file) as pdb:
        content = pdb.readlines()
        for atom in args.atoms:
            if re.search(':', atom):  # if both specified
                atoms = atom.split(':')
                atom0 = atoms[0].split(',')
                atom1 = atoms[1].split(',')
                if len(atom0) == 3 and len(atom1) == 3:
                    print("\nCalculating distance between:")
                    startpos = find_position(content, atom0)
                    if startpos == -1:
                        print ("Calculation not performed")
                        break
                    endpos = find_position(content, atom1)
                    if endpos == -1:
                        print ("Calculation not performed")
                        break
                else:
                    print("Incorrectly formatted atom reference, please ensure that each atom reference is formatted as [Chain],[Residue number],[Atom]")
                    break

            else: # if only first specified
                print("\nCalculating distance between:")
                startpos = find_position(content, atom.split(','))
                if startpos == -1:
                        print ("Calculation not performed")
                        break
                else:
                    print ("and the next atom in the structure")
                endpos = startpos + 1

            if not startpos == -1 and not endpos == -1:
                print("Distance between atoms: ", calculate_distance(content, startpos, endpos))
            else:
                print("Calculation not performed")

    print ("\n\n\n")
#---------------------------------------------------------------------------------------------------------------------

if 2 in args.perform:
    print("Drawing molecule\n________________\n")
    if args.outputpng:
        output_file = args.outputpng
    else:
        outputfile = input_file.split(".")[0]
    import __main__
    __main__.pymol_argv=["pymol", "-qc"]
    from pymol import cmd, finish_launching
    finish_launching()
    cmd.bg_color("white")
    cmd.load(input_file)
    cmd.colour("Blue", "ss s")
    cmd.colour("Yellow", "ss h")
    cmd.png(output_file + "_cartoon")
    cmd.show("cartoon","all")

    cmd.hide("everything","all")

    cmd.png(output_file + "_lines")
    cmd.show("lines","all")
#---------------------------------------------------------------------------------------------------------------------


if 3 in args.perform:
    from Bio import Entrez
    from seqinspection import get_id
    with open(input_file) as file:
        content = file.readlines()
    Entrez.email = "A.N.Other@example.com"
    result = Entrez.efetch(db="protein", id=get_id(content,args.chain), rettype="fasta")
    print(result.read())



