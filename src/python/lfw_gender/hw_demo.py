# hw_demo.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/29/15
#	
# Description    : Example showing how to use the CompetitiveLearningClassifier
# network designed for the hardware.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
Example showing how to create and use the CompetitiveLearningClassifier
designed for the hardware.

G{packagetree lfw_gender}
"""

__docformat__ = 'epytext'

# Native imports
import os

# Third party imports
import numpy as np

# Program imports
from lfw_gender.q_format   import Q
from lfw_gender.preprocess import resize_and_flatten
from lfw_gender.util       import get_data
from lfw_gender.hw_net     import CompetitiveLearningClassifier
from lfw_gender.plot       import plot_epoch, plot_weights

def reshape(data, shape):
	"""
	Resize the images from the original 30x30 size to any other desired size.
	
	@param data: A numpy array containing multiple images.
	
	@param shape: The new image shape to experiment with.
	"""
	
	d = np.zeros((data.shape[0], shape[0] * shape[1]), 'uint8')
	for i, img in enumerate(data):
		d[i] = resize_and_flatten(img.reshape((30, 30)), shape)
	return np.array(d, dtype='uint8')

def imgs_to_fp(x, m, n):
	"""
	Convert a list of images to fixed point.
	
	@param x: The data.
	
	@param m: The number of integer bits for fixed point.
		
	@param n: The number of fractional bits for fixed point.
	
	@return: A list of fixed point values represented the encoded images.
	"""
	
	return [[Q(m, n, y) for y in xi] for xi in x]

def fps_to_imgs(x, m, n):
	"""
	Convert a list of fixed point images to floating point.
	
	@param x: The data.
	
	@param m: The number of integer bits for fixed point.
		
	@param n: The number of fractional bits for fixed point.
	
	@return: A list of fixed point values represented the encoded images.
	"""
	
	return np.array([np.array([y.decode(y.q_num) for y in xi]) for xi in x])

def main(train_x, train_y, test_x, test_y, m, n, categories, nepochs=1,
	plot=True, verbose=True, learning_rate=0.01, min_weight=-1, max_weight=1,
	nrows=1, ncols=1, shape=(10, 10)):
	"""
	Demonstrates the CompetitiveLearningClassifier on LFW.
	
	@param train_x: The data to train with. This must be an iterable
	returning a numpy array.
	
	@param train_y: The labels for the training data. This must be an iterable
	returning a numpy array.
	
	@param test_x: The data to test with. This must be an iterable
	returning a numpy array.
	
	@param test_y: The labels for the testing data. This must be an iterable
	returning a numpy array.
	
	@param m: The number of integer bits for fixed point.
		
	@param n: The number of fractional bits for fixed point.
	
	@param categories: A list of the unique categories. This should be an
	iterable containing all of the unique labels in train_y / test_y.
	
	@param nepochs: The number of training epochs to perform.
	
	@param plot: If True, a plot will be created.
	
	@param verbose: If True, the network will print results after every
	iteration.
		
	@param learning_rate: The learning rate to use.
	
	@param nrows: The number of rows of plots to create for the clusters.
	
	@param ncols: The number of columns of plots to create for the clusters.
	
	@param shape: The shape of the weights. It is assumed that a 1D shape was
	used and is desired to be represented in 2D. Whatever shape is provided
	will be used to reshape the weights. For example, if you had a 10x10 image
	and each weight corresponded to one pixel, you would have a vector with a
	shape of (100, ). This vector would then need to be resized to your desired
	shape of (10, 10).
	
	@return: A tuple containing the training results, testing results, and
	weights, respectively.
	"""
	
	# Create the network
	net =  CompetitiveLearningClassifier(
		ninputs        = len(train_x[0]),
		m              = m,
		n              = n,
		categories     = categories,
		learning_rate  = learning_rate,
		min_weight     = min_weight,
		max_weight     = max_weight
	)
	
	# Run the network
	train_results, test_results = net.run(train_x, train_y, test_x, test_y,
		nepochs, verbose)
	
	# Reshape the weights
	weights = {}
	for category in categories:
		weights[category] = [net.cnets[category].weights]
		cluster_titles    = [None]
	
	# Plot the results
	if plot:
		# Plot the epochs
		plot_epoch(y_series=(train_results * 100, test_results * 100),
			series_names=('Train', 'Test'), y_bounds=(-5, 105),
			y_label='Accuracy [%]', title='LFW Gender - Example',
			legend_location='upper left')
		
		# Plot the weights for each class
		for category in categories:
			plot_weights(fps_to_imgs(weights[category], m , n), nrows, ncols,
				shape, 'Weights for Cluster {0}'.format(category),
				cluster_titles=cluster_titles)
	
	return train_results * 100, test_results * 100, weights

def basic_sim(nepochs=20, m=7, n=8):
	"""
	Perform a basic simulation.
	
	@param nepochs: The number of training epochs to perform.
	
	@param m: The number of integer bits for fixed point.
		
	@param n: The number of fractional bits for fixed point.
	"""
	
	# Get the data
	# (train_x, train_y), (test_x, test_y) = get_data()
	
	(train_x, train_y), (test_x, test_y) = get_data(30)
	train_x = reshape(train_x, (9, 9))
	test_x  = reshape(test_x, (9, 9))
	
	train_x_fp = imgs_to_fp(train_x/255., m, n)
	test_x_fp  = imgs_to_fp(test_x/255., m, n)
	
	main(train_x=train_x_fp, train_y=train_y, test_x=test_x_fp,
		test_y=test_y, m=m, n=n, categories=(0, 1), nepochs=nepochs)

if __name__ == '__main__':
	basic_sim(nepochs=5)