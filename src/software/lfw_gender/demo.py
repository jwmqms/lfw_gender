# demo.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/22/15
#	
# Description    : Example showing how to use the CompetitiveLearningClassifier
# network.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
Example showing how to create and use the CompetitiveLearningClassifier.

G{packagetree lfw_gender}
"""

__docformat__ = 'epytext'

# Native imports
import os, cPickle

# Third party imports
import numpy as np

# Program imports
from lfw_gender.preprocess import resize_and_flatten
from lfw_gender.util       import get_data
from lfw_gender.net        import CompetitiveLearningClassifier
from lfw_gender.plot       import plot_epoch, plot_weights

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

def main(train_x, train_y, test_x, test_y, categories, nepochs=1, plot=True,
	verbose=True, nclusters=1, learning_rate=0.001, boost_inc=0.1, 
	boost_dec=0.01, duty_cycle=50, min_duty_cycle=5, min_weight=-1,
	max_weight=1, nrows=1, ncols=1, shape=(10, 10)):
	"""
	Demonstrates the CompetitiveLearningClassifier on LFW.
	
	@param train_x: The data to train with. This must be an iterable
	returning a numpy array.
	
	@param train_y: The labels for the training data. This must be an iterable
	returning a numpy array.
	
	@param test_x: The data to test with. This must be an iterable
	returning a numpy array.
	
	@param test_y: The labels for the testing data. This must be an iterable
	returning a numpy array.
	
	@param categories: A list of the unique categories. This should be an
	iterable containing all of the unique labels in train_y / test_y.
	
	@param nepochs: The number of training epochs to perform.
	
	@param plot: If True, a plot will be created.
	
	@param verbose: If True, the network will print results after every
	iteration.
	
	@param nclusters: The number of clusters.
		
	@param learning_rate: The learning rate to use.
	
	@param boost_inc: The amount to increment the boost by.
	
	@param boost_dec: The amount to decrement the boost by.
	
	@param duty_cycle: The history to retain for activations for each node.
	This is the period minimum activation is compared across. It is a rolling 
	window.
	
	@param min_duty_cycle: The minimum duty cycle. If a node has not been 
	active at least this many times, increment its boost value, else decrement
	it.
	
	@param min_weight: The minimum weight value.
	
	@param max_weight: The maximum weight value.
	
	@param nrows: The number of rows of plots to create for the clusters.
	
	@param ncols: The number of columns of plots to create for the clusters.
	
	@param shape: The shape of the weights. It is assumed that a 1D shape was
	used and is desired to be represented in 2D. Whatever shape is provided
	will be used to reshape the weights. For example, if you had a 10x10 image
	and each weight corresponded to one pixel, you would have a vector with a
	shape of (100, ). This vector would then need to be resized to your desired
	shape of (10, 10).
	
	@return: A tuple containing the training results, testing results, and
	weights, respectively.
	"""
	
	# Create the network
	net =  CompetitiveLearningClassifier(
		ninputs        = train_x.shape[1],
		nclusters      = nclusters,
		categories     = categories,
		learning_rate  = learning_rate,
		boost_inc      = boost_inc,
		boost_dec      = boost_dec,
		duty_cycle     = duty_cycle,
		min_duty_cycle = min_duty_cycle,
		min_weight     = min_weight,
		max_weight     = max_weight
	)
	
	# Run the network
	train_results, test_results = net.run(train_x, train_y, test_x, test_y,
		nepochs, verbose)
	
	# Reshape the weights
	weights = {}
	for category in categories:
		if nclusters == 1:
			weights[category] = [net.cnets[category].weights]
			cluster_titles    = [None]
		else:
			weights[category] = net.cnets[category].weights.T
			cluster_titles    = None
	
	# Plot the results
	if plot:
		# Plot the epochs
		plot_epoch(y_series=(train_results * 100, test_results * 100),
			series_names=('Train', 'Test'), y_bounds=(-5, 105),
			y_label='Accuracy [%]', title='LFW Gender - Example',
			legend_location='upper left')
		
		# Plot the weights for each class
		for category in categories:
			plot_weights(weights[category], nrows, ncols, shape,
				'Weights for Cluster {0}'.format(category),
				cluster_titles=cluster_titles)
	
	return train_results * 100, test_results * 100, weights

def basic_sim(nepochs=20):
	"""
	Perform a basic simulation.
	
	@param nepochs: The number of training epochs to perform.
	"""
	
	# Get the data
	(train_x, train_y), (test_x, test_y) = get_data(30)
	train_x = reshape(train_x, (7, 7))
	test_x  = reshape(test_x, (7, 7))
	
	# Scale pixel values to be between 0 and 1
	# Run the network
	main(train_x=train_x/255., train_y=train_y, test_x=test_x/255.,
		test_y=test_y, categories=(0, 1), nepochs=nepochs)

def bulk(niters, nepochs, verbose=True, plot=True, **kargs):
	"""
	Execute the main network across many simulations.
	
	@param niters: The number of iterations to run for statistical purposes.
	
	@param nepochs: The number of training epochs to perform.
	
	@param verbose: If True, a simple iteration status will be printed.
	
	@param plot: If True, a plot will be generated.
	
	@param kargs: Any keyword arguments to pass to the main network simulation.
	
	@return: A tuple containing: (train_mean, train_std), (test_mean, test_std)
	"""
	
	# Simulate the network
	train_results = np.zeros((niters, nepochs))
	test_results  = np.zeros((niters, nepochs))
	for i in xrange(niters):
		if verbose:
			print 'Executing iteration {0} of {1}'.format(i + 1, niters)
		train_results[i], test_results[i], _ = main(verbose=False, plot=False,
			nepochs=nepochs, **kargs)
	
	# Compute the mean costs
	train_mean = np.mean(train_results, 0)
	test_mean  = np.mean(test_results, 0)
	
	# Compute the standard deviations
	train_std = np.std(train_results, 0)
	test_std  = np.std(test_results, 0)
	
	if plot:
		plot_epoch(y_series=(train_mean, test_mean), y_bounds=(-5, 105),
			legend_location='upper left', series_names=('Train', 'Test'),
			y_errs=(train_std, test_std), y_label='Accuracy [%]',
			title='LFW Gender - {0} Iterations\nBest Test Accuracy = {1:2.2f} '
			'@ {2} Epochs'.format(niters, np.max(test_mean),
			np.argmax(test_mean)))
	
	return (train_mean, train_std), (test_mean, test_std)

def bulk_sim(nepochs=50, niters=10):
	"""
	Perform a simulation across multiple iterations, for statistical purposes.
	
	@param nepochs: The number of training epochs to perform.
	
	@param niters: The number of iterations to run for statistical purposes.
	"""
	
	# Get the data
	(train_x, train_y), (test_x, test_y) = get_data(30)
	train_x = reshape(train_x, (7, 7))
	test_x  = reshape(test_x, (7, 7))
	
	bulk(nepochs=nepochs, niters=niters, train_x=train_x/255., train_y=train_y,
		test_x=test_x/255., test_y=test_y, categories=(0, 1))

def vary_params(out_dir, nepochs=50, niters=10, show_plot=True):
	"""
	Vary some parameters and generate some plots.
	
	@param out_dir: The directory to save the plots in.
	
	@param nepochs: The number of training epochs to perform.
	
	@param niters: The number of iterations to run for statistical purposes.
	
	@param show_plot: If True the plot will be displayed upon creation.
	"""
	
	def vary_image_size():
		"""
		Run an experiment varying the image size.
		"""
		
		# Make a directory for the output
		out_dir2 = os.path.join(out_dir, 'image_size')
		try:
			os.makedirs(out_dir2)
		except OSError:
			pass
		
		# Get the data for a number of image sizes
		sizes = (30, 25, 20, 15, 10, 9, 8, 7, 6, 5, 4)
		(train_x, train_y), (test_x, test_y) = get_data(30)
		test_data = [[train_x / 255., train_y, test_x / 255., test_y]]
		for size in sizes[1:]:
			test_data.append([reshape(train_x, (size, size)) / 255., train_y,
				reshape(test_x, (size, size)) / 255., test_y])
		
		print 'Varying the image size'
		train_results = np.zeros((len(sizes), nepochs))
		train_stds    = np.zeros((len(sizes), nepochs))
		test_results  = np.zeros((len(sizes), nepochs))
		test_stds     = np.zeros((len(sizes), nepochs))
		series_names  = ['Image Size = {0}x{0}'.format(s) for s in sizes]
		for i, size in enumerate(sizes):
			print 'Executing iteration {0} of {1}'.format(i + 1, len(sizes))
			(train_results[i], train_stds[i]), (test_results[i],
				test_stds[i]) = bulk(nepochs=nepochs, niters=niters,
				train_x=test_data[i][0], train_y=test_data[i][1],
				test_x=test_data[i][2], test_y=test_data[i][3],
				categories=(0, 1), plot=False, verbose=False)
		
		# Make training plot
		title    = 'LFW Gender - Training\n10 Iterations, Varying Image Size'
		out_path = os.path.join(out_dir2, 'train_vary_image_size.pdf')
		plot_epoch(y_series=train_results, series_names=series_names,
			# title=title, y_errs=train_stds, y_label='Accuracy [%]',
			y_errs=train_stds, y_label='Accuracy [%]',
			out_path=out_path, legend_location='lower right', show=show_plot,
			y_bounds=(-5, 105))
		
		# Make testing plot
		title    = 'LFW Gender - Testing\n10 Iterations, Varying Image Size'
		out_path = os.path.join(out_dir2, 'test_vary_image_size.pdf')
		plot_epoch(y_series=test_results, series_names=series_names,
			# title=title, y_errs=test_stds, y_label='Accuracy [%]',
			y_errs=test_stds, y_label='Accuracy [%]',
			out_path=out_path, legend_location='lower right', show=show_plot,
			y_bounds=(-5, 105))
		
		# Save data
		with open(os.path.join(out_dir2, 'vary_image_size.pkl'), 'wb') as f:
			cPickle.dump(((train_results, train_stds),
					(test_results, test_stds)), f, cPickle.HIGHEST_PROTOCOL)
	
	def vary_number_clusters():
		"""
		Run an experiment varying the number of clusters.
		"""
		
		# Make a directory for the output
		out_dir2 = os.path.join(out_dir, 'num_clusters')
		try:
			os.makedirs(out_dir2)
		except OSError:
			pass
		
		# Get the data
		nclusters    = (1, 5, 10, 15, 20)
		plot_details = {1:(1, 1), 5:(1, 5), 10:(2, 5), 15:(3, 5), 20:(4, 5)}
		(train_x, train_y), (test_x, test_y) = get_data(30)
		train_x = reshape(train_x, (7, 7)) / 255.
		test_x  = reshape(test_x, (7, 7)) / 255.
		
		print 'Varying the number of clusters'
		train_results = np.zeros((len(nclusters), nepochs))
		train_stds    = np.zeros((len(nclusters), nepochs))
		test_results  = np.zeros((len(nclusters), nepochs))
		test_stds     = np.zeros((len(nclusters), nepochs))
		series_names  = ['{0} Output(s)'.format(c) for c in nclusters]
		for i, ncluster in enumerate(nclusters):
			print 'Executing iteration {0} of {1}'.format(i + 1, len(nclusters))
			(train_results[i], train_stds[i]), (test_results[i],
				test_stds[i]) = bulk(nepochs=nepochs, niters=niters,
				train_x=train_x, train_y=train_y, test_x=test_x, test_y=test_y,
				categories=(0, 1), plot=False, verbose=False,
				nclusters=ncluster)
		
		# Shrink data
		new_train_results = []
		new_train_stds    = []
		idx               = range(0, len(train_results[0]),
			max(len(train_results[0]) / 100, 1)) + [len(train_results[0]) - 1]
		for result, std in zip(train_results, train_stds):
			new_train_results.append(result[idx])
			new_train_stds.append(std[idx])
		
		# Make training plot
		title    = 'LFW Gender - Training\n10 Iterations, Varying Number of ' \
			'Clusters'
		out_path = os.path.join(out_dir2, 'train_vary_number_clusters.pdf')
		plot_epoch(y_series=new_train_results, series_names=series_names,
			# title=title, y_errs=new_train_stds, y_label='Accuracy [%]',
			y_errs=new_train_stds, y_label='Accuracy [%]',
			out_path=out_path, legend_location='lower right', show=show_plot,
			y_bounds=(-5, 105), x_values=idx)
		
		# Shrink data
		new_test_results = []
		new_test_stds    = []
		idx               = range(0, len(test_results[0]),
			max(len(test_results[0]) / 100, 1)) + [len(test_results[0]) - 1]
		for result, std in zip(test_results, test_stds):
			new_test_results.append(result[idx])
			new_test_stds.append(std[idx])
		
		# Make testing plot
		title    = 'LFW Gender - Testing\n10 Iterations, Varying Number of '  \
			'Clusters'
		out_path = os.path.join(out_dir2, 'test_vary_number_clusters.pdf')
		plot_epoch(y_series=new_test_results, series_names=series_names,
			# title=title, y_errs=new_test_stds, y_label='Accuracy [%]',
			y_errs=new_test_stds, y_label='Accuracy [%]',
			out_path=out_path, legend_location='lower right', show=show_plot,
			y_bounds=(-5, 105), x_values=idx)
		
		# Generate some cluster images
		# for ncluster in nclusters:
			# weights = main(train_x=train_x, train_y=train_y, test_x=test_x,
				# test_y=test_y, nepochs=nepochs,	nclusters=ncluster,
				# categories=(0, 1), plot=False, verbose=False)[-1]
			# if ncluster == 1:
				# cluster_titles = [None]
			# else:
				# cluster_titles = None
			# for category in (0, 1):
				# plot_weights(weights[category], plot_details[ncluster][0],
					# plot_details[ncluster][1], (10, 10),
					# 'Weights for Cluster {0}'.format(category),
					# cluster_titles=cluster_titles, show=False,
					# out_path=os.path.join(out_dir2,
					# '{0}_{1}_clusters.png'.format(ncluster, 'male' if category
					# == 1 else 'female')))
		
		# Save data
		with open(os.path.join(out_dir2, 'vary_image_size.pkl'), 'wb') as f:
			cPickle.dump(((new_train_results, new_train_stds),
					(new_test_results, new_test_stds)), f,
					cPickle.HIGHEST_PROTOCOL)
	
	def vary_learning_rate():
		"""
		Run an experiment varying the learning rate.
		"""
		
		# Make a directory for the output
		out_dir2 = os.path.join(out_dir, 'learning_rate')
		try:
			os.makedirs(out_dir2)
		except OSError:
			pass
		
		# Get the data
		learning_rates = (0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1)
		(train_x, train_y), (test_x, test_y) = get_data(30)
		train_x = reshape(train_x, (7, 7)) / 255.
		test_x  = reshape(test_x, (7, 7)) / 255.
		
		print 'Varying the learning rate'
		train_results = np.zeros((len(learning_rates), nepochs))
		train_stds    = np.zeros((len(learning_rates), nepochs))
		test_results  = np.zeros((len(learning_rates), nepochs))
		test_stds     = np.zeros((len(learning_rates), nepochs))
		series_names  = ['Learning Rate of {0:1.0e}'.format(lr) for lr in
			learning_rates]
		for i, lr in enumerate(learning_rates):
			print 'Executing iteration {0} of {1}'.format(i + 1,
				len(learning_rates))
			(train_results[i], train_stds[i]), (test_results[i],
				test_stds[i]) = bulk(nepochs=nepochs, niters=niters,
				train_x=train_x, train_y=train_y, test_x=test_x, test_y=test_y,
				categories=(0, 1), plot=False, verbose=False,
				learning_rate=lr)
		
		# Shrink data
		new_train_results = []
		new_train_stds    = []
		idx               = range(0, len(train_results[0]),
			max(len(train_results[0]) / 100, 1)) + [len(train_results[0]) - 1]		
		for result, std in zip(train_results, train_stds):
			new_train_results.append(result[idx])
			new_train_stds.append(std[idx])
		
		# Make training plot
		title    = 'LFW Gender - Training\n10 Iterations, Varying Learning '  \
			'Rate'
		out_path = os.path.join(out_dir2, 'train_vary_learning_rate.pdf')
		plot_epoch(y_series=new_train_results, series_names=series_names,
			# title=title, y_errs=new_train_stds, y_label='Accuracy [%]',
			y_errs=new_train_stds, y_label='Accuracy [%]',
			out_path=out_path, legend_location='lower right', show=show_plot,
			y_bounds=(-5, 105), x_values=idx)
		
		# Shrink data
		new_test_results = []
		new_test_stds    = []
		idx               = range(0, len(test_results[0]),
			max(len(test_results[0]) / 100, 1)) + [len(test_results[0]) - 1]
		for result, std in zip(test_results, test_stds):
			new_test_results.append(result[idx])
			new_test_stds.append(std[idx])
		
		# Make testing plot
		title    = 'LFW Gender - Testing\n10 Iterations, Varying Learning '   \
			'Rate'
		out_path = os.path.join(out_dir2, 'test_vary_learning_rate.pdf')
		plot_epoch(y_series=new_test_results, series_names=series_names,
			# title=title, y_errs=new_test_stds, y_label='Accuracy [%]',
			y_errs=new_test_stds, y_label='Accuracy [%]',
			out_path=out_path, legend_location='lower right', show=show_plot,
			y_bounds=(-5, 105), x_values=idx)
		
		# Save data
		with open(os.path.join(out_dir2, 'vary_learning_rate.pkl'), 'wb') as f:
			cPickle.dump(((new_train_results, new_train_stds),
					(new_test_results, new_test_stds)), f,
					cPickle.HIGHEST_PROTOCOL)
	
	vary_image_size()
	vary_number_clusters()
	vary_learning_rate()

if __name__ == '__main__':
	# The results path (currently set to the path in the repo)
	out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
		os.getcwd()))), 'results', 'tmp')
	
	basic_sim()
	# bulk_sim()
	# vary_params(out_dir, nepochs=300, niters=10, show_plot=False)