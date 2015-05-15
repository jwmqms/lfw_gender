# plot.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 05/15/15
#	
# Description    : Plot the hardware results.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
Plot the hardware results.
"""

__docformat__ = 'epytext'

# Native imports
import os

# Third party imports
import numpy as np

# Program imports
from lfw_gender.plot import plot_epoch

def get_labels(path):
	"""
	Get the labels for the specified train or test file.
	
	@param path: The full path to the HW train / test file.
	
	@return: A numpy array containing the labels.
	"""
	
	labels = []
	with open(path, 'rb') as f:
		for line in f:
			labels.append(int(line[0]))
	return np.array(labels)

def classify(predicted, actual):
	"""
	Determine the percent correct.
	
	@param predicted: The predicted values.
	
	@param actual: The actual values.
	
	@return: The percent correct.
	"""
	
	return np.average(predicted == actual) * 100

def get_case(path, actual):
	"""
	Get the accuracies corresponding to a single instance.
	
	@param path: The full path to the values to check.
	
	@param actual: The actual values.
	
	@return: A set of accuracies corresponding to multiple epochs.
	"""
	
	accuracies = []
	with open(path, 'rb') as f:
		for line in f:
			accuracies.append(classify([int(x) for x in line.split()], actual))
	return accuracies

def main(train_dir, test_dir, train_path, test_path, out_path):
	"""
	Generate some plots for training and testing, showing their accuracies
	across multiple epochs and iterations.
	
	@param train_dir: The directory containing the training results.
	
	@param test_dir: The directory containing the testing results.
	
	@param train_path: The full path to the HW train file.
	
	@param test_path: The full path to the HW test file.
	
	@param out_path: The full path of where to save the image.
	"""
	
	# Get the ground truths
	train_labels = get_labels(train_path)
	test_labels  = get_labels(test_path)
	
	# Get all of the training data
	train = []
	for path in os.listdir(train_dir):
		train.append(get_case(os.path.join(train_dir, path), train_labels))
	train_results = np.array(train)
	
	# Get all of the testing data
	test = []
	for path in os.listdir(test_dir):
		test.append(get_case(os.path.join(test_dir, path), test_labels))
	test_results = np.array(test)
	
	# Compute the mean costs
	train_mean = np.mean(train_results, 0)
	test_mean  = np.mean(test_results, 0)
	
	# Compute the standard deviations
	train_std = np.std(train_results, 0)
	test_std  = np.std(test_results, 0)
	
	# Plot the results
	plot_epoch(y_series=(train_mean, test_mean), y_bounds=(-5, 105),
		legend_location='upper left', series_names=('Train', 'Test'),
		y_errs=(train_std, test_std), y_label='Accuracy [%]', show=False,
		out_path=out_path)

if __name__ == '__main__':
	base_path    = os.path.dirname(os.path.dirname(os.getcwd()))
	fp_path      = os.path.join(base_path, 'data', 'fixed_point')
	results_path = os.path.join(base_path, 'results', '7x7', 'hw')
	
	train_dir  = os.path.join(results_path, 'training')
	test_dir   = os.path.join(results_path, 'testing')
	test_path  = os.path.join(fp_path, 'test.txt')
	train_path = os.path.join(fp_path, 'train.txt')
	out_path   = os.path.join(results_path, 'hw_results.pdf')
	
	main(train_dir, test_dir, train_path, test_path, out_path)