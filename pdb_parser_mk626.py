#!/usr/bin/env python3
#---------------------------------------------------------------------------------------------------------------------
# A script to read the contents of a pdb file, and perform 3 operations:
#   -   Find the distance between stated atoms in the structure
#   -   Draw the protein using pymol, highlight secondary structure and produce images of the cartoon and stick representations
#   -   Print the sequence of the accession number for stated chains in the pdb file with residues that are not included in the
#       structure as lowercase and output to file
#---------------------------------------------------------------------------------------------------------------------
# Import required modules

# modules for argument parsing
import argparse
from checking import checkInput

# module for exiting if no further code will be executed
import sys

# modules for calculating atom-atom distances
from calculate_distance import calculate_distance, parse_arguments
import re

#modules for drawing the structure
import __main__
from pymol import cmd,finish_launching
import time

# modules for making the fasta file
from Bio import Entrez
import seqinspection as seqin


#---------------------------------------------------------------------------------------------------------------------
# Create an Action class for the action that needs to be performed by the function arguments (see parsing section)

# This class is a subclass of the Action class in argparse
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
    def __call__(self, parser, namespace, values, option_string=None,  nargs='*'):
        # add each command line argument to the variable specfied as dest in the argparser call
        for arg in values:
            # get the current contents of the variable with the name stored in dest
            items = getattr(namespace, self.dest, None)
            # change items into a list containing the variables
            items = argparse._copy_items(items)
            # use the list method append to add the new argument to the list
            items.append(arg)
            # set the contents of the the variable with the name stored in dest to the new list
            setattr(namespace, self.dest, items)

        # repeat the actions done above with the variable with the name stored in perf
        # get current contents
        perform = getattr(namespace, self.perf, None)
        # change to a list
        perform = argparse._copy_items(perform)
        # add new argument
        perform.append(self.const)
        # set the variable
        setattr(namespace, self.perf, perform)


#---------------------------------------------------------------------------------------------------------------------
# Parse command line arguments

# add an ArgumentParser object with a description telling the user what functions the script can perform
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 description ='''A script to read the contents of a pdb file and perform 3 operations:
\n\t-\tFind the distance between stated atoms in the structure,
\n\t-\tDraw the molecule in pymol, highlighting secondary structure, then produce images of the cartoon and stick structures,
\n\t-\tFind which residues are missing from the structure, and output a fasta file with missing residues in lower case.''')

# add each argument to the parser
# the input argument must be a string and must be present
parser.add_argument("-i", "--input",  help="Path to input pdb file", type=str,  required=True)
# each function argument uses the action class defined above so that it can both tell the script that it is present and provide arguments
# -c puts the value 1 into 'perform' and its arguments into 'atoms', sets the default values if no arguments given
parser.add_argument("-c", "--calculate",  perf="perform", dest="atoms", action=Const_Plus_Args, const=1, default=["A,1,1:A,1,CA"],  help='''Perform distance calculation for specified atoms.  
Format - '[Chain_Name],[Residue_Number],[Atom_Type/Number]', either singly or in colon-separated pairs.  
"A,1,1:A,1,CA" is the default argument.''')
# -d puts the value 2 into 'perform' and its argument into 'outputpng', more arguments can be provided, but only the first will be used, nargs = '?' caused errors
parser.add_argument("-d", "--draw", perf="perform", dest="outputpng", action=Const_Plus_Args, const=2, help='''Draw the molecule in pymol, highlighting secondary structure,
Output pngs of the cartoon and line representations.  
The file name will be based on the input file specified with an argument.
To use this option, you will need the pymol module installed.''')
# -s puts the value 3 into 'perform' and its arguments into 'chain'
parser.add_argument("-s", "--sequence", perf="perform", dest="chain", action=Const_Plus_Args, const=3, help='''Find the sequence residues missing from the structure.
Produce a fasta file containing the NCBI sequence of the protein those residues shown in lower case. 
The file will be named after the input file.  
If no argument is provided, chain A will be inspected.''')
# parse the arguments to the object args
args = parser.parse_args()

# check that the input file exists using checking.py module
input_file = checkInput(args.input)


#---------------------------------------------------------------------------------------------------------------------
# Close if no functions were chosen

# check whether args.perform exists
try:
    args.perform
