# A module containing the functions and variables for finding which amino acids are present in a structure
#---------------------------------------------------------------------------------------------------------------------
# Import required modules

import re
from alignment import align


#---------------------------------------------------------------------------------------------------------------------
# Functions to get the accession numbers of the chains

# a function to get the accession numbers of the chains provided as an argument
def get_id(content, chains):
    # get the lines that begin with DBREF, these lines contain the accession numbers
    references = get_refs(content, r"^DBREF")

    # if chains contains any chain names, get the accession numbers for those chains
    if chains:
        accessions = []
        i = 0
        badchains = []

        for chain in chains:
            i += 1
            for line in references:
                # check whether each line in references has the chain name in it, if it does add the accession number to the list of accession numbers
                if re.search(r"\s"+chain+r"\s", line):
                    accessions.append(line[33:42].strip(" "))
            # if no line has been found with that chain name
            if len(accessions) < i:
                # inform the user and add the chain name to the badchains list, which will be used to remove chains that do not exist from args.chains
                print("Chain", chain, "is not present in file, it will be ignored")
                i -= 1
                badchains.append(chain)
        return accessions, badchains
    # if there were no chains specified in arguments, use the first chain in the file
    else:
        return references[0][33:42].strip(" "), []


# a function to return a list of consecutive lines containing a certain Regex pattern from a list of lines
def get_refs(content, pattern):
    references = []
    inref = False
    # checks each line in the list for whether they match the pattern
    for line in content:
        if re.search(pattern, line):
            # if they match, they are appended to the new list, and it is recorded that the section has begun
            references.append(line)
            inref = True
        elif inref:
            # if the section has begun, and the current line does not match the pattern, break out of the loop
            break
    return references


#---------------------------------------------------------------------------------------------------------------------
# Functions to determine the sequence of the structure in the pdb file

# a function to get the structure of the selected chains from the pdb file
def get_structure_seq(content, chains):
    # get the lines starting in SEQRES, which contain the sequence of residues
    seqreslines = get_refs(content, r"^SEQRES")
    sequences = []
    acids = []

    for chain in chains:
        # for each line starting in SEQRES,
        for line in seqreslines:
            # if the line contains the chain name, append each amino acid on that line to the list of acids
            if re.search(r"\s"+chain+r"\s", line):
                acids.append(line[19:70].split(" "))
        # Change the list of 3 letter abreviations into a sequence of 1 letter codes
        sequence = getSequence(acids)
        # add each sequence to the list of sequences to be returned
        sequences.append(sequence)

    return sequences

# a function to convert a list of 3 letter abreviations to a sequence of 1 letter codes
def getSequence(acids):
    sequence = ''
    # for each 3 letter code, look up the 1 letter code in the dictionary abrevdict
    for line in acids:
        for acid in line:
            if acid is not '':
                sequence += abrevdict[acid]
    return sequence

# a dictionary of 3 letter codes to 1 letter codes
abrevdict = {

    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
    'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
    'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
    'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
    'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
}


#---------------------------------------------------------------------------------------------------------------------
# Function to get the sequence from the file returned by entrez

# a function to extract a sequence from an entrez file object
def extract_seqs(result, sequences):

    entrezresults = result.readlines()
    results = []
    j = 0
    k = 0
    # for each structure sequence
    for i in range(len(sequences)):
        # concatenate each set of lines between headers (starting with ">") and add them to the list of results
        for line in entrezresults[j:]:
            # if the next header is reached, leave the loop
            if line.startswith(">") and j > k:
                k = j
                break
            # if the line is not a header, add it to the current set of results
            elif not line.startswith(">"):
                results[i] += line
                j += 1
            # if the line is the current header, add a new empty string to the results
            else:
                j += 1
                results.append("")

    ncbiSeqs = []
    # for each result, remove the /n characters
    for seq in results:
        ncbiSeqs.append(seq.replace("\n", ""))
    return ncbiSeqs


#---------------------------------------------------------------------------------------------------------------------
#Function to determine which residues are not present in the structure sequence compared to the ncbi sequence

# a function to compare the ncbi sequences with the structure sequences and determine which residues are missing
def compare_sequences(sequence, ncbiSeq):
    # the available commandline alignment software required fasta file names to be provided,
    # so an alignment method was required that would take sequences as input
    seqs = align(sequence, ncbiSeq)
    # propagates errors from the alignment process
    if seqs is False:
        return -1
    # separate the returned tuple
    seq, ncbiSeq = seqs

    outputSeq = ""

    # add each residue to the output sequence, taking uppercase letters from the structure sequence where they are present,
    # and lowercase letters from the ncbi sequence where no structure sequence is present
    for i in range(len(seq)):
        if seq[i] == "-":
            outputSeq += ncbiSeq[i].lower()
        else:
            outputSeq += seq[i]

    return outputSeq
