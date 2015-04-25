# exception_handler.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/22/15
#	
# Description    : Module for dealing with all errors.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
Exception handler for this project. This module is used for every single
exception.

G{packagetree lfw_gender}
"""

__docformat__ = 'epytext'

# Native imports
import textwrap

def wrap_error(msg):
	"""
	Wraps an error message such that it will get displayed properly.
	
	@param msg: The error to display.
	
	@return: A string containing the formatted message.
	"""
	
	return '\n  ' + '\n  '.join(textwrap.wrap(msg, 77))
	
class BaseException(Exception):
	"""
	Base class for exception handling in this program.
	"""
	
	def __str__(self):
		"""
		Allows for the exception to throw the message even if it wasn't caught.
		
		@return: The error message.
		"""
		
		return self.msg