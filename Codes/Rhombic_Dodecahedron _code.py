# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 12:00:06 2018

@author: Jarnd
"""

import numpy as np

import Stab_group_functions as stab

stab1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
stab2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1]])
stab3 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0]])
stab4 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]])
stab5 = np.array([[1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
stab6 = np.array([[0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
stab7 = np.array([[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
stab8 = np.array([[0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
stab9 = np.array([[1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],[1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]])
stab10 = np.array([[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0],[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0]])
stab11 = np.array([[0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],[0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0]])
stab12 = np.array([[0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1],[0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1]])


gen_list = (stab1,stab2,stab3,stab4,stab5,stab6,stab7,stab8,stab9,stab10,stab11,stab12);
gen_group = stab.stabgroup(gen_list);
gen_matrix = stab.gen_group_to_matrix(gen_group);

#print(stab.check_stabgroup(gen_group))
#print((stab.list_stabgroup_elements(gen_group,stab1,'P')))
#print(len(stab.list_stabgroup_elements(gen_group,stab1)))
print(gen_matrix)
print('')
print(stab.ech(gen_matrix))