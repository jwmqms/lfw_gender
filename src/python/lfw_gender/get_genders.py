# get_genders.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/22/15
#	
# Description    : Obtain the genders for the LFW people.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
Module for obtaining the genders for the LFW dataset.

G{packagetree lfw_gender}
"""

__docformat__ = 'epytext'

# Native imports
import sys, os, csv

# Third party imports
import requests

def main(lfw_path, out_file):
	"""
	Obtain the genders for the LFW names.
	
	@param lfw_path: The full path to where the raw LFW images are located.
	
	@param out_file: The full path to where the output CSV should be created.
	"""
	
	# Get the names
	names   = list(set([n.split('_')[0].lower() for n in
		os.listdir(lfw_path)]))
	males   = []
	females = []
	
	# Base request
	base_req = 'http://api.genderize.io/?'
	
	# Determine their gender
	for i in xrange(0, len(names), 10):
		# Get the request
		req    = base_req + '&'.join('name[{0}]={1}'.format(i, n) for i, n in
			enumerate(names[i:min(len(names), i + 10)]))
		result = requests.get(req).json()
		
		# Add the names to the lists
		for r in result:
			try:
				if r['probability'] > 0.9:
					if r['gender'] == 'male':
						males.append(r['name'])
					else:
						females.append(r['name'])
			except:
				pass
	
	# Write them to a file
	with open(out_file, 'wb') as f:
		writer = csv.writer(f)
		for male in males:
			writer.writerow([male, 'male'])
		for female in females:
			writer.writerow([female, 'female'])

if __name__ == '__main__':
	# Set the base directory to be the data folder inside the repo
	base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
		os.getcwd()))), 'data')
	
	main(os.path.join(base_dir, 'raw'), os.path.join(base_dir, 'genders.csv'))