# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 11:39:17 2018

@author: Jarnd
"""

import qecc as qe
import random as rnd

## Run through circuit
def run_circuit(nq,stablist,gates,p):
    for i in range(len(stablist)):
        for gate in gates:
            if gate[-1] == 'CX':
                stablist[i] = qe.cnot(nq,gate[0],gate[1]).conjugate_pauli(stablist[i])
            elif gate[-1] == 'CXf':
                stablist[i] = faulty_cx(nq,gate[0],gate[1],stablist[i],p)
            elif gate[-1] == 'H':
                stablist[i] = qe.hadamard(nq,gate[0]).conjugate_pauli(stablist[i])
            elif gate[-1] == 'X' or gate[-1] == 'Y' or gate[-1] == 'Z':
                stablist[i] = appl_pauli(nq,gate[0],gate[-1],stablist[i])
            elif gate[-1] == 'E':
                stablist[i] = appl_pauli(nq,gate[0],random_pauli(p),stablist[i])
    return stablist

def appl_pauli(nq,qn,g,stab):
    pau = ['I']*nq
    pau[qn] = g
    return stab*qe.Pauli(''.join(pau))

def faulty_cx(nq,c,t,stab,p):
    stab = qe.cnot(nq,c,t).conjugate_pauli(stab)
    stab = appl_pauli(nq,c,random_pauli(p),stab)
    stab = appl_pauli(nq,t,random_pauli(p),stab)
    return stab
    
def random_pauli(p):
    choices = ['I','X','Y','Z']
    weights = [1-p,p/3,p/3,p/3]
    return rnd.choices(choices,weights)[0]

def faulty_pauli(nq,qn,g,stab,p):
    stab = appl_pauli(nq,qn,g,stab);
    stab = appl_pauli(nq,qn,random_pauli(p),stab)
    return stab

#def measure_pauli(nq,qn,p,stablist,p):
    