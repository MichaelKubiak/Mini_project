# A module containing the functions and variables for finding which amino acids are present in a structure
#---------------------------------------------------------------------------------------------------------------------
import re



def get_refs(content, pattern):
    references=[]
    inref=False
    for line in content:
        if re.search(pattern,line):
            references.append(line)
            inref=True
        elif inref:
            break
    return references


def get_id(content, chains):
    references = get_refs(content, "^DBREFS")

    if chains:
        accessions = []
        for chain in chains:
            for line in references:
                if re.search("\s"+chain+"\s", line):
                    accessions.append(line[33:42].strip(" "))
        return accessions
    else:
        return references[0][33:42].strip(" ")



def get_structure_seq(content, chains):
    seqreslines = get_refs(content, "^SEQRES")

    acids=[]
    if chains:
        for chain in chains:
            for line in seqreslines:
                if re.search("\s"+chain+"\s",line):
                    acids.append(line[19:70].split(" "))
        sequence = ''
        for line in acids:
            for acid in line:
                if not acid is '':
                    sequence += abrevdict[acid]
        return sequence



abrevdict = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
    'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
    'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
    'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
    'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
}
