# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 11:39:17 2018

@author: Jarnd
"""

import qecc as qe
import numpy as np
import random as rnd

nq = 3 # number of qubits
ng = 9


S1 = qe.Pauli('ZII')
S2 = qe.Pauli('IZI')
S3 = qe.Pauli('IIZ')

stablist = [S1,S2,S3]

gates = [0]*ng

## Circuit
gates[0] = [0,2,'CX']
gates[1] = [2,0,'CX']
gates[2] = [0,2,'CX']
gates[3] = [0,1,'CX']
gates[4] = [1,0,'CX']
gates[5] = [0,1,'CX']
gates[6] = [1,2,'CX']
gates[7] = [2,1,'CX']
gates[8] = [1,2,'CX']

## Implement extra gates
gates.insert(0,[0,'H'])



## Run through circuit
def run_circuit(stablist,gates):
    for i in range(len(stablist)):
        for gate in gates:
            if gate[-1] == 'CX':
                stablist[i] = qe.cnot(nq,gate[0],gate[1]).conjugate_pauli(stablist[i])
            elif gate[-1] == 'CXf':
                stablist[i] = qe.cnot(nq,gate[0],gate[1]).conjugate_pauli(stablist[i])
            elif gate[-1] == 'H':
                stablist[i] = qe.hadamard(nq,gate[0]).conjugate_pauli(stablist[i])
            elif gate[-1] == 'X' or gate[-1] == 'Y' or gate[-1] == 'Z':
                stablist[i] = appl_pauli(nq,gate[0],gate[-1],stablist[i])
    return stablist

def appl_pauli(nq,qn,g,stab):
    pau = ['I']*nq
    pau[qn] = g
    return stab*qe.Pauli(''.join(pau))

def faulty_cx(nq,c,t,stab,p):
    stab = qe.cnot(nq,c,t).conjugate_pauli(stab)
    stab = appl_pauli(nq,c,random_pauli(p),stab)
    stab = appl_pauli(nq,t,random_pauli(p),stab)
    
def random_pauli(p):
    choices = ['I','X','Y','Z']
    weights = [1-p,p/3,p/3,p/3]
    return rnd.choices(choices,weights)

print(stablist)