except AttributeError:
    # if not, inform the user and exit
    print("No functions were chosen to be performed!  \nUse the argument -h for more information!")
    sys.exit(0)


#---------------------------------------------------------------------------------------------------------------------
# Find the distance between the selected atoms

if 1 in args.perform:

    # print section heading
    print ("Distance calculation\n____________________")
    # open file safely and put the information into a list
    with open(input_file) as pdb:
        content = pdb.readlines()
    # loop through arguments
    for atom in args.atoms:
        print("\nCalculating distance between:")
        # for each argument, unpack it into the separate atoms, then return the line number for the two atoms within the file
        startpos, endpos = parse_arguments(atom, content)

        # if the function completed correctly
        if not startpos == -1 and not endpos == -1:
            # calculate the distance between the atoms, and print it
            print("Distance between atoms: ", calculate_distance(content, startpos, endpos))
        else:
            # if there was an error, inform the user
            print("Calculation not performed")

    print ("\n")
#---------------------------------------------------------------------------------------------------------------------
# Draw the molecule using pymol, highlighting the secondary structural elements.  Export pngs of cartoon and line representations.

if 2 in args.perform:
    # print section heading
    print("Drawing molecule\n________________\n")
    # set the output filename based on the argument provided, or the input filename if no argument was provided
    if args.outputpng:
        output_fname = args.outputpng[0]
    else:
        output_fname = input_file.split(".")[0]
    # run pymol with the -q and -c arguments to suppress the startup messages, and run without gui
    __main__.pymol_argv=["pymol", "-qc"]
    # finish launching pymol
    finish_launching()
    # colour the background white
    cmd.bg_color("white")
    # load the input file
    cmd.load(input_file)
    # colour strands blue
    cmd.colour("Blue", "ss s")
    # colour helices yellow
    cmd.colour("Yellow", "ss h")
    # export a png with the cartoon representation
    cmd.show("cartoon","all")
    cmd.png(output_fname+"_cartoon")
    # wait for the export command to finish
    time.sleep(2)

    # hide the cartoon representation
    cmd.hide("everything","all")

    # export a png with the line representation
    cmd.show("lines","all")
    cmd.png(output_fname+"_lines")
    # wait for the export command to finish
    time.sleep(2)
    print("\n")
#---------------------------------------------------------------------------------------------------------------------

if 3 in args.perform:
    # print section heading
    print("Determining Missing Residues\n____________________________\n")
    # open file safely and put the information into a list
    with open(input_file) as file:
        content = file.readlines()
    # set an email address for Entrez to avoid warning messages
    Entrez.email = "A.N.Other@example.com"
    # get the accession numbers for each selected chain, badchains contains the names of chains that were not found.
    accessions, badchains = seqin.get_id(content, args.chain)
    # compare the chain arguments (if present) with badchains, removing those that are not present in the file
    chains = []
    # if there were chain arguments
    if args.chain:
        # check each argument
        for chain in args.chain:
            # if the argument is not in the list of chains that do not exist
            if not chain in badchains:
                # add the chain to the chains variable
                chains.append(chain)

    # if there are no chain arguments
    else:
        # add the first chain in the DBREF section to the chains list
        chains.append(seqin.get_refs(content, r"^DBREF")[0][12])

    # if there is nothing in chains after comparison with badchains
    if not chains:
        # close the program
        sys.exit(0)
    # get the ncbi files of the selected sequences through Entrez
    result = Entrez.efetch(db="protein", id=accessions, rettype="fasta")

    # get the sequences within the structures from the pdb file
    sequences = seqin.get_structure_seq(content, chains)

    # get the sequences from the ncbi files
    ncbiSeqs = seqin.extract_seqs(result, sequences)
    # open the output file safely so that it can be written to
    with open(input_file.split(".")[0] + ".fasta", "w") as output_file:
        # loop through each required sequence
        for i in range(len(sequences)):
            # compare the structure sequence with the ncbi sequence, and output the sequence with missing residues in lower case
            outputseq = seqin.compare_sequences(sequences[i], ncbiSeqs[i])
            # if there were no errors
            if not outputseq == -1:
                # print the sequence, and output it to the fasta file
                print ("Sequence with missing residues in lower case for chain", chains[i] + ":")
                print (outputseq)
                output_file.write(">Chain " + chains[i] + "\n" + outputseq + "\n")


