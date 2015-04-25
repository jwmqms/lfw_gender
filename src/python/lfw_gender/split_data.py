# split_data.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/22/15
#	
# Description    : Divide the preprocessed data into training and testing data
# sets.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
Module for dividing the preprocessed LFW data into training and testing
datasets.

G{packagetree lfw_gender}
"""

__docformat__ = 'epytext'

# Native imports
import os, random, cPickle

# Third party imports
import numpy as np

# Program imports
from lfw_gender.exception_handler import BaseException, wrap_error

###############################################################################
########## Exception Handling
###############################################################################

class InvalidSelectionAmount(BaseException):
	"""
	Exception if the number of requested training and testing items is too
	large.
	"""
	
	def __init__(self, max_instances, requested_instances):
		"""
		Initialize this class.
		
		@param max_instances: The total number of samples available.
		
		@param requested_instances: The total number of samples requested.
		"""
		
		self.msg = wrap_error('There exists a maximum of {0} unique images '
			'per gender. You requested {1} instances. Please reduce your '
			'selection amount and try again'.format(max_instances,
			requested_instances))

###############################################################################
########## Functions
###############################################################################

def get_count(preprocessed_path):
	"""
	Get a count of the number of instances of each person in the preprocessed
	dataset.
	
	@param preprocessed_path: The full path to the preprocessed data. There
	should be a folder for "male" and "female" in this path, containing a
	number of pickle files, representing the desired images.
	"""
	
	# Initializations
	female_names = {}
	male_names   = {}
	genders      = ('male', 'female')
	
	# Loop through each gender
	for gender in genders:
		# Determine the gender
		if gender == 'male':
			d = male_names
		elif gender == 'female':
			d = female_names
		
		# Get the count
		for person in os.listdir(os.path.join(preprocessed_path, gender)):
			name = '_'.join(person.split('_')[:-1])
			try:
				d[name] += 1
			except KeyError:
				d[name] = 0
	
	return male_names, female_names

def build_dataset(names, gender, ntrain, ntest):
	"""
	Generate a dataset for a single gender.
	
	@param names: A distribution of the names for each gender.
	
	@param gender: The gender to use ("male" or "female").
	
	@param ntrain: The number of training samples to use.
	
	@param ntest: The number of testing samples to use.
	
	@return: The training and testing datasets:
	(train_x, train_y), (test_x, test_y)
	"""
	
	# Build the base y set and perform some other initializations
	requested_samples = ntrain + ntest
	if gender == 'male':
		train_y = np.ones(ntrain, dtype='uint8')
		test_y  = np.ones(ntest, dtype='uint8')
	elif gender == 'female':
		train_y = np.zeros(ntrain, dtype='uint8')
		test_y  = np.zeros(ntest, dtype='uint8')
	
	# Randomly select an even number of people
	selected_names = names.keys()
	random.shuffle(selected_names)
	if len(selected_names) != requested_samples:
		del selected_names[requested_samples:]
	
	# Randomly select a single occurrence for chosen person
	files = []
	for n in selected_names:
		idx = random.randint(0, names[n])
		files.append(os.path.join(preprocessed_path, gender,
			'{0}_{1}.pkl'.format(n, idx)))
	
	# Randomly divide the data into training and test sets
	random.shuffle(files)
	data = []
	for file in files:
		with open(file, 'rb') as f:
			data.append(cPickle.load(f))
	train_x = np.array(data[:ntrain], dtype='uint8')
	test_x  = np.array(data[ntrain:], dtype='uint8')
	
	return (train_x, train_y), (test_x, test_y)
	
def main(preprocessed_path, out_dir, ntrain=800, ntest=200):
	"""
	Build the datasets for training and testing. Note that the number of
	training and testing instances must be less than or equal to the total
	number of unique names.
	
	@param preprocessed_path: The full path to the preprocessed data. There
	should be a folder for "male" and "female" in this path, containing a
	number of pickle files, representing the desired images.
	
	@param out_dir: The full path to where the output data should be saved.
	
	@param ntrain: The number of training instances.
	
	@param ntest: The number of testing instances.
	
	@raise InvalidSelectionAmount: Occurs when too many training / testing
	samples were requested.
	"""
	
	# Get the distribution of names
	male_names, female_names = get_count(preprocessed_path)
	
	# Check to see if enough examples exist
	max_samples       = max(len(male_names.keys()), len(female_names.keys()))
	requested_samples = (ntrain + ntest) / 2
	if requested_samples > max_samples:
		raise InvalidSelectionAmount(max_samples, requested_samples)
	
	# Generate the data
	(m_train_x, m_train_y), (m_test_x, m_test_y) = build_dataset(male_names,
		'male',	ntrain / 2, ntest / 2)
	(f_train_x, f_train_y), (f_test_x, f_test_y) = build_dataset(female_names,
		'female', ntrain / 2, ntest / 2)
	
	# Combine the male and female data and randomly shuffle them
	b_train_x = np.concatenate((m_train_x, f_train_x))
	b_train_y = np.concatenate((m_train_y, f_train_y))
	p         = np.random.permutation(len(b_train_x))
	train_x   = b_train_x[p]
	train_y   = b_train_y[p]
	b_test_x  = np.concatenate((m_test_x, f_test_x))
	b_test_y  = np.concatenate((m_test_y, f_test_y))
	p         = np.random.permutation(len(b_test_x))
	test_x    = b_test_x[p]
	test_y    = b_test_y[p]
	
	# Dump the data
	with open(os.path.join(out_dir, 'lfw.pkl'), 'wb') as f:
		cPickle.dump(((train_x, train_y), (test_x, test_y)), f,
			cPickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
	# Get the path, based off the path in the repo
	preprocessed_path = os.path.join(os.path.dirname(os.path.dirname(
		os.path.dirname(os.getcwd()))), 'data', 'preprocessed')
	
	main(preprocessed_path, os.path.join(os.getcwd(), 'data'))