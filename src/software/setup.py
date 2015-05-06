# setup.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/22/15
#	
# Description    : Installs the lfw_gender project
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

# Native imports
from distutils.core import setup
import shutil

# Install the program
setup(
	name='lfw_gender',
	version='0.1.0',
	description="Labeled Faces in the Wild - Gender Classification",
	author='James Mnatzaganian',
	author_email='jamesmnatzaganian@outlook.com',
	url='http://techtorials.me',
	packages=['lfw_gender'],
	package_data={'lfw_gender':['data/10x10.pkl','data/30x30.pkl']}
	)

# Remove the unnecessary build folder
try:
	shutil.rmtree('build')
except:
	pass