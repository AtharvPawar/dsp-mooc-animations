import math
from math import pi

def chebyschev_polynomial(x, N):
	"""
	Evaluates the Nth order Chebyschev polynomial at x and returns the value.
	"""
	if x < 1 and x >= -1:
		return math.cos(N * math.acos(x))
	elif x < -1:
		# TODO
		raise ValueError()
		return None
	else:
		return math.cosh(N * math.acosh(x))

def chebyschev_lowpass(f_pass, f_stop, tol_pass, tol_stop):
	"""
	Returns the Chebyschev analog lowpass filter function corresponding to
	passband and stopband frequencies and tolerances.

	Inputs:
	- f_pass: The passband boundary frequency in Hz
	- f_stop: The stopband boundary frequency in Hz
	- tol_pass: The tolerance required in the passband
	- tol_stop: The tolerance required in the stopband.

	Returns a function that takes a frequency (in Hz) as input and returns
	the filter magnitude at that frequency as the output.
	"""

	if f_pass == f_stop:
		# TODO
		raise ValueError()

	if tol_pass == 0 or tol_stop == 0:
		# TODO
		raise ValueError()

	D1 = 1 / (1 - tol_pass)**2 - 1
	D2 = 1 / tol_stop**2 - 1

	# Optimal epsilon to get minimum N possible
	# epsilon = math.sqrt(D1)
	
	# Minimum order of the filter that is required
	# (Note that D1 is the same as epsilon**2)
	N = math.acosh(D2 / D1) / math.acosh(f_stop / f_pass)
	N = math.ceil(N)

	def filter_func(f):
		# Note that D1 is the same as epsilon**2
		mag2 = 1 / (1 + D1*chebyshev_polynomial(f / f_pass, N))
		return math.sqrt(mag2)

	return filter_func