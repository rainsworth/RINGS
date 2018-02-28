import numpy as np
import io,json
import pylab as pl
from decimal import Decimal
from fringe_fitters import *

inname='emerlin_data.json'
input_file  = file(inname, "r")
dataset = json.loads(input_file.read().decode("utf-8"), parse_int=Decimal, parse_float=Decimal)

# extract array of timestamps:
times = np.array([d['timestamp'] for d in dataset])
# extract array of unique timestamps:
times = np.unique(times)

time_03=[]
for entry in dataset:

	if entry['antenna1']=='0' and entry['antenna2']=='3' and entry['spw']=='0':

		time_03.append(entry['timestamp'])

		real = np.array(entry['real']).astype(float)
		imag = np.array(entry['imag']).astype(float)
		flag = np.array(entry['flags']).astype(float)

		# calculate the phase 
		phase = np.arctan2(real,imag)
		
		try:
			real_03 = np.vstack((real_03,real))
			imag_03 = np.vstack((imag_03,imag))
			phase_03 = np.vstack((phase_03,phase))
			flags_03 = np.vstack((flags_03,flag))
		except NameError:
			# this error will be thrown if we've only 
			# read the first entry in the dataset
			real_03 = real
			imag_03 = imag
			phase_03 = phase
			flags_03 = flag


time_03 = np.array(time_03)

spw0 = 4816.500  # MHz
freq0 = np.arange(spw0,spw0+128.,1.)

pl.subplot(111)
pl.imshow(phase_03.T,aspect='auto')
pl.show()

pl.subplot(111)
phase_fav = np.mean(phase_03,axis=1)
real_fav = np.mean(real_03,axis=1)
imag_fav = np.mean(imag_03,axis=1)
pl.plot(time_03,phase_fav)
pl.show()

pl.subplot(111)
phase_tav = np.mean(phase_03,axis=0)
real_tav = np.mean(real_03,axis=0)
imag_tav = np.mean(imag_03,axis=0)
pl.plot(freq0,phase_tav)
pl.show()

# 1D FFT method:
T = FFT_1D(freq0,phase_tav)
print " ------------ "
print "1D FFT"
print "T = ",T

# 1D FFT method:
T = FFT_2D(time_03,freq0,real_03,imag_03)
print " ------------ "
print "2D FFT"
print "T = ",T

# 1D GradPhi method:
T = GradPhi_1D(freq0,phase_tav)
print " ------------ "
print "1D Grad Phi"
print "T = ",T

# 1D LLS method:
T = LLS_1D(freq0,real_tav,imag_tav)
print " ------------ "
print "1D LLS"
print "T = ",T


print peak



