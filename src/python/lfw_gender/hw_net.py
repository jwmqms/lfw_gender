# hw_net.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/29/15
#	
# Description    : A HW implementation of the net.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
A HW implementation of the net.

G{packagetree lfw_gender}
"""

__docformat__ = 'epytext'

# Native imports
from   abc       import ABCMeta, abstractmethod
from   itertools import izip
import random

# Third party imports
import numpy as np

# Program imports
from lfw_gender.q_format import Q
from lfw_gender.timers   import MultiTimer, pretty_time

###############################################################################
########## Class Templates
###############################################################################

class BaseCompetitiveLearning(object):
	"""
	Base class for a competitive learning network.
	"""
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __init__(self):
		"""
		Initialize the class instance.
		"""
	
	@abstractmethod
	def step(self, x):
		"""
		Compute a single step of the network.
		
		@param x: The input data to compute for this step.
		"""
	
	def initialize_weights(self, ninputs, min_weight=-1, max_weight=1):
		"""
		Initialize the weights of the network. Initialization is done randomly.
		
		@param ninputs: The number of nodes in the entire network.
		
		@param min_weight: The minimum weight value.
		
		@param max_weight: The maximum weight value.
		"""
		
		self.weights = [Q(self.m, self.n, random.uniform(min_weight,
			max_weight)) for _ in xrange(ninputs)]
	
	def enable_learning(self):
		"""
		Enables learning for the network.
		"""
		
		self.learning = True
	
	def disable_learning(self):
		"""
		Disables learning for the network.
		"""
		
		self.learning = False

###############################################################################
########## Class Implementations
###############################################################################

class SimpleCompetitiveLearning(BaseCompetitiveLearning):
	"""
	Class for a competitive learning network with a single cluster.
	"""
	
	def __init__(self, ninputs, m, n, learning_rate=0.01, min_weight=-1,
		max_weight=1):
		"""
		Initializes this competitive learning network.
		
		@param ninputs: The number of inputs to the network.
		
		@param m: The number of integer bits for fixed point.
		
		@param n: The number of fractional bits for fixed point.
		
		@param learning_rate: The learning rate to use.
		
		@param min_weight: The minimum weight value.
		
		@param max_weight: The maximum weight value.
		"""
		
		# Store the params
		self.m              = m
		self.n              = n
		self.learning_rate  = Q(self.m, self.n, learning_rate)
		
		# Enable learning
		self.enable_learning()
		
		# Construct the weights
		self.initialize_weights(ninputs, min_weight, max_weight)
	
	def step(self, x):
		"""
		Compute a single step of the network.
		
		@param x: The input data to compute for this step.
		"""
		
		# Calculate the output
		self.soutput = Q(self.m, self.n, 0)
		for wi, xi in izip(self.weights, x):
			self.soutput += (wi - xi) ** 2
		
		# Train the network
		if self.learning:
			i = 0
			for wi, xi in izip(self.weights, x):
				self.weights[i] += self.learning_rate * (xi - wi)
				i               += 1

class CompetitiveLearningClassifier(object):
	"""
	Base class for a competitive learning network (clustering) that can perform
	classification.
	"""
	
	def __init__(self, ninputs, m, n, categories, learning_rate=0.01,
		min_weight=-1, max_weight=1):
		"""
		Initializes this competitive learning network.
		
		@param ninputs: The number of inputs to the network.
		
		@param m: The number of integer bits for fixed point.
		
		@param n: The number of fractional bits for fixed point.
		
		@param categories: A list of the labels for the categories. Each label
		should be an integer.
		
		@param learning_rate: The learning rate to use.
		
		@param min_weight: The minimum weight value.
		
		@param max_weight: The maximum weight value.
		"""
		
		# Create the competitive learning networks
		self.cnets = {category:SimpleCompetitiveLearning(ninputs, m, n,
			learning_rate, min_weight, max_weight) for category in categories}
		
		# Initialize a timing unit
		self.timers = MultiTimer()
	
	def enable_learning(self):
		"""
		Enable learning for all of the nets.
		"""
		
		for cnet in self.cnets.values():
			cnet.enable_learning()
	
	def disable_learning(self):
		"""
		Disable learning for all of the nets.
		"""
		
		for cnet in self.cnets.values():
			cnet.disable_learning()
	
	def train(self, x, y):
		"""
		Train the network for a single step.
		
		@param x: The training data.
		
		@param y: The labels for the training data.
		"""
		
		# Enable learning for all of the networks
		self.enable_learning()
		
		# Train the networks
		for xi, yi in izip(x, y):
			self.cnets[yi].step(xi)
	
	def classify(self, x, y):
		"""
		Classify the network.
		
		@param x: The data to classify with.
		
		@param y: The labels for the classification data.
		
		@return: The classification accuracy (1 == 100%).
		"""
		
		# Initialize the accuracy
		accuracy = 0.
		
		# Disable learning for all of the networks
		self.disable_learning()
		
		# Evaluate all patterns
		count = 0
		for xi, yi in izip(x, y):
			min_dist = np.inf; found_class = None
			for i, category in enumerate(self.cnets):
				self.cnets[category].step(xi)
				cur_min = self.cnets[category].soutput.decode(
					self.cnets[category].soutput.q_num)
				if cur_min < min_dist:
					min_dist = cur_min; found_class = category
			if found_class == yi: accuracy += 1
			count += 1
		accuracy /= count
		
		return accuracy
	
	def run(self, train_x, train_y, test_x, test_y, nepochs=1, verbose=True):
		"""
		Simulate the entire network.
		
		@param train_x: The data to train with. This must be an iterable
		returning a numpy array.
		
		@param train_y: The labels for the training data. This must be an
		iterable returning a numpy array.
		
		@param test_x: The data to test with. This must be an iterable
		returning a numpy array.
		
		@param test_y: The labels for the testing data. This must be an
		iterable returning a numpy array.
		
		@param nepochs: The number of training epochs to perform.
		
		@param verbose: If True, details will be printed after each epoch.
		
		@return: A tuple containing the training and test accuracies.
		"""
		
		# Make some timers
		self.timers = MultiTimer()
		self.timers.add_timers('global', 'train', 'train_epoch', 'test',
			'test_epoch')
		self.timers.stop_timers('train', 'train_epoch', 'test', 'test_epoch')
		
		# Initializations
		train = self.train; classify = self.classify
		train_accuracy = np.zeros(nepochs); test_accuracy  = np.zeros(nepochs)
		
		# Iterate through all epochs
		for i in xrange(nepochs):
			# Train with all of the patterns
			self.timers.start_timers('train', 'train_epoch')
			self.train(train_x, train_y)
			
			# Get the accuracy for all of the training patterns
			train_accuracy[i] = classify(train_x, train_y)
			self.timers.pause_timers('train')
			self.timers.stop_timers('train_epoch')
			
			# Print out training stats
			if verbose:
				print '\nEpoch {0} of {1}:'.format(i + 1, nepochs)
				print '  Training Accuracy : {0}%'.format(train_accuracy[i] *
					100)
				print '  Training Time     : {0}'.format(
					self.timers.get_elapsed_time('train_epoch', True))
			
			# Get the accuracy for all of the testing patterns
			self.timers.start_timers('test', 'test_epoch')
			test_accuracy[i] = classify(test_x, test_y)
			self.timers.pause_timers('test')
			self.timers.stop_timers('test_epoch')
			
			# Print out testing stats
			if verbose:
				print '  Testing Accuracy  : {0}%'.format(test_accuracy[i] *
					100)
				print '  Testing Time      : {0}'.format(
					self.timers.get_elapsed_time('test_epoch', True))
		
		# Print out the final results
		self.timers.stop_timers('global')
		if verbose:
			print '\n' + '*' * 79
			print '\nBest Training Accuracy : {0}% at Epoch {1}'.format(np.max(
				train_accuracy) * 100, np.argmax(train_accuracy) + 1)
			print 'Best Testing Accuracy  : {0}% at Epoch {1}'.format(np.max(
				test_accuracy) * 100, np.argmax(test_accuracy) + 1)
			print '\nTotal Execution Time        : {0}'.format(
				self.timers.get_elapsed_time('global', True))
			print 'Total Training Time         : {0}'.format(
				self.timers.get_elapsed_time('train', True))
			print 'Average Training Epoch Time : {0}'.format(
				pretty_time(self.timers.get_elapsed_time('train') / nepochs))
			print 'Total Testing Time          : {0}'.format(
				self.timers.get_elapsed_time('test', True))
			print 'Average Testing Epoch Time  : {0}'.format(
				pretty_time(self.timers.get_elapsed_time('test') / nepochs))		
		
		return (train_accuracy, test_accuracy)