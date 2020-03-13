#!/usr/bin/python

import os
import read_data as rd
#import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import sklearn.datasets, sklearn.decomposition

THRESHOLD = 0.99

X_train = rd.field_mat

sc = StandardScaler()
X_train_std = sc.fit_transform(X_train)

cov_mat = np.cov(X_train_std.T)
eigen_vals, eigen_vecs = np.linalg.eig(cov_mat)

print "************************************** XTRAIN *************************************8"
print X_train

tot = sum(eigen_vals)
var_exp = [(i / tot) for i in sorted(eigen_vals, reverse=True)]
cum_var_exp = np.cumsum(var_exp)

print "************************************** CUM_VAR *************************************8"
print cum_var_exp
count = 0

for num in cum_var_exp:
    if num >= THRESHOLD:
        count += 1
        break
    count += 1

eigen_pairs = [(np.abs(eigen_vals[i]), eigen_vecs[:, i]) for i in range(len(eigen_vals))]

# Sort the (eigenvalue, eigenvector) tuples from high to low
eigen_pairs.sort(key=lambda k: k[0], reverse=True)

mu = np.mean(X_train, axis = 0)

print "************************************** MU *************************************8"
print mu.shape
print mu
pca = sklearn.decomposition.PCA()
pca.fit(X_train)

print "************************************** nComp *************************************8"
nComp = count
print nComp
X_PCA = pca.transform(X_train)[:,:nComp]

print "************************************** XPCA *************************************8"
print X_PCA.shape
print X_PCA
eigen_trans = pca.components_[:nComp,:]

#Xhat = np.dot(X_PCA, eigen_trans)
#Xhat += mu


print "************************************** XHAT *************************************8"
#print Xhat
