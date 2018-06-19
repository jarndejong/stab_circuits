# -*- coding: utf-8 -*-
"""
Created on Tue May 15 13:50:07 2018

@author: Jarnd
"""
import numpy as np
import math as mt
import scipy.linalg as lin


X = np.matrix([[0, 1],[1, 0]]);
Z = np.matrix([[1, 0],[ 0, -1]]);
Y = 1j*np.dot(X,Z);
I = np.matmul(X,X);
H = (1/np.sqrt(2))*np.matrix([[1, 1],[1, -1]])

S = np.matrix([[1, 0],[ 0, 1j]]);


XI = np.kron(X,I)
YI = np.kron(Y,I)
ZI = np.kron(Z,I)
HI = np.kron(H,I)
IX = np.kron(I,X)
IY = np.kron(I,Y)
IZ = np.kron(I,Z)
IH = np.kron(I,H)

XII = np.kron(XI,I)
IXI = np.kron(I,XI)
IIX = np.kron(I,IX)
ZII = np.kron(ZI,I)
IZI = np.kron(I,ZI)
IIZ = np.kron(I,IZ)
HII = np.kron(HI,I)
IHI = np.kron(I,HI)
IIH = np.kron(I,IH)

II = np.kron(I,I)
III = np.kron(II,I)
CZ = np.asmatrix(np.copy(II))
CZ[3,3] = -1
CCZ = np.asmatrix(np.copy(III))
CCZ[-1,-1] = -1
CX = IH @ CZ @ IH
SWAP = np.matrix([[1, 0, 0, 0],[0, 0, 1, 0],[0, 1, 0, 0],[0, 0, 0, 1]])
CIZ = (1/2)*(III+IIZ+ZII-ZII*IIZ)






zest = np.matrix([1, 0]).T
onst = np.matrix([0, 1]).T
plst = 1/np.sqrt(2)*np.matrix([1, 1]).T
mist = 1/np.sqrt(2)*np.matrix([1, -1]).T
yplst = 1/np.sqrt(2)*np.matrix([1, 1j]).T
ymist = 1/np.sqrt(2)*np.matrix([1, 1j]).H

st = np.mat([1/np.sqrt(3),np.sqrt(2/3)*1j]).T
print('H = ',st.H*H*st)
print('X = ',st.H*X*st)
print('Y = ',st.H*Y*st)
print('Z = ',st.H*Z*st)
print('H = ',st.H*H*st)