# generate_hw_data.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/29/15
#	
# Description    : Reformat the data, for HW purposes.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
Reformat the data, for HW purposes.

G{packagetree lfw_gender}
"""

__docformat__ = 'epytext'

# Native imports
import os

# Third party imports
import numpy as np

# Program imports
from lfw_gender.q_format   import imgs_to_fp
from lfw_gender.preprocess import reshape
from lfw_gender.util       import get_data

def output_data(dir, x, y):
	"""
	Output the provided data.
	
	@param dir: The full path to the directory to create the files in.
	
	@param x: The x-data.
	
	@param y: The y-data.
	"""
	
	i = 0
	for xi, yi in zip(x, y):
		i += 1
		with open(os.path.join(dir, '{0}.txt'.format(i)), 'wb') as f:
			f.write('{0}\n'.format(yi))
			for m7 in xrange(7, 50, 7):
				f.write('{0}\n'.format(' '.join(str(fp) for fp in
					xi[m7-7:m7])))

def generate_data(train_dir, test_dir, imsize=7, m=1, n=11):
	"""
	Generate the test cases into the format required for HW testing.
	
	@param train_dir: The full path to the training directory.
	
	@param test_dir: The full path to the testing directory.
	
	@param imsize: The size of the image to work with.
	
	@param m: The number of integer bits for fixed point.
		
	@param n: The number of fractional bits for fixed point.
	"""
	
	# Get the data	
	(train_x, train_y), (test_x, test_y) = get_data(30)
	train_x = reshape(train_x, (7, 7))
	test_x  = reshape(test_x, (7, 7))
	
	# Convert to fixed point
	train_x_fp = imgs_to_fp(train_x/255., m, n)
	test_x_fp  = imgs_to_fp(test_x/255., m, n)
	
	# Output data
	output_data(train_dir, train_x_fp, train_y)
	output_data(test_dir, test_x_fp, test_y)

if __name__ == '__main__':
	# The results path (currently set to the path in the repo)
	base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
		os.getcwd()))), 'data', 'fixed_point')
	
	generate_data(os.path.join(base_dir, 'train'),
		os.path.join(base_dir, 'test'))