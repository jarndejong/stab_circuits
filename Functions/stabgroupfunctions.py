# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 13:52:00 2018

@author: Jarnd
"""

import numpy as np
import itertools as itt
import copy


def bitstring_to_pauli(stab_list):
    """This function takes an numpy array of size 2*1 with every entry a n-bit 
    string, representing a stabilizer, and returning a string of length n 
    representing the stabilizer as its Pauli's"""
    pau_dict = {0:'I',1:'Z',2:'X',3:'Y'};
    stab_str_list = []
    if type(stab_list[0][0]) == np.int32:
        stab_syn = list(stab_list[0]+2*stab_list[1]);
        stab_str = ''
        for entry in stab_syn:
            stab_str += pau_dict[entry]
        return stab_str
    
    for stab in stab_list:
        stab_syn = list(stab[0]+2*stab[1]);
        stab_str = ''
        for entry in stab_syn:
            stab_str += pau_dict[entry]
        stab_str_list.append(stab_str)
    return stab_str_list

def pauli_to_bitstring(pauli):
    """pauli_to_bitstring(pauli) for pauli a string representation of a stabilizer
    Converts the pauli from a string to a list with two entries: 
    a list of z and a list of x weights. 
    """
    pau_dict = {'I':[0,0],'Z':[1,0],'X':[0,1],'Y':[1,1]};
    x = []; z = [];
    for char in pauli:
        z.append(pau_dict[char][0]);
        x.append(pau_dict[char][1]);
    return np.array([z,x])
    

def comp_comm(A,B):
    """comp_comm(A,B) for A & B two stabilizers in the bitstring representation
    Calculates the symplectic inner product and returns the value
    Return 0 for commutation and 1 for anticommutation
    """
    return (np.dot(A[0],B[1])+np.dot(A[1],B[0])) % 2

def stabgroup(gen_list):
    """ stabgroup(gen_list) for gen_list a python list of stabilizers
    Creates two matrices Z & X and puts them in an element stabgroup. 
    Call matrix Z as stabgroup[0] and X as stabgroup[1].
    The element stabgroup is used in other functions
    """
    k = len(gen_list[0][0]);
    Z = np.zeros((k,), dtype=int)   # Defining an empty array seems not to work
    X = np.zeros((k,), dtype=int)
    for item in gen_list:
        Z = np.vstack((Z,item[0]))
        X = np.vstack((X,item[1]))
    stabgroup = (np.delete(Z,0,0), np.delete(X,0,0)) # Now I need to delete these, can I do this in another way?
    return stabgroup

def check_stabgroup(stab_group):
    """check_stabgroup(stab_group) for a stabgroup:
    Checks if all stabilizers in the stab_group commute and if the elements are indeed generators
    Returns False if the rank of Z & Xs combined are not zero
    Returns False if the the simplectic inner product of Z & X is nonzero
    Returns True otherwise
    """
    Z = stab_group[0];
    X = stab_group[1];
    
    if np.count_nonzero((Z @ np.transpose(X) - X @ np.transpose(Z))%2) != 0:
        return [False, (Z @ np.transpose(X) - X @ np.transpose(Z))%2, 'noncommuting']
    elif rank(gen_group_to_matrix(stab_group)) != len(Z[:,0]):
        return [False, rank(gen_group_to_matrix(stab_group)),'overcomplete']
    else:
        return True

def check_commuting(stab_group):
    """check_commuting(stab_group) for a stabgroup
    Checks if all elements in the stab_group commute with each other. 
    If not, it outputs [False, (Z @ np.transpose(X) - X @ np.transpose(Z))%2]
    If so, it outputs [True, 0]
    """
    Z = stab_group[0];
    X = stab_group[1];
    if np.count_nonzero((Z @ np.transpose(X) - X @ np.transpose(Z))%2) != 0:
        return [False, (Z @ np.transpose(X) - X @ np.transpose(Z))%2]
    else:
        return [True, 0]


def min_noncomm(state,pauli):
    """min_noncomm(stab_group,pauli) for stab_group a stabilizer group
    Checks if pauli commutes with the stab_group. If so, outputs an errorstring
    If not, it minimizes the number of generators that anticommute with the pauli to 1.
    It then returns an updated generator group with only the one anticommuting stabilizer, and its index
    returns [state_min, index_of_noncomm_stab]
    """
    stab_group = state[0]
    phases = state[1]
    total_space_group = gen_matrix_to_stab_list(gen_group_to_matrix(stab_group));
    total_space_group.append(pauli);
    total_space_group = stabgroup(total_space_group);
    if check_commuting(total_space_group)[0]:
        return 'Error: Pauli commutes with given stabilizer group'
    noncomm_stab_ind = np.nonzero(check_commuting(total_space_group)[1][:,-1])[0];
    stab_matrix = gen_group_to_matrix(stab_group)
    for ind in noncomm_stab_ind[1:]:
        stab_matrix[ind,:] += stab_matrix[noncomm_stab_ind[0],:]
        phases[ind] += phases[noncomm_stab_ind[0]]
    stab_matrix = stab_matrix%2
    phases = (phases)%4
    return [[stabgroup(gen_matrix_to_stab_list(stab_matrix)),phases],noncomm_stab_ind[0]]

def gen_matrix_to_stab_list(S):
    """gen_matrix_to_stab_list(gen_matrix) for gen_matrix a generator matrix
    return a list of the generators/elements in the generator matrix
    """
    gen_list = []
    h,w = np.shape(S)
    for i in range(h):
        gen_list.append([S[i,:int(w/2)],S[i,int(w/2):]])
    return gen_list
        

