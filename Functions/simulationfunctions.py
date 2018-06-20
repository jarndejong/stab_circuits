# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 12:23:35 2018

@author: Jarnd
"""

import circuitfunctions as cf

def run_one_round(nq,pau_list_init,phase_list_init,circuit,p_m,p_s,meas_basis):
    state = cf.initialize_pau_eigstate(nq,pau_list_init,phase_list_init)
    state = cf.run_circuit(nq,state,circuit,p_m,p_s)
    m_list = measure_out(nq,state,meas_basis)
    return m_list
    
def measure_out(nq,state,meas_basis):
    measurements = []
    for pauli in meas_basis:
        paulim = cf.initialize_pau_eigstate(nq,pauli,[0]*nq)
        [state,m] = cf.measure_pauli(nq,paulim,state);
        measurements.append(m)
    return measurements
