# q_format.py
#	
# Author         : James Mnatzaganian
# Contact        : http://techtorials.me
# Date Created   : 04/29/15
#	
# Description    : Module for dealing with Q formatted numbers.
# Python Version : 2.7.8
#
# License        : MIT License http://opensource.org/licenses/mit-license.php
# Copyright      : (c) 2015 James Mnatzaganian

"""
Module for dealing with Q formatted numbers.
"""
__docformat__ = 'epytext'

# Program imports
from lfw_gender.exception_handler import wrap_error, BaseException

###############################################################################
########## Exception Handling
###############################################################################

class InvalidQNumber(BaseException):
	"""
	Exception raise if the Q formatted number is invalid. This occurs when the
	number of bits does not match the format.
	"""
	
	def __init__(self, q, num_bits):
		"""
		Initializes this class.
		
		@param q: The Q formatted number.
		
		@param num_bits: The number of bits supported by the format.
		"""
		
		self.msg = wrap_error('The Q formatted number, {0}, has {1} bits. Only'
			' {2} bits are allowed in this format. Change the format for '
			'decoding or fix your Q formatted number.'.format(q, len(q),
			num_bits))

###############################################################################
########## Classes
###############################################################################

class Q(object):
	"""
	Class for a Q formatted number.
	
	The MSB will be the sign bit, with '1' for negative and '0' for positive.
	The bits from MSB-1 to MSB-1-m represent the integer portion of the number,
	where the parameter 'm' is used to determine the length of the integer
	portion. The bits from MSB-1-m to LSB represent the fractional portion of
	the number. The bit count for the fractional portion is determined by the
	parameter 'n'.
	
	NOTE - This is a lossy operation. Conversions from a scalar to the Q format
	and back may result in a loss of data. This is based off the provided
	precision for "m" and "n".
	
	For example:
		The number 1.125 is represented as 01.0010 if m = 1 and n = 4.
		The integer portion '1' is represented as '01', '0' for a positive
		sign and '1' for the binary equivalent of '1'.
		The fractional portion '.125' is represented in binary as '0010'.
		0 * 2^-1 + 0 * 2^-2 + 1 * 2^-2 + 0 * 2^-3 = 0.125
		
		The number -1.25 is represented as 10.1100 if m = 1 and n = 4.
		The integer portion '1' is represented as '10', which in 2's
		complement is '01', so resulting in a -1.
		The integer portion, without 2's complement is equal to -2. To obtain
		the number -1.25, 0.75 must be added to the number. 0.75 represented
		in this format is 1100.
		1 * 2^-1 + 1 * 2^-2 + 0 * 2^-2 + 0 * 2^-3 = 0.75
	
	"""
	
	def __init__(self, m, n, scalar=None):
		"""
		Initializes this class.
		
		@param m: The number of integer bits.
		
		@param n: The number of fractional bits.
		
		@param scalar: The number to convert to fixed point. If provided, this
		object will be used as a data type. If it isn't provided, this object
		will be used to perform conversions.
		"""
		
		self.m        = m
		self.n        = n
		self.num_bits = m + n + 1
		
		if scalar is not None:
			self.q_num = self.encode(scalar)
	
	def _clamp(self, q):
		"""
		Check the q number for overflow and underflow and then clamp at the
		max and min bounds:
		
		@param q: The Q formatted number to clamp.
		"""
		
		# Check for overflow and underflow
		if len(q) > self.num_bits:
			if q[0] == 1:
				return '1' * (self.m + 1) + '0' * self.n
			else:
				return '0' + '1' * (self.m + self.n)
		else:
			return q
	
	def _check_q_num(self, q):
		"""
		Verifies that a Q formatted number is valid.
		
		@param q: The Q formatted number to check.
		
		@raise: IvalidQNumber when the number of bits is bad.
		@raise: Exception when the format is invalid.
		"""
		
		try:
			len(q)
		except:
			raise Exception('Q formatted number must be a string!')
		
		if len(q) != self.num_bits:
				raise InvalidQNumber(q, self.num_bits)
		
	def get_pretty_q_format(self, q):
		"""
		Returns a Q formatted number with a decimal point for easier human
		understanding.
		
		@param q: A string containing the q formatted number.
		
		@return: A Q formatted number with an added decimal point.
		"""
		
		return q[:self.m+1] + '.' + q[self.m+1:]
		
	def encode(self, scalar):
		"""
		Encodes a scalar to a Q formatted number.
		
		@param scalar: The scalar being converted.
		
		@return: A string representing the Q point number.
		"""
		
		sign   = int(scalar < 0)
		scalar = abs(scalar)
		
		# Separate the integer, i, and fractional, f, portions
		i = int(scalar)
		f = scalar - i
		
		# Build the binary representation for the integer portion
		bi = str(bin(i))[2:].zfill(self.m)
		
		# Build the binary representation for the fractional portion
		bf  = []
		val = 0
		for iter in xrange(1, self.n+1):
			temp = val + pow(2, iter*-1)
			if temp <= f:
				val = temp
				bf.append('1')
			else:
				bf.append('0')
		
		# Create q number
		q_num = bi + ''.join(bf)
		
		# Use 2's complement to convert negative number
		if sign:
			# Invert the bits
			q_num = ''.join('1' if bit == '0' else '0' for bit in q_num)
			
			# Add 1 and insert sign
			q_num =  '1' + bin(int(q_num, 2) + 1)[2:].zfill(self.num_bits - 1)
			
			# Check for underflow
			if len(q_num) > self.num_bits:
				q_num = q_num[:-1]
			
			# Check for poor encoding (required for numbers close to 0)
			if abs(self.decode(q_num)) > scalar:
				return '0' * self.num_bits
		else:
			q_num = '0' + q_num
		
		return q_num
		
	def decode(self, q):
		"""
		Decodes a Q formatted number to a scalar.
		
		@param q: The Q formatted number being converted.
		
		@return: The float equivalent to the Q formatted number.
		"""
		
		# Check the number
		self._check_q_num(q)
		
		# Extract bits
		sign = int(q[0])
		bi   = q[1:self.m+1]
		bf   = q[self.m+1:]
		
		# Determine the integer portion
		if sign:
			bi = ''.join('1' if x == '0' else '0' for x in bi)
			si = float(int(bi,2)) * -1
		else:
			si = float(int(bi,2))
		
		# Determine the fraction portion
		f = sum([int(bit) * pow(2, i * -1) for i, bit in enumerate(bf, 1)])
		if sign:
			f -= 1
		
		return si + f
		
	def add(self, q0, q1):
		"""
		Adds two Q formatted numbers.
		
		@param q0: A Q formatted number.
		
		@param q1: A Q formatted number.
		
		@return: The addition of q0 and q1 as a Q formatted number.
		"""
		
		# Error checking
		self._check_q_num(q0)
		self._check_q_num(q1)
		
		# Perform addition
		val   = self.decode(q0) + self.decode(q1)
		q_num = self._clamp(self.encode(val))
		
		# Enforce encoded number to be smaller than the actual result
		if self.decode(q_num) > val:
			q_num = self.add(q_num, '1' * (self.m + self.n + 1))
		
		# Check for overflow and underflow
		return self._clamp(q_num)
	
	def mult(self, q0, q1):
		"""
		Multiplies two Q formatted numbers.
		
		@param q0: A Q formatted number.
		
		@param q1: A Q formatted number.
		
		@return: The product of q0 and q1 as a Q formatted number.
		"""
		
		# Error checking
		self._check_q_num(q0)
		self._check_q_num(q1)
		
		# Perform multiplication
		val   = self.decode(q0) * self.decode(q1)
		q_num = self._clamp(self.encode(val))
		
		# Enforce encoded number to be smaller than the actual result
		if self.decode(q_num) > val:
			return self.add(q_num, '1' * (self.m + self.n + 1))
		else:
			return q_num
		
		# Check for overflow and underflow
		return self._clamp(q_num)
	
	def __repr__(self):
		return self.get_pretty_q_format(self.q_num)
	
	def __str__(self):
		return self.q_num
	
	def __hash__(self):
		return hash(self.q_num)
	
	def __eq__(self, q):
		return self.q_num == q.q_num
	
	def __ne__(self, q):
		return self.q_num != q.q_num
	
	def __lt__(self, q):
		return self.decode(self.q_num) < self.decode(q.q_num)
	
	def __le__(self, q):
		return self.decode(self.q_num) <= self.decode(q.q_num)
	
	def __gt__(self, q):
		return self.decode(self.q_num) > self.decode(q.q_num)
	
	def __ge__(self, q):
		return self.decode(self.q_num) >= self.decode(q.q_num)
	
	def __add__(self, q):
		return Q(self.m, self.n, self.decode(self.add(self.q_num, q.q_num)))
	
	def __iadd__(self, q):
		self.q_num = self.add(self.q_num, q.q_num)
		return self
	
	def __sub__(self, q):
		return Q(self.m, self.n, self.decode(self.add(self.q_num,
			self.encode(-self.decode(q.q_num)))))
	
	def __isub__(self, q):
		self.q_num = self.add(self.q_num, self.encode(-self.decode(q.q_num)))
		return self
	
	def __mul__(self, q):
		return Q(self.m, self.n, self.decode(self.mult(self.q_num, q.q_num)))
	
	def __imul__(self, q):
		self.q_num = self.mult(self.q_num, q.q_num)
		return self
	
	def __pow__(self, num):
		val = Q(self.m, self.n, self.decode(self.q_num))
		for _ in xrange(num - 1):
			val = Q(self.m, self.n, self.decode(self.mult(self.q_num,
				str(val))))
		return val
	
	def __ipow__(self, num):
		val = Q(self.m, self.n, self.decode(self.q_num))
		for _ in xrange(num - 1):
			val = Q(self.m, self.n, self.decode(self.mult(self.q_num,
				str(val))))
		self.q_num = val.q_num
		return self

