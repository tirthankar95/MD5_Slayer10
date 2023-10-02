import random 
import hashlib
from multiprocessing import Process, Manager, Value, Lock
import math 
import os

class Seq:
    def __init__(self, start, cnt):
        self._start_ = start 
        self._cnt_ = cnt 

SLAY, num_processes = 7, os.cpu_count()

'''
# Rate ~ 1 distinguised point every 1 min.(Assume)
# 1 sec ~ 10**7 iterations.(Assume)
# => 1 min ~ 10**8 iterations.
'''
theta = 1/1e6

def randomSt():
    mxLen = 2*SLAY
    chrSet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']# HEX FAMILY
    res = ""
    for indx in range(mxLen):
        res = res + chrSet[random.randint(0, len(chrSet) - 1)] 
    return res 

def fn(string, reduced = True):
    s = hashlib.md5(string.encode('utf-8')).hexdigest()
    if reduced:
        return s[:SLAY] + s[-SLAY:]
    return s

def dist_prop(string) -> bool:
    prefix_str = "a5"
    suffix_str = "31"
    return True if string[:len(prefix_str)] == prefix_str and \
                   string[-len(suffix_str):] == suffix_str else False 

def randomWalk(p_id, hashMapSync, seq0, seq1, gFound, lock):
    while not gFound.value:
        s0 = randomSt()
        x, mx_path = s0, math.ceil(1//theta)
        for _ in range(1, mx_path+1):
            if gFound.value: return
            if dist_prop(x):
                # print(f'distnc[{p_id}] ~ {x}')
                if x not in hashMapSync:
                    hashMapSync[x] = [s0, _]
                else:
                    print(f' {[s0, _]}, {hashMapSync[x]} ')
                    with lock:
                        gFound.value = True 
                    seq0 += [s0, _]
                    seq1 += hashMapSync[x]
                    return
            x = fn(x)

if __name__ == '__main__':
    processes, gFound = [], False
    with Manager() as manager:
        hashMapSync = manager.dict()
        gFound = Value('i', False)
        seq0, seq1 = manager.list([]), manager.list([])
        lock = Lock()
        for i in range(num_processes):
            p = Process(target = randomWalk, args = (i,hashMapSync, seq0, seq1, gFound, lock))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()
