import numpy as np
import scipy.linalg as lg

m = 0.005
m1 = 0.370
m2 = 0.100

k1 = 300
k2 = 100

M = np.array([[ m1, 0],
              [  0,  m2]])

K = np.array([[ 2*k1+k2, -k2],
              [  -k2,  k2]])


res = lg.eig(K,M)
vecw = res[0]
phi = res[1]

w1 = np.sqrt(vecw[0]).real
w2 = np.sqrt(vecw[1]).real

print("Frequencies = ", w1, "rad/s ",  w2, "rad/s ")
print("            = ", w1/(2*np.pi), "Hzs",  w2/(2*np.pi), "Hzs")

Kg = np.dot(np.dot(phi.T, K), phi)
Mg = np.dot(np.dot(phi.T, M), phi)

phiM = phi.copy()

phiM[:,0] = phiM[:,0]/np.sqrt(Mg[0,0])
phiM[:,1] = phiM[:,1]/np.sqrt(Mg[1,1])

Km = np.dot(np.dot(phiM.T, K), phiM)
Mm = np.dot(np.dot(phiM.T, M), phiM)


print("Normalized by mass matrices")
print("K = ")
print(Km)
print("M = ")
print(Mm)