###############################################################################
########## Functions
###############################################################################

def imgs_to_fp(x, m, n):
	"""
	Convert a list of images to fixed point.
	
	@param x: The data.
	
	@param m: The number of integer bits for fixed point.
		
	@param n: The number of fractional bits for fixed point.
	
	@return: A list of fixed point values represented the encoded images.
	"""
	
	return [[Q(m, n, y) for y in xi] for xi in x]

def fps_to_imgs(x, m, n):
	"""
	Convert a list of fixed point images to floating point.
	
	@param x: The data.
	
	@param m: The number of integer bits for fixed point.
		
	@param n: The number of fractional bits for fixed point.
	
	@return: A list of fixed point values represented the encoded images.
	"""
	
	return np.array([np.array([y.decode(y.q_num) for y in xi]) for xi in x])

def test_cases():
	"""
	An example usage for the Q class.
	See the internal comments for more details.
	"""
	
	# Some numbers to encode
	cases   = [-0.6875, -1.25, 1.125, 0.0625]
	encoded = []
	
	# Define a Q formatted number
	# The first parameter is "m" and the second is "n"
	q = Q(1, 4)
	
	# Encode all of the test cases and print them out in a pretty format
	print "encoding.."
	for case in cases:
		# Add the encoded number to the list of cases to decode
		# Use the standard q.encode(...) function to generate the Q numbers
		encoded.append(q.encode(case))
		
		# Make the Q formatted number in a human-readable format
		print '{0} -> {1}'.format(case, q.get_pretty_q_format(encoded[-1]))
	
	# Decode all of the test cases
	print "\ndecoding.."
	for item in encoded:
		# Use the standard q.decode(...) function to convert the Q number back
		# to a scalar.
		print '{0} -> {1}'.format(item, q.decode(item))
	
	print '\nmath opertaions...'
	
	# Add a couple numbers together
	q_add = q.add(encoded[0], encoded[2])
	print '{0} + {1} = {2} = {3}'.format(encoded[0], encoded[2],
		q.get_pretty_q_format(q_add), q.decode(q_add))
	
	# Multiply a couple numbers together
	q_mult = q.mult(encoded[0], encoded[2])
	print '{0} * {1} = {2} = {3}'.format(encoded[0], encoded[2],
		q.get_pretty_q_format(q_mult), q.decode(q_mult))

