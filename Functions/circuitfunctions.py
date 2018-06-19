# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 11:39:17 2018

@author: Jarnd
"""

import random as rnd
import stab_group_functions as sf
import numpy as np

## Run through circuit
def run_circuit(nq,state,gates,p_m,p_s):
    for gate in gates:
        if gate[-1] == 'CX':
            state = appl_cnot(nq,gate[0],gate[1],state)
        elif gate[-1] == 'CXf':
            state = appl_faulty_cx(nq,gate[0],gate[1],state,p_m)
        elif gate[-1] == 'H':
            state = appl_hadamard(nq,gate[0],state)
        elif gate[-1] == 'X' or gate[-1] == 'Y' or gate[-1] == 'Z':
            state = appl_pauli(nq,gate[0],gate[-1],state)
        elif gate[-1] == 'E':
            state = appl_pauli(nq,gate[0],random_pauli(p_s),state)
        elif gate[-1] == 'Xf' or gate[-1] == 'Yf' or gate[-1] == 'Zf':
            state = appl_faulty_pauli(nq,gate[0],gate[-1][0],state,p_s)
    return state


### Single qubit gates
def appl_pauli(nq,qn,g,state):
    stab_group = state[0]
    phases = state[1]
    pau = ['I']*nq
    pau[qn] = g
    pau = sf.pauli_to_bitstring(''.join(pau))
    Zt = np.vstack((stab_group[0],pau[0]))
    Xt = np.vstack((stab_group[1],pau[1]))
    phase_add = (Zt@Xt.T)[:-1,-1];
    return [stab_group,(phases+2*phase_add)%4]

def appl_faulty_pauli(nq,qn,g,state,p):
    state = appl_pauli(nq,qn,g,state);
    state = appl_pauli(nq,qn,random_pauli(p),state)
    return state

def appl_hadamard(nq,qn,state):
    stab_group = state[0]
    phases = state[1]
    H = np.eye(2*nq)
    H[:, qn], H[:, qn+nq] = H[:, qn+nq], H[:, qn].copy()
    K = np.zeros(2*nq);
    K[qn], K[qn+nq] = 1,1;
    gen_matrix = sf.gen_group_to_matrix(stab_group);
    stab_group = sf.stabgroup(sf.gen_matrix_to_stab_list(gen_matrix@H));
    phases_upd = 2*np.floor(gen_matrix@K/2)
    return [stab_group,(phases+phases_upd)%4]

### Multi-qubit gates
def appl_cnot(nq,c,t,state):
    stab_group = state[0]
    phases = state[1]
    stab_group[0][:,c] += stab_group[0][:,t]
    stab_group[1][:,t] += stab_group[1][:,c]
    return [[stab_group[0]%2,stab_group[1]%2],phases]
    
    
def appl_faulty_cx(nq,c,t,state,p_m):
    state = appl_cnot(nq,c,t,state)
    state = appl_pauli(nq,c,random_pauli(p_m),state)
    state = appl_pauli(nq,t,random_pauli(p_m),state)
    return state

def appl_cz(nq,c,t,state):
    state = appl_hadamard(nq,t,state);
    state = appl_cnot(nq,c,t,state);
    state = appl_hadamard(nq,t,state);
    
def appl_faulty_cz(nq,c,t,state,p_m):
    state = appl_cz(nq,c,t,state)
    state = appl_pauli(nq,c,random_pauli(p_m),state)
    state = appl_pauli(nq,t,random_pauli(p_m),state)
    return state


### Help functions    
def random_pauli(p):
    choices = ['I','X','Y','Z']
    weights = [1-p,p/3,p/3,p/3]
    return rnd.choices(choices,weights)[0]

def initialize_zero_state(nq):
    stab_list = []
    for i in range(nq):
        stab = np.array([np.zeros(nq),np.zeros(nq)])
        stab[0][i] = 1;
        stab_list.append(stab.astype(int))
    phases = np.zeros(nq)
    return [sf.stabgroup(stab_list),phases.astype(int)]

def measure_pauli(nq,pauli,state):
    stab_group = state[0]
    phases = state[1]
    total_space_group = sf.gen_matrix_to_stab_list(sf.gen_group_to_matrix(stab_group));
    total_space_group.append(pauli);
    total_space_group = sf.stabgroup(total_space_group);
    if sf.check_commuting(total_space_group)[0] == True:
        if sf.rank(total_space_group) == sf.rank(stab_group):
            m = 0
            return [[stab_group,phases], m]
        else:
            m = rnd.choice([0,2])
            return [[total_space_group,phases.append(m)],1-m]
    elif sf.check_commuting(total_space_group)[0] == False:
        [[stab_group_min,phases_min], noncommind] = sf.min_noncomm(state,pauli);
        stab_list_min = sf.gen_matrix_to_stab_list(sf.gen_group_to_matrix(stab_group_min));
        stab_list_min[noncommind] = pauli
        m = rnd.choice([0,2])
        phases_min[noncommind] = m;
        return [[sf.stabgroup(stab_list_min),phases_min],1-m]
        


    
        