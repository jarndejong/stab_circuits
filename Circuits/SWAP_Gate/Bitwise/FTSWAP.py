# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 15:13:21 2018

@author: Jarnd
"""



import random as rnd
import numpy as np

import MEP.Functions.circuitfunctions.py as cf
import MEP.Functions.stab_group_functions.py as sf

nq = 3 # number of qubits
ng = 9
p_m = 0
p_s = 0


S1 = sf.pauli_to_bitstring('ZII')
S2 = sf.pauli_to_bitstring('IZI')
S3 = sf.pauli_to_bitstring('ZZZ')


stablist = [S1,S2,S3]
phases = np.array([0,0,0])
stab_group = sf.stabgroup(stablist)

state = [stab_group,phases]

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
gates.insert(0,[1,'H'])


state = cf.run_circuit(nq,state,gates,p_m,p_s)

