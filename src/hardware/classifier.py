# classifier.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 05/06/15
#	
# Description    : Simple classifier for the HW output.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
Simple classifier for the HW output.
"""

__docformat__ = 'epytext'

# Native imports
import os
from   itertools import izip

# Third party imports
import numpy as np

def classify(test_path, source_path):
	"""
	Determine the percent correct for the HW test cases.
	
	@param test_path: The full path to the HW test file.
	
	@param source_path: The Full path to the output from the HW.
	"""
	
	accuracy = 0.
	c        = 0
	with open(test_path, 'rb') as yt, open(source_path, 'rb') as ys:
		for tline, sline in izip(yt, ys):
			c += 1
			if tline[0] == sline[0]: accuracy += 1
	
	return (accuracy / c) * 100

def main(train_dir, test_dir, train_path, test_path):
	"""
	Generate some plots for training and testing, showing their accuracies
	across multiple epochs and iterations.
	
	@param train_dir: The directory containing the training results.
	
	@param test_dir: The directory containing the testing results.
	
	@param train_path: The full path to the HW train file.
	
	@param test_path: The full path to the HW test file.
	"""
	
	# Get all of the training data
	train = []
	for path in os.listdir(train_dir):
		train.append(classify(train_path, os.path.join(train_dir, path)))
	train_results = np.array(train)
	
	# Get all of the testing data
	test = []
	for path in os.listdir(test_dir):
		test.append(classify(test_path, os.path.join(test_dir, path)))
	test_results = np.array(test)
	
	# Compute the mean costs
	train_mean = np.mean(train_results, 0)
	test_mean  = np.mean(test_results, 0)
	
	# Compute the standard deviations
	train_std = np.std(train_results, 0)
	test_std  = np.std(test_results, 0)
	
	print 'Train Accuracy: {0}; Train STDEV: {1}'.format(train_mean, train_std)
	print 'Test Accuracy: {0}; Test STDEV: {1}'.format(test_mean, test_std)

if __name__ == '__main__':
	base_path    = os.path.dirname(os.path.dirname(os.getcwd()))
	fp_path      = os.path.join(base_path, 'data', 'fixed_point')
	results_path = os.path.join(base_path, 'results', '7x7', 'hw')
	
	train_dir  = os.path.join(results_path, 'training')
	test_dir   = os.path.join(results_path, 'testing')
	test_path  = os.path.join(fp_path, 'test.txt')
	train_path = os.path.join(fp_path, 'train.txt')
	
	main(train_dir, test_dir, train_path, test_path)