# __init__.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/22/15
#	
# Description    : Defines the lfw_gender package.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
This is a suite for performing gender classification on the LFW dataset.

Legal
=====
	This code is licensed under the U{MIT license<http://opensource.org/
	licenses/mit-license.php>}. The dataset we are using originated from
	U{here<http://vis-www.cs.umass.edu/lfw/>}. Additionally, we are using a
	preprocessed, frontalized, version of this dataset, which was obtained from
	U{here<http://www.openu.ac.il/home/hassner/projects/frontalize/>}. Please
	refer to the licensing of those datasets for more details. These authors
	claim no ownership of those datasets and merely provided the dataset for
	convenience purposes, only.

Prerequisites
=============
	- U{Python 2.7.X<https://www.python.org/downloads/release/python-279/>}
	- U{Numpy<http://www.numpy.org/>}
	- U{matplotlib<http://matplotlib.org/>}
	- U{requests<http://docs.python-requests.org/en/latest/>} - Only required
	if the genders are being updated.
	- U{scipy<http://www.scipy.org/>} - Only required if you are redoing the
	image processing.

Installation
============
	1. Install all prerequisites
		Assuming you have U{pip<https://pip.pypa.io/en/latest/installing.html>}
		installed, located in your X{Python27/Scripts} directory:
		
		X{pip install numpy matplotlib requests scipy}
	2. Install this package: X{python setup.py install}. The setup file is
	located in the "src/python" folder.

Getting Started
===============
	Click U{here<http://techtorials.me/lfw_gender/index.html>} to access the
	API.
	
	Initial Workflow
	----------------
	1. Build the project.
		- Inside the repo go to "src/python".
		- Execute  X{python setup.py install}.
	
	2. Generate the updated genders.
		- Inside the repo go to "src/python/lfw_gender".
		- Execute  X{python get_genders.py}. You should have the file
		"data/genders.csv", which is a list of first names and genders.
	
	3. Preprocess the data.
		- Inside the repo go to "src/python/lfw_gender".
		- Execute  X{python preporcess.py}. You should have a folder
		"data/preprocessed". Inside of that folder there should be a "male" and
		"female" folder. Inside each of those folders will be a pickled file
		containing the preprocessed image. Note that these files are not
		deleted. If you update the genders, you should delete all of those
		pickle files and update them again. If you don't update the images, but
		change the preprocessing, the files will be overwritten automatically.
	
	4. Split the data.
		- Inside the repo go to "src/python/lfw_gender".
		- Execute  X{python split_data.py}. The pickle file 
		"src/python/lfw_gender/data/lfw.pkl" will be created. The file will
		have the data stored in the format of:
		X{(train_x, train_y), (test_x, test_y)}.
	
	5. Rebuild the project. After this step, you can use the updated images as
	you normally would. They will be included in the package.
		- Inside the repo go to "src/python".
		- Execute X{python setup.py install}.

Package Organization
====================
	The lfw_gender package contains the following subpackages and modules:

	G{packagetree lfw_gender}

Connectivity
============
	The following image shows how everything is connected:

	G{importgraph}

Developer Notes
===============
	The following notes are for developers only.

	Installation
	------------
		1.  Download and install U{graphviz<http://www.graphviz.org/Download..
		php>}
		2.  Edit line 111 in X{epydoc_config.txt} to point to the directory
		containing "dot.exe". This is part of the graphviz installation.
		3.  Download this repo and execute X{python setup.py install}.
		4.  Download and install U{Epydoc<http://sourceforge.net/projects/
		epydoc/files>}

	Generating the API
	------------------
		From the root level, execute X{python epydoc --config=epydoc_config.txt
		lfw_gender}

@author: U{James Mnatzaganian<http://techtorials.me>}
@requires: Python 2.7.X
@version: 0.1.0
@license: U{The MIT License<http://opensource.org/licenses/mit-license.php>}
@copyright: S{copy} 2015 James Mnatzaganian
"""

__docformat__ = 'epytext'