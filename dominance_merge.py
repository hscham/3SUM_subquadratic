import sys, re

d0 = 0
A = B = None

def read_input(inp):
    global d0, A, B
    with open(inp, 'r+') as fin:
        d0 = int(fin.readline())
        pattern = 'r' + '\s+'.join(['(%d+)'] * d0)
        Nr = int(fin.readline())
        A = [tuple(['r'] + list(map(int, fin.readline().split()))) for i in range(Nr)]
        Nb = int(fin.readline())
        B = [tuple(['b'] + list(map(int, fin.readline().split()))) for i in range(Nb)]
    if any([d0+1 != len(v) for v in (A+B)]):
        print('Incorrect input data! Wrong dimension of input vector!')
        exit()

def median_sort(l):
    l.sort()
    try:
        return l[(len(l)-1)//2]
    except:
        print('error')
        print(l)
        print((len(l)-1)//2)
        exit()

def kmedian(l, k):
    medians = [median_sort(l[i:i+5]) for i in range(0, len(l)//5, 5)]
    m = median(medians)
    L = []
    R = []
    for i in l:
        L.append(i) if i < m else R.append(i)
    if len(L) + 1 == k:
        return m
    elif len(L) + 1 > k:
        return kmedian(L, k)
    else:
        return kmedian(R, k-len(L)+1)

def median(l):
    if len(l) == 1:
        return l[0]
    if len(l) < 5:
        return median_sort(l)
    return kmedian(l, (len(l)-1)//2)

def dominance(d, E, level):
    global output
    print('\t'*level + 'd = %d, len(E) = %d'%(d, len(E)))
    if len(E) == 0:
        print('\t'*level + 'Empty set of vectors')
        return
    if d == 0:
        for u in [u for u in E if u[0] == 'b']:
            for v in [v for v in E if v[0] == 'r']:
                output.add((u,v))
        return
    m = median([v[d] for v in E])
    print('\t'*level + 'median of %dth component = %d' % (d, m))
    L = []
    Sr = []
    Sb = []
    R = []
    for v in E:
        if v[d] < m: L.append(v)
        elif v[d] > m: R.append(v)
        else: Sr.append(v) if v[0] == 'r' else Sb.append(v)
    merged = L + Sr + Sb + R
    H1 = merged[:len(merged)//2]
    H2 = merged[len(merged)//2:]
    withRed = withBlue = False
    for v in H1:
        if v[0] == 'r': withRed = True
        else: withBlue = True
        if withRed and withBlue:
            print('\t'*level + 'H1 has both red and blue vectors')
            dominance(d, H1, level+1)
            break
    withRed = withBlue = False
    for v in H2:
        if v[0] == 'r': withRed = True
        else: withBlue = True
        if withRed and withBlue:
            print('\t'*level + 'H2 has both red and blue vectors')
            dominance(d, H1, level+1)
            break
    if d >= 0:
        print('\t'*level + 'Proceed to (d-1) of E')
        dominance(d-1, [v for v in H1 if v[0] == 'b'] + [v for v in H2 if v[0] == 'r'], level+1)
    return output

def print_output(outp):
    with open(outp, 'w+') as fout:
        fout.write('\n'.join(['%s, %s' % (pair[0], pair[1]) for pair in output]))

def main(inp, outp):
    read_input(inp)
    print('input:\nd0=%d'%(d0))
    for v in A + B:
        print(v)
    global output
    output = set()
    dominance(d0, A + B, 0)
    print_output(outp)
    
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
