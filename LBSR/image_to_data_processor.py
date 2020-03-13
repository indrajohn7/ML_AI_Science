#!/usr/bin/python3

import os
import sys
from PIL import Image
import numpy as np
from sklearn.preprocessing import StandardScaler
import sklearn.datasets, sklearn.decomposition

THRESHOLD = 0.99

#	**********************************************		CONVERTING IMAGE DATA		**************************************************************#
image_name = "opera_house.jpg"

# load the image
image = Image.open(image_name)

# convert image to numpy array
data = np.asarray(image)

#Summarize Data
print (data.shape)
print (data)

#	**********************************************		Segmenting RGB Channel		***************************************************************#

print ("Shape: %d :: %d :: %d" % (data.shape[0], data.shape[1], data.shape[2]))
row = data.shape[0]
col = data.shape[1]
channel = data.shape[2]

r_channel = data[:row, :col, :1]
r_channel = np.reshape(r_channel, (row, col))

print (r_channel.shape)
print (r_channel)

g_channel = data[:row, :col, 1:2]
g_channel = np.reshape(g_channel, (row, col))

print (g_channel.shape)
print (g_channel)

b_channel = data[:row, :col, 2:]
b_channel = np.reshape(b_channel, (row, col))

print (b_channel.shape)
print (b_channel)

#	**********************************************		Standardizing Data Set		***************************************************************#

sc = StandardScaler()
r_channel_std = sc.fit_transform(r_channel)
g_channel_std = sc.fit_transform(g_channel)
b_channel_std = sc.fit_transform(b_channel)

#	**********************************************		Covariance matrix		***************************************************************#

cov_mat_r = np.cov(r_channel_std.T)
cov_mat_g = np.cov(g_channel_std.T)
cov_mat_b = np.cov(b_channel_std.T)

#	**********************************************		Eigen properties		***************************************************************#

eigen_vals_r, eigen_vecs_r = np.linalg.eig(cov_mat_r)
eigen_vals_g, eigen_vecs_g = np.linalg.eig(cov_mat_g)
eigen_vals_b, eigen_vecs_b = np.linalg.eig(cov_mat_b)

#	**********************************************		Correctness Parameter Tuning		***************************************************************#

tot_r = sum(eigen_vals_r)
var_exp_r = [(i / tot_r) for i in sorted(eigen_vals_r, reverse=True)]
cum_var_exp_r = np.cumsum(var_exp_r)

tot_g = sum(eigen_vals_g)
var_exp_g = [(i / tot_g) for i in sorted(eigen_vals_g, reverse=True)]
cum_var_exp_g = np.cumsum(var_exp_g)

tot_b = sum(eigen_vals_b)
var_exp_b = [(i / tot_b) for i in sorted(eigen_vals_b, reverse=True)]
cum_var_exp_b = np.cumsum(var_exp_b)

count_r = count_g = count_b = 0

for num in cum_var_exp_r:
	if (num >= THRESHOLD):
		count_r += 1
		break
	count_r += 1

for num in cum_var_exp_g:
	if (num >= THRESHOLD):
		count_g += 1
		break
	count_g += 1

for num in cum_var_exp_b:
	if (num >= THRESHOLD):
		count_b += 1
		break
	count_b += 1

#	**********************************************		Eigen Pairs		***************************************************************#

eigen_pairs_r = [(np.abs(eigen_vals_r[i]), eigen_vecs_r[:, i]) for i in range(len(eigen_vals_r))]
eigen_pairs_g = [(np.abs(eigen_vals_g[i]), eigen_vecs_g[:, i]) for i in range(len(eigen_vals_g))]
eigen_pairs_b = [(np.abs(eigen_vals_b[i]), eigen_vecs_b[:, i]) for i in range(len(eigen_vals_b))]

# Sort the (eigenvalue, eigenvector) tuples from high to low
eigen_pairs_r.sort(key=lambda k: k[0], reverse=True)
eigen_pairs_g.sort(key=lambda k: k[0], reverse=True)
eigen_pairs_b.sort(key=lambda k: k[0], reverse=True)

#	**********************************************		Mean properties		***************************************************************#

mu_r = np.mean(r_channel, axis = 0)
mu_g = np.mean(g_channel, axis = 0)
mu_b = np.mean(b_channel, axis = 0)

#	**********************************************		Principal Component		***************************************************************#

pca_r = sklearn.decomposition.PCA()
pca_r.fit(r_channel)
nComp = count_r
r_PCA = pca_r.transform(r_channel)[:,:nComp]

pca_g = sklearn.decomposition.PCA()
pca_g.fit(g_channel)
nComp = count_g
g_PCA = pca_g.transform(g_channel)[:,:nComp]

pca_b = sklearn.decomposition.PCA()
pca_b.fit(b_channel)
nComp = count_b
b_PCA = pca_b.transform(b_channel)[:,:nComp]

print ("R_PCA SHAPE: %s" % str(r_PCA.shape))
print (r_PCA)
print ("G_PCA SHAPE: %s" % str(g_PCA.shape))
print (g_PCA)
print ("B_PCA SHAPE: %s" % str(b_PCA.shape))
print (b_PCA)
#	**********************************************		Eigen TransPose properties		***************************************************************#

eigen_trans_r = pca_r.components_[:count_r,:]
eigen_trans_g = pca_g.components_[:count_g,:]
eigen_trans_b = pca_b.components_[:count_b,:]

#	**********************************************		Actual RGB dataset		***************************************************************#

rhat = np.dot(r_PCA, eigen_trans_r)
rhat += mu_r
ghat = np.dot(g_PCA, eigen_trans_g)
ghat += mu_g
bhat = np.dot(b_PCA, eigen_trans_b)
bhat += mu_b

print ("RHAT SHAPE: %s" % (str(rhat.shape)))
print (rhat)
print ("GHAT SHAPE: %s" % (str(ghat.shape)))
print (ghat)
print ("BHAT SHAPE: %s" % (str(bhat.shape)))
print (bhat)

#	**********************************************		Creating RGB Data Frame		***************************************************************#
if (rhat.shape == ghat.shape and ghat.shape == bhat.shape):
	rows = rhat.shape[0]
	cols = ghat.shape[1]
	data_list = []
	rhat_list = rhat.tolist()
	ghat_list = ghat.tolist()
	bhat_list = bhat.tolist()
	for r in range(row):
		rlist = [int(round(x)) for x in rhat_list[r]]
		glist = [int(round(x)) for x in ghat_list[r]]
		blist = [int(round(x)) for x in bhat_list[r]]
		row_list = []
		for c in range(cols):
			alist = []
			alist.append(rlist[c])
			alist.append(glist[c])
			alist.append(blist[c])
			row_list.append(alist)
		data_list.append(row_list)

else:
	print ("RGB Properties Mismatching while doing back propagation: Exiting!")
	sys.exit()

rgb_frame = np.array(data_list)
print ("RGB SHAPE: %s" % (str(rgb_frame.shape)))
#rgb_frame = np.reshape(rgb_frame, (rows, cols, 3))
print (rgb_frame)

#	**********************************************		Data to Image Processor		***************************************************************#

#Create Pillow Image

#image2 = Image.fromarray(rgb_frame)
image2 = Image.fromarray((rgb_frame * 255).astype(np.uint8))

print(image2.format)
print(image2.mode)
print(image2.size)

image2.show()
image_arr = image_name.split()[:-1]
new_image_name = '.'.join(image_arr) + "comp.jpg"
image2.save(new_image_name)

