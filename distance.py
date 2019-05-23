# A module containing the functions for calculating the c-c_alpha distance
#---------------------------------------------------------------------------------------------------------------------
import re
from math import sqrt


def calculate_distance(cnum,content):
    print("\n ")
    print("C alpha coordinates:")
    ca = get_coords(re.finditer("(\d|-).{0,3}\.", content[cnum-1]), content[cnum-1])
    print("C coordinates:")
    c = get_coords(re.finditer("(\d|-).{0,3}\.", content[cnum]), content[cnum])
    return sqrt(pow(c["x"]-ca["x"],2) + pow(c["y"]-ca["y"],2) + pow(c["z"]-ca["z"],2))


def get_coords(nums, line):
    c = {}
    c["x"] = float(re.split(r"\s",line[nums.__next__().start():])[0])
    c["y"] = float(re.split(r"\s",line[nums.__next__().start():])[0])
    c["z"] = float(re.split(r"\s",line[nums.__next__().start():])[0])
    print(c)
    return c


def find_position(content, chain, residue, atom):
    endpos, startpos = get_residue(chain,content,residue)

    try:
        # check if the atom variable is a number
        pos = int(atom)
        # if so find that atom number out of the residue
        if startpos + (pos-1) > endpos:
            print("Residue ", residue, " from chain ", chain, " does not have atom number ", pos)
            return -1
        else:
            return startpos + pos

    except ValueError:
        # otherwise it will be a string
        for i in range(startpos, endpos):
            found = re.search(atom, content[i][14:17])
            if found:
                return i
    return -1

def get_residue(chain,content,residue):
    startpos=0
    endpos=0
    inres=False
    for i in range(0,len(content)):
        line=content[i]
        if re.search('^ATOM',line) and re.search(chain,line[21:23]) and re.search(residue,line[23:27]):
            if not inres:
                print("found start")
                startpos=i
                inres=True
        elif inres:
            endpos=i-1
            break

        if i==len(content) and startpos==0:
            # should never reach this point
            print("No atoms in provided file")
            import sys
            sys.exit(0)
    return endpos,startpos
