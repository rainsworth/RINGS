import numpy as np
import pylab as pl
from data_handling import *

# read data:
inname='emerlin_data.json'
dataset = read_file(inname)

# extract RR polarization:
dataset = get_data_rr(dataset)

# get data for baseline 03:
ae1 = 0; ae2 = 3
time_03, real_03, imag_03, phase_03, flags_03 = get_baseline_data_allspw(ae1, ae2, dataset)
freq_03 = get_emerlin_freqs('all')

# -----------------------------------------------------------------
# start plotting:

pl.subplot(111)
delta_t = float(np.max(time_03)-np.min(time_03))
extent=[0,delta_t,np.min(freq_03),np.max(freq_03)]
pl.imshow(phase_03.T, origin='lower',extent=extent,aspect='auto')
pl.xlabel("Time [s]")
pl.ylabel("Frequency [MHz]")
pl.colorbar(label='Phase [rads]')
pl.show()

pl.subplot(111)
phase_fav = np.mean(phase_03,axis=1)
real_fav = np.mean(real_03,axis=1)
imag_fav = np.mean(imag_03,axis=1)
pl.plot(time_03,phase_fav)
pl.title("Frequency averaged phase data")
pl.xlabel("Time [s]")
pl.ylabel("Phase [rads]")
pl.show()

pl.subplot(111)
phase_tav = np.mean(phase_03,axis=0)
real_tav = np.mean(real_03,axis=0)
imag_tav = np.mean(imag_03,axis=0)
pl.plot(freq_03,phase_tav)
pl.title("Time averaged phase data")
pl.xlabel("Frequency [MHz]")
pl.ylabel("Phase [rads]")
pl.show()



