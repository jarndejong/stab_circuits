# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 12:23:35 2018

@author: Jarnd
"""

import sys
sys.path.append('../Functions')
sys.path.append('../Circuits/BitwiseFTSWAP')
import circuitfunctions as cf






def run_one_round(nq,init_state,circuit,p_m,p_s,meas_basis):
    state = cf.run_circuit(nq,init_state,circuit,p_m,p_s)
    m_list = measure_out(state,meas_basis)
    return m_list
    
def measure_out(nq,state,meas_basis):
    measurements = []
    for pauli in meas_basis:
        paulim = cf.initialize_pau_eigstate(nq,pauli,[0]*nq)
        [state,m] = cf.measure_pauli(nq,paulim,state);
        measurements.append(m)
    return measurements


