# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 15:21:42 2018

@author: Jarnd
"""
import sys
sys.path.append('../Functions')

import stab_group_functions as sf

S1 = 'XXXXIII'
S2 = 'ZZIIZZI'
S3 = 'YIYIYIY'
S4 = 'IZIZIII'
S5 = 'IIXIIIX'
S6 = 'IIIIYYI'


stab1 = sf.pauli_to_bitstring(S1)
stab2 = sf.pauli_to_bitstring(S2)
stab3 = sf.pauli_to_bitstring(S3)
stab4 = sf.pauli_to_bitstring(S4)
stab5 = sf.pauli_to_bitstring(S5)
#stab6 = sf.pauli_to_bitstring(S6)

stab_list = [stab1,stab2,stab3,stab4,stab5]#,stab6]

stab_group = sf.stabgroup(stab_list)
stab_matrix = sf.gen_group_to_matrix(stab_group)
sf.check_stabgroup(stab_group)
logicals = sf.logical_pauli(stab_matrix)

null_basis = sf.nullspace_basis(stab_matrix)

log1 = logicals[0]
log2 = logicals[1]
