# A module containing the functions for calculating the distance between atoms
#---------------------------------------------------------------------------------------------------------------------
# Impor required modules

import re
from math import sqrt


#---------------------------------------------------------------------------------------------------------------------
# Functions for getting the line numbers of specific atoms

# a method to split arguments into pairs of atoms and return the line number for each atom
def parse_arguments(atom, content):
    if re.search(':', atom):  # if both atoms are specified
        # split up the atom pair
        atoms = atom.split(':')

        # find the line number of each atom
        startpos = find_position(content, atoms[0])
        # propagate an error code if the atom is not present
        if startpos == -1:
            return -1, -1
        endpos = find_position(content, atoms[1])
        if endpos == -1:
            return -1, -1

    else:  # if only the first atom is specified
        # find the line number of the atom
        startpos = find_position(content, atom)
        # propagate an error code if the atom is not present
        if startpos == -1:
            return -1, -1
        else:
            print("and the next atom in the structure")
        # set the value for the other atom to the next line in the file, which will contain the next atom
        endpos = startpos + 1

    return startpos, endpos


# a method to split an atom entry into chain, residue and atom, then find and return the line number of that atom
def find_position(content, atom):
    # split the entry
    splitatom = atom.split(',')
    # check that the entry has the correct number of sections
    if len(splitatom) == 3:
        # get the start and end of the residue in which the atom resides
        resend, resstart = get_residue(content, splitatom[0], splitatom[1])
        # propagate an error code if the residue is not present
        if resend == -1 or resstart == -1:
            return -1
        try:
            # check whether the atom variable (splitatom[2]) is an integer
            pos = int(splitatom[2])
            # check that that number of atoms are present in the residue
            if not resstart + pos > resend:
                print("Atom number", splitatom[2], "from residue", splitatom[1], "in chain", splitatom[0])
                # return the line number
                return resstart + pos

        except ValueError:
            # otherwise it will be a string containing the atom type
            for i in range(resstart, resend):
                # find which line of the residue contains that string
                if re.search(r'\s' + splitatom[2] + r'\s', content[i][12:18]):
                    print(splitatom[2], "from residue", splitatom[1], "in chain", splitatom[0])
                    # return that line number
                    return i
        # if the atom is not present, inform the user and return an error code
        print("Residue", splitatom[1], "from chain", splitatom[0], "does not have atom", pos)

        return -1
    # the entry did not have the correct number of sections, it was incorrectly formatted, inform the user and return an error code
    else:
        print("Incorrectly formatted atom reference, please ensure that each atom reference is formatted as [Chain],[Residue number],[Atom]")
        return -1

# a method for finding the start and end line positions of a residue in the pdb file
def get_residue(content, chain, residue):
    resstart = 0
    resend = 0
    inres = False
    # loop through the pdb file lines by number
    for i in range(0, len(content)):
        line = content[i]
        # check whether the line is an atom and has the correct chain and residue identifiers
        if re.search(r'^ATOM', line) and re.search(chain, line[21:23]) and re.search(residue, line[23:27]):
            # if this is the first line in the residue
            if not inres:
                # set the start line number and the boolean that shows that the residue has started
                resstart = i-1
                inres = True
        # if the residue has started, but the current line is not part of it, the residue has ended
        elif inres:
            # set the line number of the end of the residue, and break the for loop
            resend = i-1
            break

        # if the end of the file is reached while the residue has not begun, the residue is not present
        if i + 1 == len(content) and resstart == 0:
            # inform the user and return an error code
            print("Chain", chain + ", residue", residue, "not found")
            return -1, -1
        # if the end of the file is reached within a residue, the residue ends here
        elif i + 1 == len(content):
            # set the line number of the end of the residue
            resend = i
    # return the line numbers of the end and start of the residue
    return resend, resstart


#---------------------------------------------------------------------------------------------------------------------
# Functions for calculating the distance between atoms on known lines of the file

# a function to get the coordinates from two lines of a pdb file and calculate the distance between the atoms
def calculate_distance(content, startpos, endpos):
    # get the atom type from each line
    atom1 = re.search(r"\w{,3}", content[startpos][13:16]).group()
    atom2 = re.search(r"\w{,3}", content[endpos][13:16]).group()
    # get and print the coordinates from each line
    print("\n" + atom1, "coordinates:")
    a1 = get_coords(re.finditer(r"(\d|-).{0,3}\.", content[startpos]), content[startpos])
    print(a1)
    print(atom2, "coordinates:")
    a2 = get_coords(re.finditer(r"(\d|-).{0,3}\.", content[endpos]), content[endpos])
    print(a2)
    # return the calculated distance between the coordinates of the two atoms
    return sqrt(pow(a2["x"]-a1["x"], 2) + pow(a2["y"]-a1["y"], 2) + pow(a2["z"]-a1["z"], 2))


# a function to get the coordinates on a line of a pdb file
def get_coords(nums, line):
    # make a dictionary to contain the coordinates for each axis
    c = dict()
    # get the coordinates for each axis
    c["x"] = float(re.split(r"\s", line[nums.__next__().start():])[0])
    c["y"] = float(re.split(r"\s", line[nums.__next__().start():])[0])
    c["z"] = float(re.split(r"\s", line[nums.__next__().start():])[0])
    # return the dictionary
    return c


