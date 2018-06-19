# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 15:13:21 2018

@author: Jarnd
"""

import qecc as qe
import random as rnd
import circuitfunctions as cf

nq = 3 # number of qubits
ng = 9
p = 0.01


S1 = qe.Pauli('ZII')
S2 = qe.Pauli('IZI')
S3 = qe.Pauli('IIZ')

stablist = [S1,S2,S3]

gates = [0]*ng

## Circuit
gates[0] = [0,2,'CXf']
gates[1] = [2,0,'CXf']
gates[2] = [0,2,'CXf']
gates[3] = [0,1,'CXf']
gates[4] = [1,0,'CXf']
gates[5] = [0,1,'CXf']
gates[6] = [1,2,'CXf']
gates[7] = [2,1,'CXf']
gates[8] = [1,2,'CXf']

## Implement extra gates
gates.insert(0,[0,'H'])

print(cf.run_circuit(nq,stablist,gates,p))