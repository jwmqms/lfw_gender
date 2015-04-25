# net.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/22/15
#	
# Description    : Module for carrying out the actual network implementation.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
Module for carrying out the actual network implementation.

G{packagetree lfw_gender}
"""

__docformat__ = 'epytext'

# Native imports
from abc       import ABCMeta, abstractmethod
from itertools import izip

# Third party imports
import numpy as np

# Program imports
from lfw_gender.timers import MultiTimer, pretty_time

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
	
	def initialize_weights(self, shape, min_weight=-1, max_weight=1):
		"""
		Initialize the weights of the network. Initialization is done randomly.
		
		@param shape: The number of nodes in the entire network. This parameter
		must be a sequence.
		
		@param min_weight: The minimum weight value.
		
		@param max_weight: The maximum weight value.
		"""
		
		self.weights = np.random.uniform(min_weight, max_weight, shape)
	
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
	
	def __init__(self, ninputs, learning_rate=0.001, min_weight=-1,
		max_weight=1):
		"""
		Initializes this competitive learning network.
		
		@param ninputs: The number of inputs to the network.
		
		@param learning_rate: The learning rate to use.
		
		@param min_weight: The minimum weight value.
		
		@param max_weight: The maximum weight value.
		"""
		
		# Store the params
		self.learning_rate  = learning_rate
		
		# Enable learning
		self.enable_learning()
		
		# Construct the weights
		self.initialize_weights(ninputs, min_weight, max_weight)
		
		# Construct the scalar output
		self.soutputs = np.zeros(1)
	
	def step(self, x):
		"""
		Compute a single step of the network.
		
		@param x: The input data to compute for this step.
		"""
		
		# Calculate the outputs
		self.soutputs[0] = np.sum((self.weights - x) ** 2)
		
		# Train the network
		if self.learning:
			self.weights += self.learning_rate * (x - self.weights)

class CompetitiveLearning(BaseCompetitiveLearning):
	"""
	Class for a competitive learning network (clustering) that does
	boosting.
	"""
	
	def __init__(self, ninputs, nclusters, learning_rate=0.001, boost_inc=0.1,
		boost_dec=0.01, duty_cycle=50, min_duty_cycle=5, min_weight=-1,
		max_weight=1):
		"""
		Initializes this competitive learning network.
		
		@param ninputs: The number of inputs to the network.
		
		@param nclusters: The number of clusters.
		
		@param learning_rate: The learning rate to use.
		
		@param boost_inc: The amount to increment the boost by.
		
		@param boost_dec: The amount to decrement the boost by.
		
		@param duty_cycle: The history to retain for activations for each node.
		This is the period minimum activation is compared across. It is a
		rolling window.
		
		@param min_duty_cycle: The minimum duty cycle. If a node has not been
		active at least this many times, increment its boost value, else
		decrement it.
		
		@param min_weight: The minimum weight value.
		
		@param max_weight: The maximum weight value.
		"""
		
		# Store the params
		self.learning_rate  = learning_rate
		self.boost_inc      = boost_inc
		self.boost_dec      = boost_dec
		self.duty_cycle     = duty_cycle
		self.min_duty_cycle = min_duty_cycle
		
		# Enable learning
		self.enable_learning()
		
		# Construct the weights
		self.initialize_weights((ninputs, nclusters), min_weight, max_weight)
		
		# Construct the boost values
		self.boost = np.ones(nclusters)
		
		# Construct the binary outputs
		#   - Each item represents a single cluster.
		#   - Each cluster maintains a history of length two of its update.
		#      - The first item refers to the current iteration.
		#      - The second item refers to the previous iteration.
		#      - The last item refers to the furthest iteration.
		self.boutputs = np.ones((nclusters, duty_cycle))
		
		# Construct the scalar outputs
		#   - Each item represents a single cluster.
		#   - Each cluster only maintains the current output
		self.soutputs = np.zeros(nclusters)
	
	def _update_boost(self):
		"""
		Update the boost values.
		"""
		
		for i, active in enumerate(self.boutputs):
			if int(np.sum(active)) >= self.min_duty_cycle:
				self.boost[i] += self.boost_inc
			else:
				self.boost[i] = max(self.boost[i] - self.boost_dec, 0)
	
	def step(self, x):
		"""
		Compute a single step of the network.
		
		@param x: The input data to compute for this step.
		"""
		
		# Shift outputs
		self.boutputs = np.roll(self.boutputs, 1, 1)
		
		# Calculate the outputs
		for i, weights in enumerate(self.weights.T):
			self.boutputs[i][0] = self.boost[i] * np.sum((weights - x) ** 2)
		
		# Get the scalar outputs
		self.soutputs = np.copy(self.boutputs.T[0])
		
		# Set a specific cluster to be the winner
		min_ix                   = np.argmin(self.boutputs.T[0])
		self.boutputs.T[0]       = 0
		self.boutputs[min_ix][0] = 1
		
		# Train the network
		if self.learning:
			# Update the boosts
			self._update_boost()
			
			# Update the weights
			for i, weights in enumerate(self.weights.T):
				self.weights.T[i] += self.learning_rate * self.boutputs[i][0] \
					* (x - weights)

class CompetitiveLearningClassifier(object):
	"""
	Base class for a competitive learning network (clustering) that can perform
	classification.
	"""
	
	def __init__(self, ninputs, nclusters, categories, learning_rate=0.001,
		boost_inc=0.1, boost_dec=0.01, duty_cycle=50, min_duty_cycle=5,
		min_weight=-1, max_weight=1):
		"""
		Initializes this competitive learning network.
		
		@param ninputs: The number of inputs to the network.
		
		@param nclusters: The number of clusters. If only 1 cluster is being
		used, boosting will be ignored.
		
		@param categories: A list of the labels for the categories. Each label
		should be an integer.
		
		@param learning_rate: The learning rate to use.
		
		@param boost_inc: The amount to increment the boost by.
		
		@param boost_dec: The amount to decrement the boost by.
		
		@param duty_cycle: The history to retain for activations for each node.
		This is the period minimum activation is compared across. It is a
		rolling window.
		
		@param min_duty_cycle: The minimum duty cycle. If a node has not been
		active at least this many times, increment its boost value, else
		decrement it.
		
		@param min_weight: The minimum weight value.
		
		@param max_weight: The maximum weight value.
		"""
		
		# Store the params
		self.nclusters      = nclusters
		self.learning_rate  = learning_rate
		self.boost_inc      = boost_inc
		self.boost_dec      = boost_dec
		self.duty_cycle     = duty_cycle
		self.min_duty_cycle = min_duty_cycle
		
		# Create the competitive learning networks
		if nclusters == 1:
			self.cnets = {category:SimpleCompetitiveLearning(ninputs,
				learning_rate, min_weight, max_weight)
				for category in categories}
		else:
			self.cnets = {category:CompetitiveLearning(ninputs, nclusters,
				learning_rate, boost_inc, boost_dec, duty_cycle,
				min_duty_cycle, min_weight, max_weight)
				for category in categories}
		
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
				cur_min = np.min(self.cnets[category].soutputs)
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