# A module containing the functions and variables for finding which amino acids are present in a structure
#---------------------------------------------------------------------------------------------------------------------
import re


def get_id(content, chains):
    references = get_refs(content)

    if chains:
        accessions=[]
        for chain in chains:
            for line in references:
                if re.search("\s"+chain+"\s", line):
                    accessions.append(line[33:42].strip(" "))
        return accessions
    else:
        return references[0][33:42].strip(" ")


def get_refs(content):
    references=[]
    inref=False
    for line in content:
        if re.search("^DBREF",line):
            references.append(line)
            inref=True
        elif inref:
            break
    return references


def get_structure_seq(content, chains):
    seqreslines = []
    for line in content:
        inseqres = False
        if re.search("^SEQRES", line):
            inseqres = True
            seqreslines.append(line)
        elif inseqres:
            break


abrevdict = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
    'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
    'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
    'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
    'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
}
