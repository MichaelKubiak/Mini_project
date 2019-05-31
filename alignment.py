# Alignment module, since mafft requires files containing the correct information, based on Needleman-Wunsch algorithm,
# and the java alignment program provided for an algorithms assignment
#---------------------------------------------------------------------------------------------------------------------

d=8

blosumChars=['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V']

BLOSUM50=[
    [5,-2,-1,-2,-1,-1,-1,0,-2,-1,-2,-1,-1,-3,-1,1,0,-3,-2,0],
    [-2,7,-1,-2,-4,1,0,-3,0,-4,-3,3,-2,-3,-3,-1,-1,-3,-1,-3],
    [-1,-1,7,2,-2,0,0,0,1,-3,-4,0,-2,-4,-2,1,0,-4,-2,-3],
    [-2,-2,2,8,-4,0,2,-1,-1,-4,-4,-1,-4,-5,-1,0,-1,-5,-3,-4],
    [-1,-4,-2,-4,13,-3,-3,-3,-3,-2,-2,-3,-2,-2,-4,-1,-1,-5,-3,-1],
    [-1,1,0,0,-3,7,2,-2,1,-3,-2,2,0,-4,-1,0,-1,-1,-1,-3],
    [-1,0,0,2,-3,2,6,-3,0,-4,-3,1,-2,-3,-1,-1,-1,-3,-2,-3],
    [0,-3,0,-1,-3,-2,-3,8,-2,-4,-4,-2,-3,-4,-2,0,-2,-3,-3,-4],
    [-2,0,1,-1,-3,1,0,-2,10,-4,-3,0,-1,-1,-2,-1,-2,-3,2,-4],
    [-1,-4,-3,-4,-2,-3,-4,-4,-4,5,2,-3,2,0,-3,-3,-1,-3,-1,4],
    [-2,-3,-4,-4,-2,-2,-3,-4,-3,2,5,-3,3,1,-4,-3,-1,-2,-1,1],
    [-1,3,0,-1,-3,2,1,-2,0,-3,-3,6,-2,-4,-1,0,-1,-3,-2,-3],
    [-1,-2,-2,-4,-2,0,-2,-3,-1,2,3,-2,7,0,-3,-2,-1,-1,0,1],
    [-3,-3,-4,-5,-2,-4,-3,-4,-1,0,1,-4,0,8,-4,-3,-2,1,4,-1],
    [-1,-3,-2,-1,-4,-1,-1,-2,-2,-3,-4,-1,-3,-4,10,-1,-1,-4,-3,-3],
    [1,-1,1,0,-1,0,-1,0,-1,-3,-3,0,-2,-3,-1,5,2,-4,-2,-2],
    [0,-1,0,-1,-1,-1,-1,-2,-2,-1,-1,-1,-1,-2,-1,2,5,-3,-2,0],
    [-3,-3,-4,-5,-5,-1,-3,-3,-3,-3,-2,-3,-1,1,-4,-4,-3,15,2,-3],
    [-2,-1,-2,-3,-3,-1,-2,-3,2,-1,-1,-2,0,4,-3,-2,-2,2,8,-1],
    [0,-3,-3,-4,-1,-3,-3,-4,-4,4,1,-3,1,-1,-3,-2,0,-3,-1,5]
]

charToIndex = []

for i in range (26):
    charToIndex.append(-1)

for i in range(len(blosumChars)):
    charToIndex[ord(blosumChars[i])-ord('A')]=i

def s(x,y):
    if ord(x) < ord('A') or ord(x) > ord('Z'):
        print (x, "is not a legal charachter, alignment is not possible")
        return "error"
    if ord(y) < ord('A') or ord(y) > ord('Z'):
        print(y,"is not a legal charachter, alignment is not possible")
        return "error"

    ix = ord(x)-ord('A')
    iy = ord(y)-ord('A')

    if charToIndex[ix] == -1:
        print(x, "is not a legal charachter, alignment is not possible")
        return "error"
    if charToIndex[iy] == -1:
        print(y, "is not a legal charachter, alignment is not possible")
        return "error"
    return BLOSUM50[charToIndex[ix]][charToIndex[iy]]


def gamma(g):

    return -g*d


def align(seq1, seq2):

    T = 1
    L = 2
    D = 3

    n = len(seq1)
    m = len(seq2)
    F = []
    P = []

    for i in range (n+1):
        F.append([])
        P.append([])
        for j in range (m+1):
            F[i].append(0)
            P[i].append(0)

    for i in range(n+1):
        for j in range(m+1):
            if i == 0 and j == 0:
                F[i][j] = 0
            elif i == 0:
                F[i][j] = -j*d
                P[i][j] = L
            elif j == 0:
                F[i][j] = -i*d
                P[i][j] = T
            else:
                match_score = s(seq1[i-1], seq2[j-1])
                if match_score == "error":
                    return False
                diag = F[i-1][j-1] + match_score
                left = F[i][j-1] - d
                top = F[i-1][j] - d

                if diag >= left and diag >= top:
                    F[i][j] = diag
                    P[i][j] = D
                elif left >= diag and left >= top:
                    F[i][j] = left
                    P[i][j] = L
                else:
                    F[i][j] = top
                    P[i][j] = T

    Xa = ""
    Ya = ""
    i = n
    j = m

    while i+j > 0:
        if P[i][j] == D:
            Xa = seq1[i-1] + Xa
            Ya = seq2[j-1] + Ya
            i -= 1
            j -= 1
        elif P[i][j] == T:
            Xa = seq1[i-1] + Xa
            Ya = '-' + Ya
            i -= 1
        else:
            Xa = '-' + Xa
            Ya = seq2[j-1] + Ya
            j -= 1
    return Xa, Ya