def test_cases2():
	q0 = Q(1, 4, -0.6875)
	q1 = Q(1, 4, 1.125)
	
	print q0 + q1
	print q0 * q1

def test_net(m=1, n=11, learning_rate=0.001, iters=100):
	from random import uniform
	
	o_err = 0; w_err = 0; scale = 1 / 7.
	for _ in xrange(iters):
		x_raw = [uniform(-1, 1) for _ in xrange(49)]
		w_raw = [uniform(-1, 1) for _ in xrange(49)]
		
		x  = [Q(m, n, xi) for xi in x_raw]
		w  = [Q(m, n, wi) for wi in w_raw]
		o  = Q(m, n, 0)
		lr = Q(m, n, learning_rate)
		s  = Q(m, n, scale)
		i = 0
		for xi, wi in zip(x, w):
			o    += ((wi - xi) * s) ** 2
			w[i] += lr * (xi - wi)
			i    += 1
		
		o_raw  = 0
		i      = 0
		for xi, wi in zip(x_raw, w_raw):
			o_raw    += ((wi - xi) * scale) ** 2
			w_raw[i] += learning_rate * (xi - wi)
			i        += 1
		
		pct_error = abs(o.decode(str(o)) - o_raw) / abs(o_raw) * 100
		if pct_error > o_err:
			o_err  = pct_error
			o_vals = (o.decode(str(o)), o_raw)
		
		for wi, wi_raw in zip(w, w_raw):
			pct_error = abs(wi.decode(str(wi)) - wi_raw) / abs(wi_raw) * 100
			if pct_error > w_err:
				w_err  = pct_error
				w_vals = (wi.decode(str(wi)), wi_raw)
		
	print 'm = {0}, n = {1}\nOutput Error: {2:3.2f}%; {3} vs. {4}\nWeight '   \
		'Update Error: {5:3.2f}%; {6} vs. {7}'.format(m, n, o_err, o_vals[0],
		o_vals[1], w_err, w_vals[0], w_vals[1])

if __name__ == '__main__':
	# test_cases()
	# test_cases2()
	test_net(1, 11, 0.001, 100)