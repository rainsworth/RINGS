import numpy as np
import io,json

# ---------------------------------------------------------------------------------------------------

def read_file(inname):

	"""
	This function reads the data from a JSON file

	:param inname: input JSON file name
	:return: dataset as a dict
	"""

	input_file  = file(inname, "r")
	dataset = json.loads(input_file.read().decode("utf-8"))

	return dataset

# ---------------------------------------------------------------------------------------------------

def get_baseline_data(ae1,ae2,spw,dataset):

	"""
	This function extract data for a single baseline from the full dataset

	:param ae1: first antenna in baseline
	:param ae2: second antenna in baseline
	:param spw: spectral window
	:param dataset: full dataset dict
	:return: timestamps, real part of visibility, imaginary part of visibility, phase of visibility, flags
	"""

	time_ab=[]
	for entry in dataset:

		if entry['antenna1']==str(ae1) and entry['antenna2']==str(ae2) and entry['spw']==str(spw):

			time_ab.append(entry['timestamp'])

			real = np.array(entry['real']).astype(float)
			imag = np.array(entry['imag']).astype(float)
			flag = np.array(entry['flags']).astype(float)

			# calculate the phase 
			phase = np.arctan2(imag,real)
			
			try:
				real_ab = np.vstack((real_ab,real))
				imag_ab = np.vstack((imag_ab,imag))
				phase_ab = np.vstack((phase_ab,phase))
				flags_ab = np.vstack((flags_ab,flag))
			except NameError:
				# this error will be thrown if we've only 
				# read the first entry in the dataset
				real_ab = real
				imag_ab = imag
				phase_ab = phase
				flags_ab = flag


	time_ab = np.array(time_ab)

	return time_ab,real_ab,imag_ab,phase_ab,flags_ab


# ---------------------------------------------------------------------------------------------------

def get_baseline_data_allspw(ae1, ae2, dataset):

	"""
	This function extract data for a single baseline from the full dataset
	for all spectral windows

	:param ae1: first antenna in baseline
	:param ae2: second antenna in baseline
	:param dataset: full dataset dict
	:return: timestamps, real part of visibility, imaginary part of visibility, phase of visibility, flags
	"""

	for spw in range(0, 4):
		time, real, imag, phase, flags = get_baseline_data(ae1, ae2, spw, dataset)

		if spw==0:
			time_ab = time
			real_ab = real
			imag_ab = imag
			phase_ab = phase
			flags_ab = flags
		else:
			real_ab = np.hstack((real_ab, real))
			imag_ab = np.hstack((imag_ab, imag))
			phase_ab = np.hstack((phase_ab, phase))
			flags_ab = np.hstack((flags_ab, flags))


	return time_ab, real_ab, imag_ab, phase_ab, flags_ab



# ---------------------------------------------------------------------------------------------------

def get_emerlin_freqs(spw):

	"""
	Function to return frequency axis information for emerlin
	for a specific spectral window

	:param spw: spectral window
	:return: frequency array
	"""

	if (spw==0):
		spw0 = 4816.500  # MHz
		freqs = np.arange(spw0, spw0 + 128., 1.)
	elif (spw==1):
		spw0 = 4944.500  # MHz
		freqs = np.arange(spw0, spw0 + 128., 1.)
	elif (spw==2):
		spw0 = 5072.500  # MHz
		freqs = np.arange(spw0, spw0 + 128., 1.)
	elif (spw==3):
		spw0 = 5200.500  # MHz
		freqs = np.arange(spw0, spw0 + 128., 1.)
	elif (spw=='all'):
		spw0 = 4816.500  # MHz
		freqs = np.arange(spw0, spw0 + 512., 1.)

	return freqs


# ---------------------------------------------------------------------------------------------------

def get_sim1_freqs(spw):

	"""
	Function to return frequency axis information for simulated data
	for a specific spectral window

	:param spw: spectral window
	:return: frequency array
	"""

	if (spw==0):
		spw0 = 43000.000  # MHz
		freqs = np.arange(spw0, spw0 + 2000., 31.250)
	else:
		print "That SPW doesn't exist - I'm giving you spw='0' instead"
		spw0 = 43000.000  # MHz
		freqs = np.arange(spw0, spw0 + 2000., 31.250)

	return freqs


# ---------------------------------------------------------------------------------------------------

def get_data_rr(dataset):

	"""
	Function to compress full dataset with cross-polarizations listed
	separately into a single polarization dataset

	:param dataset: full dataset
	:return: compressed dataset
	"""

	data_rr = [entry for entry in dataset if entry['polarization']=='0']

	return data_rr


# ---------------------------------------------------------------------------------------------------

def get_data_ll(dataset):

	"""
	Function to compress full dataset with cross-polarizations listed
	separately into a single polarization dataset

	:param dataset: full dataset
	:return: compressed dataset
	"""

	data_ll = [entry for entry in dataset if entry['polarization']=='3']

	return data_ll
