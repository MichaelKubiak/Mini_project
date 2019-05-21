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


def find_positions(content):
    lastLine = ""
    atoms = []
    firstAtom = []
    chains = []
    firstAtom.append(0)
    newChain = False
    i = 0
    for line in content:
        if re.search("^ATOM", line):
            if not line[21] in chains:
                chains.append(line[21])
            if newChain:
                newChain = False
                firstAtom.append(firstAtom[i-1] + int(re.search('\s\d+\s', line).group()))
            
            if re.search("^C\s", line[13:15]) and re.search("^CA\s", lastLine[13:16]):
                m = re.search("\d", line)
                atoms.append(re.split(r"\s.", line[m.start():])[0])
        elif atoms == []:
            firstAtom[0] += 1
        elif newChain:
            break
        elif re.search("^TER", line):
            newChain = True
            i += 1
        lastLine = line
    return [firstAtom, chains, atoms]
