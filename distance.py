# A module containing the functions for calculating the distance between atoms
#---------------------------------------------------------------------------------------------------------------------
import re
from math import sqrt


def parse_arguments(atom, content):
    if re.search(':', atom):  # if both atoms are specified
        # split up the atom pair
        atoms = atom.split(':')
        # find the coordinates of each atom, stopping if the residue is not present

        startpos = find_position(content, atoms[0])
        if startpos == -1:
            return -1, -1
        endpos = find_position(content, atoms[1])
        if endpos == -1:
            return -1, -1

    else:  # if only the first atom is specified
        # find the coordinates of the atom, stopping if the residue is not present
        startpos = find_position(content, atom)
        if startpos == -1:
            return -1, -1
        else:
            print("and the next atom in the structure")
        endpos = startpos + 1

    return startpos, endpos


def calculate_distance(content, startpos, endpos):
    atom1 = re.search(r"\w{,3}", content[startpos][13:16]).group()
    atom2 = re.search(r"\w{,3}", content[endpos][13:16]).group()
    print("\n" + atom1, "coordinates:")
    a1 = get_coords(re.finditer(r"(\d|-).{0,3}\.", content[startpos]), content[startpos])
    print (a1)
    print(atom2, "coordinates:")
    a2 = get_coords(re.finditer(r"(\d|-).{0,3}\.", content[endpos]), content[endpos])
    print(a2)
    return sqrt(pow(a2["x"]-a1["x"], 2) + pow(a2["y"]-a1["y"], 2) + pow(a2["z"]-a1["z"], 2))


def get_coords(nums, line):
    c = {}
    c["x"] = float(re.split(r"\s", line[nums.__next__().start():])[0])
    c["y"] = float(re.split(r"\s", line[nums.__next__().start():])[0])
    c["z"] = float(re.split(r"\s", line[nums.__next__().start():])[0])
    return c


def find_position(content, atom):
    atom = atom.split(',')
    if len(atom) == 3:
        resend, resstart = get_residue(content, atom[0], atom[1])
        if resend == -1 or resstart == -1:
            return -1
        try:
            # check if the atom variable is a number
            pos = int(atom[2])
            # if so find that atom number out of the residue
            if not resstart + pos > resend:
                print ("Atom number", atom[2], "from residue", atom[1], "in chain", atom[0])
                return resstart + pos

        except ValueError:
            # otherwise it will be a string
            for i in range(resstart, resend):
                if re.search(r'\s'+atom[2]+r'\s', content[i][12:18]):
                    print(atom[2], "from residue", atom[1], "in chain", atom[0])
                    return i
        print("Residue", atom[1], "from chain", atom[0], "does not have atom", pos)

        return -1
    else:
        print("Incorrectly formatted atom reference, please ensure that each atom reference is formatted as [Chain],[Residue number],[Atom]")
        return -1


def get_residue(content, chain, residue):
    startpos = 0
    endpos = 0
    inres = False
    for i in range(0, len(content)):
        line = content[i]
        if re.search(r'^ATOM', line) and re.search(chain, line[21:23]) and re.search(residue, line[23:27]):
            if not inres:
                startpos = i-1
                inres = True
        elif inres:
            endpos = i-1
            break

        if i + 1 == len(content) and startpos == 0:
            print("Chain", chain + ", residue", residue, "not found")
            return -1,-1
    return endpos, startpos
