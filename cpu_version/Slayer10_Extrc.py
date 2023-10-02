import hashlib

reduced = True
def fn(string, reduced = True):
    s = hashlib.md5(string.encode('utf-8')).hexdigest()
    if reduced:
        return s[:SLAY] + s[-SLAY:]
    return s

x, y = None, None
seq0, seq1 =  ['QFF=CQZ:[]`P==', 8139761], ['4Y`[aA>]F:2P38', 2158850] 
SLAY = len(seq0[0])//2

if seq0[-1] > seq1[-1]:
    x, y = seq0[0], seq1[0]
    while seq0[-1] > seq1[-1]:
        x = fn(x)
        seq0[-1] -= 1

if seq0[-1] < seq1[-1]:
    x, y = seq1[0], seq0[0]
    while seq0[-1] < seq1[-1]:
        x = fn(x)
        seq1[-1] -= 1

while seq0[-1] and fn(x) != fn(y):
    x, y = fn(x), fn(y)
    seq0[-1] -= 1
print(f'Result ~ [{x}: {fn(x, reduced = False)}]  [{y}: {fn(y, reduced = False)}]')
