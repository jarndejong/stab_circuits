# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 15:10:44 2018

@author: Jarnd
"""
import time
import sys
sys.path.append('../Circuits/BitwiseFTSWAP')
sys.path.append('../Functions')

from FTSWAP import nq, gates, p_s, p_m

import simulationfunctions as smf

import itertools as itt


Ps = ['X','Y','Z']
Ms = ['X','Y','Z','I']
k = 0
start_time = time.time()
for iteration in itt.product(Ps, repeat = nq):
    if iteration == ('I',)*nq: continue
    for phase_iteration in itt.product([0,2], repeat = nq):
        for meas_iteration in itt.product(Ms, repeat = nq):
            #print('initial state',list(iteration))
            measurements = smf.run_one_round(nq,iteration,phase_iteration,gates,p_m,p_s,list(meas_iteration))
            k+=1
            

stop_time = time.time()
print(stop_time - start_time)