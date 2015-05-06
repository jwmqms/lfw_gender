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
import os, sys
from   itertools import izip

def main(test_path, source_path):
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
	
	print 'Test Accuracy = {0:2.2f}%'.format((accuracy / c) * 100)

if __name__ == '__main__':
	test_path = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())),
		'data', 'fixed_point', 'test.txt')
	
	main(test_path, sys.argv[1])