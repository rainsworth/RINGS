import numpy as np
import scipy as sp
import pylab as pl
import scipy.fftpack, scipy.optimize

# -------------------------------------------------------------------------

def mock_vis_1D_nondisp(parms,freq):

	phi0, t = parms

	phi = phi0 + 2.*np.pi*freq*1e6*t

	real = np.cos(phi)
	imag = np.sin(phi)

	vis = real+1j*imag

	return vis

# -------------------------------------------------------------------------

def fun_1D_nondisp(parms,x,y):

	model_vis = mock_vis_1D_nondisp(parms,x)

	res = model_vis - y 
	
	return np.abs(res)


# -------------------------------------------------------------------------

def FFT_1D(freq,phase):

	"""
	Performs 1D FFT of 
	frequency dependent visibility
	data to find the tropospheric delay

	Inputs:

	freq - array of frequency values [MHz]
	phase - array of phase values [rad]

	Outputs:

	peak - the location of the maximum in delay space

	"""

	# Number of samplepoints
	N = len(freq)

	# sample spacing
	T = (freq[1] - freq[0])*1e6  # MHz --> Hz

	x = freq*1e6  # MHz --> Hz

	y = np.cos(phase) + 1j*np.sin(phase)

	yf = scipy.fftpack.fftshift(scipy.fftpack.fft(y))
	xf = np.linspace(-1.0/(2.0*T), 1.0/(2.0*T), N)

	fig, ax = pl.subplots()
	ax.plot(xf, 1.0/N * np.abs(yf))
	pl.show()

	return xf[yf.argmax()]



# -------------------------------------------------------------------------

def FFT_2D(time,freq,real,imag):

	"""
	Performs 2D FFT of time and 
	frequency dependent visibility
	data to find the tropospheric delay

	Inputs:

	freq - array of frequency values [MHz]
	phase - array of phase values [rad]

	Outputs:

	peak - the location of the maximum in delay space

	"""

	y = real+1j*imag
	yf = scipy.fftpack.fftshift(scipy.fftpack.fft2(y))

	fig, ax = pl.subplots()
	ax.imshow(np.abs(yf))
	pl.show()

	return 0.0


# -------------------------------------------------------------------------

def GradPhi_1D(freq,phase):

	"""
	Calculates the mean of the 1D
	gradient of the phase with
	respect to frequency

	Inputs:

	freq - array of frequency values [MHz]
	phase - array of phase values [rad]

	Outputs:

	T - the average gradient

	"""

	fdiff = np.ediff1d(freq)*1e6   # MHz --> Hz
	pdiff = np.ediff1d(phase)

	grad = (pdiff/fdiff)/(2.*np.pi)
	T = np.mean(grad)

	# the histogram of the data
	pl.subplot(111)
	n, bins, patches = pl.hist(grad, 50, normed=1, facecolor='green', alpha=0.75)
	pl.show()

	return T


# -------------------------------------------------------------------------

def LLS_1D(freq,real,imag):

	"""
	Calculates a linear least squares fit 
	to the complex visibility as a function of frequency.
	We fit to the visibility rather than the phase to
	avoid wrapping issues.

	Inputs:

	freq - array of frequency values [MHz]
	real - array of real data values 
	imag - array of imag data values

	Outputs:

	T - the tropospheric delay
	"""

	vis = real+1j*imag

	x0 = np.array([0.0,0.0])
	res_lsq = scipy.optimize.least_squares(fun_1D_nondisp, x0, args=(freq, vis))
	print res_lsq

	return res_lsq.x[1]



