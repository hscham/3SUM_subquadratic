import sys, re, math, itertools

A = B = C = L = None
n = g = s = 0
Ldim = Flen = 0
chunklen = blockdim = 0
output = set()

def read_input(inp):
    global A, B, C
    with open(inp, 'r+') as fin:
        A = list(map(int, fin.readline().split()))
        B = list(map(int, fin.readline().split()))
        C = list(map(int, fin.readline().split()))
    if len(A) != len(B) or len(B) != len(C):
        print('Length of A, B, C not the same')
        exit()

def init_var():
    global n, g, s, Ldim, Flen
    n = len(A)
    g = math.ceil(math.log(n) / 11)
    s = math.ceil(g / math.log(g))
    Ldim = math.ceil(n/g)
    Flen = math.ceil(pow(g, 2) / s)
    print('|A| = |B| = |C| = n = %d' % (len(A)))
    print('# chunks = g = %d' % (g))
    print('# elements per chunk = s = %d' % (s))

#def instruction_to_path(instructions):
#    path = []
#    pappend = path.append
#    i = 0
#    j = g
#    for step in instructions:
#        pappend((i, j))
#        if step == 'r': i += 1
#        else: j -= 1
#    return path
#
#def dominance(p, q):
#    for pco, qco in zip(instruction_to_path(p), instruction_to_path(q)):
#        if pco[0] < qco[0] or pco[1] < qco[1]:
#            return False
#    return True
#
#def num_squares_below(path):
#    d = 0
#    dim = g*g
#    ret = dim - d
#    for step in path[1:]:
#        if step == 'd': 
#            d -= 1
#        else:
#            ret += (dim - d)
#    return ret

def square_between(p, q):
    #return sequence of tiles if p dominates q; return None otherwise
    pi = qi = 0
    pj = qj = g
    stepq = 0
    seq = []
    sappend = seq.append
    for step in p:
        while pi > qi and pj > qj:
            for j in range(qj, pj, -1):
                sappend((pi, j))
            if stepq == 'r': pi += 1
            else: pj -= 1
        if pi <= qi and step == 'r': pi += 1
    return seq

def preprocess_blocks():
    global L
    L = [[None for i in range(g*g//s)] for j in range((n//g)*(n//g))]
    for e in range(g*g//s):
        for p in range(g, 2g-1):
            for q in range(g, 2g-1):
                for P in permutations('rd', p):
                    for P_prime in permutations('rd', q):
                        if not dominance(P_prime, P): continue

def main(inp, outp):
    read_input(inp)
    init_var()
    A.sort()
    B.sort()
    preprocess_blocks()
    for c in C:
        lo = 1
        hi = math.ceil(n/g)
        while (lo <= math.ceil(n/g) and hi > 0):
            ab = search_c(lo, hi)
            if ab: 
                print('Triplet %s satisfies equality a[%d] + b[%d] = c[%s]' % ((ab[0], ab[1], c), ab[0], ab[1], c))
                return 0
            else:
                if A_max(lo) + B_min(hi) < c: lo += 1
                else: hi -= 1
    print('No triplet (a,b,c) s.t. a + b = c exist')
    return 1

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
