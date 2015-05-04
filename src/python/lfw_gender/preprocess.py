# preprocess.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/22/15
#	
# Description    : Preprocess the LFW data.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
Module for preprocessing LFW dataset.

G{packagetree lfw_gender}
"""

__docformat__ = 'epytext'

# Native imports
import os, csv, cPickle

# Third party imports
import numpy      as     np
from   scipy.misc import imread, imresize

def read_img(path):
	"""
	Read an image from a given path.
	
	@param path: The full path to the image.
	
	@return: A numpy array representing the image.
	"""
	
	return imread(path)

def rgb_to_gray(rgb, dtype=np.uint8):
	"""
	Convert an RGB image to grayscale.
	
	@param rgb: The RGB image (numpy array with three pixel values per each
	pixel, where the image is 2D).
	
	@param dtype: The dtype to use.
	
	@return: The grayscale image (2D numpy array).
	"""
	
	return np.dot(rgb, [0.2989, 0.5870, 0.1140]).astype(np.uint8)

def resize_and_flatten(img, shape=(30, 30)):
	"""
	Resize an image and then flatten it.
	
	@param img: The 2D image to work with (numpy array).
	
	@param shape: The shape to resize the image.
	
	@return: A vector containing the flattened, resized image.
	"""
	
	return imresize(img, shape).ravel()

def reshape(data, shape):
	"""
	Resize the images from the original 30x30 size to any other desired size.
	
	@param data: A numpy array containing multiple images.
	
	@param shape: The new image shape to experiment with.
	"""
	
	d = np.zeros((data.shape[0], shape[0] * shape[1]), 'uint8')
	for i, img in enumerate(data):
		d[i] = resize_and_flatten(img.reshape((30, 30)), shape)
	return np.array(d, dtype='uint8')

def get_genders(img_path, gender_path):
	"""
	Get a dictionary containing a list of male and female path names.
	
	@param img_path: The full path to the raw images.
	
	@param gender_path: The full path to the CSV containing the gender data.
	
	@return: A dictionary of the format {'male':[...], 'female':[...]}.
	"""
	
	# Get the genders
	genders = {'male':set(), 'female':set()}
	with open(gender_path, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			genders[row[1]].add(row[0])
	
	# Get the paths
	paths = [(n.split('_')[0].lower(), n) for n in os.listdir(img_path)]
	
	# Split out the genders
	final_genders = {'male':[], 'female':[]}
	for test_name, path_name in paths:
		if test_name in genders['male']:
			final_genders['male'].append(os.path.join(img_path, path_name))
		elif test_name in genders['female']:
			final_genders['female'].append(os.path.join(img_path, path_name))
	
	return final_genders

def main(img_path, gender_path, out_path, shape=(30, 30)):
	"""
	Preprocess the data:
		1. Reduces image set to only images with genders
		2. Converts images to grayscale
		3. Resizes the images
		4. Saves the new images in a pkl file, one for each image
	
	@param img_path: The full path to the raw images.
	
	@param gender_path: The full path to the CSV containing the gender data.
	
	@param out_path: The full path to where the preprocessed data should be
	saved.
	
	@param shape: The shape to resize the images to.
	"""
	
	# Figure out which genders are valid
	final_genders = get_genders(img_path, gender_path)
	
	# Loop through each gender
	for gender in final_genders:
		# Determine which gender to work with
		if gender == 'male':
			base_path = os.path.join(out_path, 'male')
		elif gender == 'female':
			base_path = os.path.join(out_path, 'female')
		
		# Loop through all of the people
		for person in final_genders[gender]:
			# Loop through each person's images
			for i, f in enumerate(os.listdir(person)):
				# Process the image
				p   = os.path.join(person, f)
				img = resize_and_flatten(rgb_to_gray(read_img(p)), shape)
				
				# Save the image
				file_name = '{0}_{1}.pkl'.format(os.path.basename(person), i)
				with open(os.path.join(base_path, file_name), 'wb') as f:
					cPickle.dump(img, f, cPickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
	# Set the base directory to be the data folder inside the repo
	base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
		os.getcwd()))), 'data')
	
	main(os.path.join(base_dir, 'raw'), os.path.join(base_dir, 'genders.csv'),
		os.path.join(base_dir, 'preprocessed'))