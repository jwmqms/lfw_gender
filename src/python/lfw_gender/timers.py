# timers.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/22/15
#	
# Description    : Module used for timing.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
Module used for timing.

G{packagetree lfw_gender}
"""

__docformat__ = 'epytext'

# Native imports
import time, csv
from itertools import izip

###############################################################################
########## Primary Functions
###############################################################################

def pretty_time(elapsed_time):
	"""
	Get a string representing a formatted time in a pretty (human-readable)
	format.
	
	@param elapsed_time: The number of elapsed seconds.
	"""
	
	# The time labels
	labels          = ('days', 'hours', 'minutes', 'seconds')
	formatted_times = []
	
	# Compute the times
	days    = elapsed_time / 86400.
	i_days  = int(days)
	hours   = (days  - i_days)  * 24
	i_hours = int(hours)
	mins    = (hours - i_hours) * 60
	i_mins  = int(mins)
	seconds = (mins  - i_mins)  * 60
	times   = (i_days, i_hours, i_mins, seconds)
	
	# Format all times but the last element
	for t, l in izip(times[:-1], labels[:-1]):
		if t != 0:
			formatted_times.append('{0} {1}'.format(t, l))
	
	# Format the last element
	if times[-3] != 0:
		str = ', and {0:.3f} {1}'
	elif times[-2] != 0:
		str = ' and {0:.3f} {1}'
	else:
		str = '{0:.3f} {1}'
	
	# Return the formatted time
	return ', '.join(formatted_times) + str.format(times[-1], labels[-1])

###############################################################################
########## Class Implementations
###############################################################################

class SimpleTimer(object):
	"""
	Simple timer used to hold data just about a single timer.
	"""
	
	def __init__(self, name=None):
		"""
		Initialize this timer instance, starting the timer.
		"""
		
		# Init params
		self.name         = name
		self.elapsed_time = 0.
		self.start()
	
	def start(self):
		"""
		Start the timer.
		"""
		
		self.start_time = time.time()
	
	def pause(self):
		"""
		Pauses the timer and compute the elapsed time.
		"""
		
		self.finish_time  = time.time()
		self.elapsed_time += self.finish_time - self.start_time
	
	def stop(self):
		"""
		Stop the timer and compute the elapsed time.
		"""
		
		self.finish_time  = time.time()
		self.elapsed_time = self.finish_time - self.start_time
	
	def get_elapsed_time(self, pretty=False):
		"""
		Return the elapsed time.
		
		@param pretty: If False the time is returned as the elapsed time in
		seconds. If True, the equivalent time breakdown is computed.
		
		@return: The elapsed time.
		"""
		
		# Determine how to format the time
		if not pretty:
			return self.elapsed_time
		else:
			return pretty_time(self.elapsed_time)

class MultiTimer(object):
	"""
	Timer class used to work with multiple timers..
	"""
	
	def __init__(self):
		"""
		Initialize this timer instance.
		"""
		
		self.timers = {}
	
	def add_timers(self, *timer_names):
		"""
		Adds a new timer to the class and starts the timer.
		
		@param timer_names: The name of the timer.
		"""
		
		for timer in timer_names:
			self.timers[timer] = SimpleTimer(timer)
			self.timers[timer].start()
	
	def stop_timers(self, *timer_names):
		"""
		Stop the specified timers.
		
		@param timer_names: One or more timer names to be stopped.
		"""
		
		for timer in timer_names:
			self.timers[timer].stop()
	
	def start_timers(self, *timer_names):
		"""
		Starts the specified timers.
		
		@param timer_names: One or more timer names to be started.
		"""
		
		for timer in timer_names:
			self.timers[timer].start()
	
	def pause_timers(self, *timer_names):
		"""
		Pauses the specified timers.
		
		@param timer_names: One or more timer names to be paused.
		"""
		
		for timer in timer_names:
			self.timers[timer].pause()
	
	def get_elapsed_time(self, timer_name, pretty=False):
		"""
		Retrieve the elapsed time for the specified timer.
		
		@param timer_name: The name of the timer to get the info for.
		
		@param pretty: If False the time is returned as the elapsed time in
		seconds. If True, the equivalent time breakdown is computed.
		
		@return: The elapsed time.
		"""
		
		return self.timers[timer_name].get_elapsed_time(pretty)
	
	def log_timers(self, out_path, header=True):
		"""
		Creates a log CSV file for all timers. Make sure to stop any timers
		before calling this.
		
		@param out_path: The full path to the CSV to write to.
		
		@param header: Flag denoting whether the header should be printed or
		not.
		"""
		
		with open(out_path, 'wb') as f:
			writer = csv.writer(f)
			if header:
				writer.writerow(self.timers.keys())
			writer.writerow([timer.get_elapsed_time() for timer in
				self.timers.values()])