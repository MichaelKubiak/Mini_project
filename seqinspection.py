# A module containing the functions and variables for finding which amino acids are present in a structure
#---------------------------------------------------------------------------------------------------------------------
import re
from alignment import align


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
        i = 0
        badchains = []
        for chain in chains:
            i+=1
            for line in references:
                if re.search("\s"+chain+"\s", line):
                    accessions.append(line[33:42].strip(" "))

            if len(accessions)<i:
                print ("Chain", chain, "is not present in file, it will be ignored")
                i += 1
                badchains.append(chain)
        return accessions, badchains
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


def compare_sequences(sequence,ncbiSeq):

    seqs = align(sequence, ncbiSeq)
    if seqs == False:
        return -1

    seq, ncbiSeq = seqs

    outputSeq = ""

    for i in range(len(seq)):
        if seq[i] == "-":
            outputSeq += ncbiSeq[i].lower()
        else:
            outputSeq += seq[i]

    return outputSeq