def gen_group_to_matrix(gen_group):
    """gen_group_to_matrix(gen_group) for a stabgroup
    Return a matrix of binary representation of the generators in the stabgroup
    """
    return np.concatenate((gen_group[0],gen_group[1]),axis=1)

def pauli_mult(P_A,P_B):
    """pauli_mult(P_a,P_b) for P_a & P_b both Pauli's in the bitstring representation
    Computes the multiplication of two Pauli's as a bitstringsum.
    ## TO DO(?): Add phase?"""
    return (P_A+P_B) % 2

def list_stabgroup_elements(gen_group,stab, notation = None):
    """list_stabgroup_elements(gen_group,stab, notation = None) for a gen_group
    list all the elements in the stabilizer group. Also pass one stabilizer of the group
    Pass optional parameter B or P. B for bitwise representation, P for Puli representation. B is standard
    """
    element_list = []
    if notation is None:
        notation = 'B'
    for item in itt.product(range(2),repeat = len(gen_group[0])):
        element = copy.deepcopy(stab)
        element[0] = np.sum(gen_group[0]*np.array(item)[:, None],axis = 0) % 2;
        element[1] = np.sum(gen_group[1]*np.array(item)[:, None],axis = 0) % 2;
        if notation == 'B': element_list.append(element)
        elif notation == 'P': element_list.append(bitstring_to_pauli(element))
    return element_list

def swap_row(mat,row1,row2):
    """swap_row(mat,row1,row2) for mat a generator matrix and row 1 and row 2 indices
    Swaps the row row1 and row2 and return the matrix with the swapped rows
    """
    mat[[row1,row2]] = mat[[row2,row1]];
    return mat

def ech(K):
    """ech(K) for K a binary matrix
    Returns the echelon form of a binary matrix
    """
    S = K.copy()
    rank = 0
    for i in range(np.shape(S)[1]):
        ones = np.where(S[rank:,i] == 1)[0]
        if len(ones) > 0:
            S = swap_row(S,ones[0]+rank,rank)
            ones[0] = rank
            for j in range(1,len(ones)):
                S[ones[j]+rank,:] = (S[ones[j]+rank,:] - S[ones[0],:])%2
            rank +=1;
    return S
             
def rank(K):
    """rank(K) for binary matrix K
    Returns the rank of K
    """
    S = ech(np.copy(K))
    r = np.shape(S)[0]
    for row in range(r):
        if not np.any(S[row,:]):
            r -= 1
    return r 

def piv_columns(K):
    """piv_columns(K) for a binary matrix K
    Returns the indeces of the pivot columns of K as a python list
    """
    S = ech(K.copy())
    piv_column = []
    for row in range(rank(S)):
        piv_column.append(np.where(S[row,:] == 1)[0][0])
    return piv_column

def red_ech(K):
    """red_ech(K) for a binary matrix K
    Returns the reduced echelon form of a binary matrix K
    """
    S = ech(K.copy())
    columns = piv_columns(S)
    for column in columns:
        ones_ind = list(np.where(S[:,column] == 1)[0])
        if len(ones_ind) > 1:
            for entry in range(0,len(ones_ind)-1):
                S[ones_ind[entry],:] = (S[ones_ind[entry],:]+S[ones_ind[-1],:])%2
    return S

def swap_XZ(vect):
    """swap_XZ(vect) for vect a binary Pauli
    swaps the X&Z part for the Pauli vect in binary representation
    """
    l = np.size(vect)
    h = int(l/2)
    vectn = np.zeros(l)
    vectn[:h] = vect[h:]
    vectn[h:] = vect[:h]
    return vectn.astype(int)

def nullspace_basis(K):
    """nullspace_basis(K) for a binary matrix K
    Returns a basis for the nullspace of the binary matrix K.
    For a generator matrix, this is a list of the Logical Pauli's for the code
    combined with a basis for the stabilizer space as well, since those vectors
    are orthogonal to themselves
    """
    S = red_ech(K.copy()) 
    w,l = np.shape(K)
    basis = []
    non_piv_col = [x for x in [x for x in range(l)] if x not in piv_columns(K)]
    piv_col = piv_columns(K);
    for col in non_piv_col:
        vect = np.zeros(l);
        vect[col] = 1;
        red_row_column = S[:,col];
        i = 0;
        for entry in piv_col:
            vect[entry] = red_row_column[i]
            i +=1
        basis.append(obtain_sympl_P(int(l/2))@vect)    
            
        
    return basis

def obtain_sympl_P(nq):
    """obtain_sympl_P(nq) for nq the number of qubits
    Returns the matrix P that swaps the first and second half of a vector.
    Used for the symplectic inner product.
    """
    P = np.eye(2*nq)
    P[:,:nq],P[:,nq:] = P[:,nq:], P[:,0:nq].copy()
    return P

def logical_pauli(K):
    """logical_pauli(K) for binary matrix K
    Returns a set of vectors that are the logical paulis,
    for the set of stabilizers specified in the generator matrix K
    """
    S = red_ech(K.copy())
    paulis = []
    basis = nullspace_basis(S)
    oldmatr = S
    for vect in basis:
        newmatr = np.vstack((oldmatr,vect))
        if rank(newmatr) >= rank(oldmatr):
            paulis.append(vect_to_bitstring(vect))
        oldmatr = newmatr
    return paulis
    
def vect_to_bitstring(vect):
    """vect_to_bitstring(vect)
    Returns the pauli in vect as a bitstring representation (with Z&X in different arrays)
    """
    l = len(vect)
    return np.array([vect[:int(l/2)],vect[int(l/2):]]).astype(int)    
#def list_detectable_errors(gen_matrix):
#    
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        