# A module containing the functions and variables for finding which amino acids are present in a structure
#---------------------------------------------------------------------------------------------------------------------
import re


def get_refs(content, pattern):
    references = []
    inref = False
    for line in content:
        if re.search(pattern,line):
            references.append(line)
            inref = True
        elif inref:
            break
    return references


def get_id(content, chains):
    references = get_refs(content, "^DBREF")

    if chains:
        accessions = []
        for chain in chains:
            for line in references:
                if re.search("\s"+chain+"\s", line):
                    accessions.append(line[33:42].strip(" "))
        return accessions
    else:
        return references[0][33:42].strip(" ")


def getSequence(acids):
    sequence = ''
    for line in acids:
        for acid in line:
            if acid is not '':
                sequence+=abrevdict[acid]
    return sequence


def get_structure_seq(content, chains):
    seqreslines = get_refs(content, "^SEQRES")
    sequences=[]
    if chains:

        for chain in chains:
            acids=[]
            for line in seqreslines:
                if re.search("\s"+chain+"\s", line):
                    acids.append(line[19:70].split(" "))
            sequence = getSequence(acids)
            sequences.append(sequence)

    else:
        chain = seqreslines[0][11:15]
        for line in seqreslines:
            if re.search(chain, line):
                acids.append(line[19:70].split(" "))
        sequence = getSequence(acids)
        sequences.append(sequence)
    return sequences


abrevdict = {

    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
    'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
    'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
    'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
    'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
}


def extract_seqs(result, sequences):

    entrezresults = result.readlines()
    results = []
    j = 0
    k = 0
    for i in range(len(sequences)):

        for line in entrezresults[j:]:
            if line.startswith(">") and j > k:
                k = j
                break
            elif not line.startswith(">"):
                results[i] += line
                j += 1
            else:

                j += 1
                results.append("")
    ncbiSeqs=[]
    for seq in results:
        ncbiSeqs.append(seq.replace("\n", ""))
    return ncbiSeqs


def find_structure_seq(sequences, ncbiSeqs):
    from alignment import align

    for i in range (len(sequences)):

        print(align(sequences[i],ncbiSeqs[i]))
