# plot.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/22/15
#	
# Description    : Module for plotting.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
Module for plotting.

G{packagetree lfw_gender}
"""

__docformat__ = 'epytext'

# Native imports
import itertools

# Third-Party imports
import numpy                as     np
import matplotlib.pyplot    as     plt
from   matplotlib           import rcParams
from   mpl_toolkits.mplot3d import Axes3D

params = {
		'backend'             : 'ps',
		# 'text.usetex'       : True,
		# 'text.latex.preamble' : ['\usepackage{gensymb}'],
		'axes.labelsize'      : 20,
		'axes.titlesize'      : 20,
		'text.fontsize'       : 20,
		'legend.fontsize'     : 20,
		'xtick.labelsize'     : 20,
		'ytick.labelsize'     : 20,
		'font.family'         : 'serif',
		'lines.linewidth'     : 2
	}
rcParams.update(params)

def plot_epoch(y_series, x_values=None, series_names=None, y_errs=None,
	y_bounds=None, y_label=None, title=None, semilog=False,
	legend_location='best', out_path=None, show=True):
	"""
	Basic plotter function for plotting various types of data against
	training epochs. Each item in the series should correspond to a single
	data point for that epoch.
	
	@param y_series: A tuple containing all of the desired series to plot.
	
	@param x_values: The x_values shared between all y_series.
	
	@param series_names: A tuple containing the names of the series.
	
	@param y_errs: The error in the y values. There should be one per series
	per datapoint. It is assumed this is the standard deviation, but any error
	will work.
	
	@param y_bounds: The bounds to use for the y-axis. This should be a tuple
	containing the upper and lower bounds. If None, then it will autofit.
	
	@param y_label: The label to use for the y-axis.
	
	@param title: The name of the plot.
	
	@param semilog: If True the y-axis will be plotted using a log(10) scale.
	
	@param legend_location: The location of where the legend should be placed.
	Refer to matplotlib's U{docs<http://matplotlib.org/api/pyplot_api.html#
	matplotlib.pyplot.legend>} for more details.
	
	@param out_path: The full path to where the image should be saved. The file
	extension of this path will be used as the format type. If this value is
	None then the plot will not be saved, but displayed only.
	
	@param show: If True the plot will be show upon creation.
	"""
	
	# Construct the basic plot
	fig, ax = plt.subplots()
	if title   : plt.title(title)
	if semilog : ax.set_yscale('log')
	if y_label : ax.set_ylabel(y_label)
	ax.set_xlabel('Epoch')
	if x_values is not None:
		m = x_values[-1] + 1
	else:
		m = max([x.shape[0] for x in y_series])
	plt.xlim((0, m + 1))
	if m >= 10:
		ticks = range(0, m + m / 10, m / 10)
	else:
		ticks = range(0, m + 1, 1)
	tick_marks = ticks[:]; tick_marks[0] = ''
	plt.xticks(ticks, tick_marks)
	if y_bounds is not None: plt.ylim(y_bounds)
	colormap = plt.cm.brg
	colors   = itertools.cycle([colormap(i) for i in np.linspace(0, 0.9,
		len(y_series))])
	markers  = itertools.cycle(['.', ',', 'o', 'v', '^', '<', '>', '1', '2',
		'3', '4', '8', 's', 'p', '*', 'p', 'h', 'H', '+', 'D', 'd', '|', '_',
		'TICKLEFT', 'TICKRIGHT', 'TICKUP', 'TICKDOWN', 'CARETLEFT',
		'CARETRIGHT', 'CARETUP', 'CARETDOWN'])
	
	# Add the data
	if y_errs is not None:
		for y, err in zip(y_series, y_errs):
			if x_values is None:
				x_values = np.arange(1, x.shape[0] + 1)
			ax.errorbar(x_values, y, yerr=err, color=colors.next(),
				marker=markers.next())
	else:
		for y in y_series:
			if x_values is None:
				x_values = np.arange(1, x.shape[0] + 1)
			ax.scatter(x_values, y, color=colors.next(), marker=markers.next())
	
	# Create the legend
	if series_names: plt.legend(series_names, loc=legend_location)
	
	# Save the plot
	fig.set_size_inches(19.20, 10.80)
	if out_path:
		plt.savefig(out_path, format=out_path.split('.')[-1], dpi = 100)
	
	# Show the plot and close it after the user is done
	if show: plt.show()
	plt.close()

def plot_weights(weights, nrows, ncols, shape, title=None, cluster_titles=None,
	out_path=None, show=True):
	"""
	Plot the weight matrices for the network.
	
	@param weights: A numpy array containing a weight matrix. Each row in the
	array corresponds to a unique node. Each column corresponds to a weight
	value.
	
	@param nrows: The number of rows of plots to create.
	
	@param ncols: The number of columns of plots to create.
	
	@param shape: The shape of the weights. It is assumed that a 1D shape was
	used and is desired to be represented in 2D. Whatever shape is provided
	will be used to reshape the weights. For example, if you had a 28x28 image
	and each weight corresponded to one pixel, you would have a vector with a
	shape of (784, ). This vector would then need to be resized to your desired
	shape of (28, 28).
	
	@param title: The name of the plot.
	
	@param cluster_titles: The titles for each of the clusters.
	
	@param out_path: The full path to where the image should be saved. The file
	extension of this path will be used as the format type. If this value is
	None then the plot will not be saved, but displayed only.
	
	@param show: If True the plot will be show upon creation.
	"""
	
	# Construct the basic plot
	fig = plt.figure()
	if title is not None: fig.suptitle(title, fontsize=16)
	if cluster_titles is None:
		cluster_titles = ['Node {0}'.format(i) for i in xrange(len(weights))]
	
	# Add all of the figures to the grid
	for i, weight_set in enumerate(weights):
		ax = plt.subplot(nrows, ncols, i + 1)
		if cluster_titles[i]:
			ax.set_title(cluster_titles[i])
		ax.imshow(weight_set.reshape(shape), cmap=plt.cm.gray)
		ax.axes.get_xaxis().set_visible(False)
		ax.axes.get_yaxis().set_visible(False)
	
	# Save the plot
	fig.set_size_inches(19.20, 10.80)
	if out_path is not None:
		plt.savefig(out_path, format=out_path.split('.')[-1], dpi = 100)
	
	# Show the plot and close it after the user is done
	if show: plt.show()
	plt.close()

def show_image(img, shape=(10, 10)):
	"""
	Plot a single image.
	
	@param img: A numpy vector representing the flattend image.
	
	@param shape: The original dimensions of the image.
	"""
	
	plt.imshow(img.reshape(shape), cmap=plt.get_cmap('gray'))
	plt.show()

def make_grid(data):
	"""
	Convert the properly spaced, but unorganized data into a proper 3D grid.
	
	@param data: A sequence containing of data of the form (x, y, z). x and y
	are independent variables and z is the dependent variable.
	
	@return: A tuple containing the new x, y, and z data.
	"""
	
	# Sort the data
	x, y, z  = np.array(sorted(data, key=lambda x: (x[0], x[1]))).T
	xi       = np.array(sorted(list(set(x))))
	yi       = np.array(sorted(list(set(y))))
	xim, yim = np.meshgrid(xi, yi)
	zi       = z.reshape(xim.shape)
	
	return (xim, yim, zi)

def plot_surface(x, y, z, x_label=None, y_label=None, z_label=None,
	x_limits=None, y_limits=None, z_limits=None, vmin=None, vmax=None,
	title=None, out_path=None, show=True):
	"""
	Basic plotter function for plotting scatter plots
	
	@param x: A sequence containing the x-axis data.
	
	@param y: A sequence containing the y-axis data.
	
	@param z: A sequence containing the z-axis data.
	
	@param x_label: The label to use for the x-axis.
	
	@param y_label: The label to use for the y-axis.
	
	@param z_label: The label to use for the z-axis.
	
	@param x_limits: A sequence containing the minimum and maximum values,
	respectively for the x-axis.
	
	@param y_limits: A sequence containing the minimum and maximum values,
	respectively for the y-axis.
	
	@param z_limits: A sequence containing the minimum and maximum values,
	respectively for the z-axis.
	
	@param vmin: The minimum value to map to the plot.
	
	@param vmax: The maximum value to map to the plot.
	
	@param title: The name of the plot.
	
	@param out_path: The full path to where the image should be saved. The file
	extension of this path will be used as the format type. If this value is
	None then the plot will not be saved, but displayed only.
	
	@param show: If True the plot will be show upon creation.
	"""
	
	# Construct the basic plot
	fig  = plt.figure()
	ax   = fig.add_subplot(111, projection='3d')
	surf = ax.plot_surface(x, y, z, cmap=plt.cm.jet, rstride=1, cstride=1,
		linewidth=0, vmin=vmin, vmax=vmax)
	if x_limits is not None: ax.set_xlim3d(x_limits)
	if y_limits is not None: ax.set_ylim3d(y_limits)
	if z_limits is not None: ax.set_zlim3d(z_limits)
	fig.colorbar(surf, shrink=0.5, aspect=15, pad=-0.05)
	ax.view_init(azim=58, elev=28)
	
	# Add the labels
	if title   : plt.title(title)
	if x_label : ax.set_xlabel(x_label)
	if y_label : ax.set_ylabel(y_label)
	if z_label : ax.set_zlabel(z_label)
	
	ax.patch.set_facecolor('white')
	ax.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
	ax.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
	ax.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
	
	# Save the plot
	fig.set_size_inches(19.20, 10.80)
	if out_path:
		plt.savefig(out_path, format=out_path.split('.')[-1], dpi = 100)
	
	# Show the plot and close it after the user is done
	if show: plt.show()
	plt.close()