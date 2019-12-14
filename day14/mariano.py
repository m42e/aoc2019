#!/usr/bin/python3
import os
from time import sleep
import math

file = open("data/data.txt", "r")
lines = file.read().splitlines()
file.close()

E = {}

for l in lines:
    f,t = l.split(" => ")
    tc, tn = t.split(" ")
    tc = int(tc)
    f = f.split(", ")
    f = [x.split(" ") for x in f]
    f = dict(zip([a[1] for a in f], [int(a[0]) for a in f]))
    assert (tc,tn) not in E
    E[tn] = (tc, f)

L = {}
def getLevel(e):
    assert e is not str
    if (e == "ORE"):
        return 0
    else:
        if e in L:
            return L[e]
        else:
            L[e] = max([getLevel(e) for e in E[e][1]]) + 1
        return L[e]

N = {}

def getMaxLevel():
    global N
    max = -1
    maxkey = ""
    #print(N)
    for key in N:
        #print(key, getLevel(key))
        if (getLevel(key) > max):
            max = getLevel(key)
            maxkey = key
    
    #print(maxkey)
    return maxkey
        

def ore(c,e):
    global N
    if e in N:
        del N[e]
    mul = int(math.ceil(c/E[e][0]))
    ans = E[e][1]
    for key in ans:
        if key not in N:
            N[key] = 0
        N[key] += ans[key] * mul
    
    key = getMaxLevel()
    if (key == "ORE"):
        return
    ore(N[key], key)
    
def getOre(n):
    global N
    ore(n, "FUEL")
    tmp = N['ORE']
    N.clear()
    return tmp

print("Part1: ", str(getOre(1)))
if (1):
    nr = 1
    step = 1000000
    while step > 0:
        while getOre(nr) < 1000000000000:
            nr += step
        nr -= step
        step = step // 2

    print("Part2:", nr)
