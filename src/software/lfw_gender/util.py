# util.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/22/15
#	
# Description    : Utility module.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
Utility module. This module handles any sort of accessory items.

G{packagetree lfw_gender}
"""

__docformat__ = 'epytext'

# Native imports
import os, pkgutil, cPickle

# Third party imports
import numpy as np

# Program imports
from lfw_gender.exception_handler import BaseException, wrap_error

###############################################################################
########## Exception Handling
###############################################################################

class InvalidShape(BaseException):
	"""
	Exception if the provided shape is invalid.
	"""
	
	def __init__(self, shape, valid_shapes=(10, 30)):
		"""
		Initialize this class.
		
		@param shape: The requested shape.
		
		@param valid_shapes: A sequence of the valid shapes.
		"""
		
		self.msg = wrap_error('The shape you requested, {0}, is invalid. The '
			'shape must be one of the following: {1}'.format(shape, ', '.join(
			str(s) for s in valid_shapes)))

###############################################################################
########## Functions
###############################################################################

def get_data(shape=10):
	"""
	Return the example LFW data. This is a subset of the data. There are 400
	samples per gender in the training set (800 total items) and 100 samples
	per gender for the testing set (200 total items).
	
	@param shape: The shape of the image. Valid shapes are 10 for a 10x10 image
	or 30 for a 30x30 image.
	
	@return: A tuple of tuples of the following format:
	(train_data, train_labels), (test_data, test_labels)
	
	@raise InvalidShape: Raised if the provided shape is invalid.
	"""
	
	if shape == 10:
		s = '10x10'
	elif shape == 30:
		s = '30x30'
	else:
		raise InvalidShape(shape)
	
	with open(os.path.join(pkgutil.get_loader('lfw_gender').filename,
		'data', '{0}.pkl'.format(s)), 'rb') as f:
		return cPickle.load(f)