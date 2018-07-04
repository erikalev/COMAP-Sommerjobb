import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys

def plot():

	print "---------------------------------------------------------------------"
	print "Input filename (no quotations signs): "
	infile = str(raw_input())
	print ""
	try:
		f = h5py.File(infile, "r")
	except IOError:
		print "File not located"
		print "Make sure you have provided the correct location and filename"
		exit()

	group_keys 		= list(f.keys())

	print "---------------------------------------------------------------------"
	print "Output filename (no quotations signs): "
	outfile = str(raw_input())
	print ""
	print "---------------------------------------------------------------------"


	det_values = range(1, 20)
	det_choices = ["all", 1, 2, 4]
	detectors = [[0, 12, 11, 10, 0], [0, 13, 4, 3, 9], [14, 5, 1, 2, 8], [0, 15, 6, 7, 19], [0, 16, 17, 18, 0]]
	all_det = False
	#sb = raw_input("Input sb value: ")


	print "Input object on the y-axis. Possible choices are: "
	print "alpha"
	print "fknee"
	print "gain"
	print "sigma0"
	print "tod"
	y1 = str(raw_input())
	if y1 in group_keys:
		index = group_keys.index(y1)
		y = list(f[group_keys[index]])	
	else:
		print "The y object could not be found." 
		print "Make sure the object name is spelled correctly and exists,"
		print "exiting.."

	print "---------------------------------------------------------------------"
	print ""	

	if y1 == "tod":
		print "Possible x-values are: "
		print "nu (frequency)"
		print "time"
		x1 = str(raw_input())
		print "---------------------------------------------------------------------"
		print ""	
		index = group_keys.index(x1)
		x = list(f[group_keys[index]])
	if x1 != "nu": 
			if x1 != "time":
				print "The x object could not be found." 
				print "Make sure the object name is spelled correctly and exists,"
				exit()
	else:	
		index = group_keys.index("nu")
		x = list(f[group_keys[index]])
		print "Frequency selected as x-value"
		print "---------------------------------------------------------------------"
		print ""	



	print "Input the detector number you wish to study. Possible choices are:"
	print "1 detector (select detector number, ie. 1 or 17)"
	print "2 detectors (select detector numbers, ie. 1, 2 or 12, 17)"
	print "4 detectors (select detector numbers, ie. 1, 2, 3, 4 or 5, 7, 12, 17)"
	print "All detectors (write all)"
	det = raw_input("")
	if det == "all":
		all_det = True
		print "All detectors chosen"
	else:
		det = det.split(",")
		for i in range(len(det)):
			try:
				det[i] = int(det[i])
			except ValueError:
				print "The detector choice needs to be given by an integer, try again."
				exit()

			if det[i] in det_values[:][:]:
				continue
			else:
				print det[i]
				print "Your detector selection was not valid."
				print "Make sure you provide the correct detector number (1-19)"
				exit()


	if len(det) in det_choices:
		pass
	elif det == "all":
		pass
	else:
		print "Your detector selection was not valid, make sure you have the correct amount of detectors (1, 2, 4 or all)"
		exit()

	print ""	
	print "---------------------------------------------------------------------"


	freq_values 	= list(np.linspace(26, 34, 4*32+1)) # until frequencies works
	freq_index 		= []
	band_index		= []
	#frequencies	= list(f[group_keys[7]])
	df = 0.0625
	frequencies		= [list(np.linspace(26, 28-df, 32)), list(np.linspace(28, 30-df, 32)), list(np.linspace(30, 32-df, 32)), list(np.linspace(32, 34-df, 32))] #list(f[group_keys[7]])

	
	if x == "time":
		print "Input desired frequency."
		print "The available frequencies are 26 GHz - 34 GHz with 0.0625 GHz step size."
		print "Possible choices are:"
		print "1 frequency (ie. 26.0625)"
		print "2 frequencies (ie. 26.0, 28.875 or 32.1875, 34.0)"
		print "4 frequencies (ie. 26.0, 28.875, 32.1875, 34.0 or 31.375, 31.5, 32.1875, 32.25)"
		print "All frequencies (write all)"
		print ""

		all_freq = False
		freq = raw_input()
		freq_choices = ["all", 1, 2, 4]

		if freq == "all":
			all_freq = True
			print "All frequencies chosen"
		else:
			freq = freq.split(",")
			for i in range(len(freq)):
				try:
					freq[i] = float(freq[i])
				except ValueError:
					print "The frequency choice needs to be given by as a float, try again."
					exit()
				if freq[i] in freq_values:
					if 26.0 <= freq[i] < 28.0:
						band_index.append(0)  
					elif 28.0 <= freq[i] < 30.0:
						band_index.append(1)  
					elif 30.0 <= freq[i] < 32.0:
						band_index.append(2)
					else:
					 	band_index.append(3) 
					freq_index.append(frequencies[band_index[i]].index(freq[i]))
				else:
					print "Your frequency selection was not valid."
					print "Make sure you provide the correct frequency values"
					exit()
			print "Chosen frequencies are:", freq[:]

		if len(freq) in freq_choices:
			pass

		elif freq == "all":
			pass
		else:
			print "Your frequency selection was not valid, make sure you have the correct amount of frequencies (1, 2, 4 or all)" 
			exit()

		print "---------------------------------------------------------------------"
	
	"""
	# Get the data
	self.alpha 				= list(f[self.group_keys[0]])
	self.coord_sys 			= f[self.group_keys[1]].value
	self.decimation_nu 		= f[self.group_keys[2]].value
	self.decimation_time 	= f[self.group_keys[3]].value
	self.fknee 				= list(f[self.group_keys[4]])
	self.flag 				= list(f[self.group_keys[5]])
	self.gain 				= list(f[self.group_keys[6]])
	self.nu 				= list(f[self.group_keys[7]])
	self.pixsize 			= f[self.group_keys[8]].value
	self.point 				= list(f[self.group_keys[9]])
	self.point_cel 			= list(f[self.group_keys[10]])
	self.point_lim 			= list(f[self.group_keys[11]])
	self.point_tel 			= list(f[self.group_keys[12]])
	self.samprate 			= f[self.group_keys[13]].value
	self.scanfreq 			= list(f[self.group_keys[14]])
	self.sigma0 			= list(f[self.group_keys[15]])
	self.stats 				= list(f[self.group_keys[16]])
	self.time 				= list(f[self.group_keys[17]])
	self.time_gain 			= list(f[self.group_keys[18]])
	self.tod 				= list(f[self.group_keys[19]])
	"""


	# large subplot
	if len(det) == 1:
		print ""
		#plt.plot(x, y[])
	elif len(det) == 2:
		print
	elif len(det) == 4:
		print
	else:
		rows = 5
		cols = 60
		gridspec.GridSpec(rows, cols)
		end_rows = [0, 4]
		for row in range(5):
			for col in range(5):
				index = detectors[row][col]
				if index != 0:
					if row in end_rows:
						plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
						plt.plot(x, y[0][0][detectors[row][col]][:], "b")
						leg = plt.legend(["%i" %(detectors[row][col])], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
						for item in leg.legendHandles:
						    item.set_visible(False)	
						#plt.legend(["(%i)" %(detectors[row][col])], loc="upper right", markerscale=0)
						plt.xticks([])
						plt.yticks([])
					elif row == 2:
						plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
						plt.plot(x, y[0][0][detectors[row][col]][:], "b")	
						plt.plot(x, y[0][0][detectors[row][col]][:])
						leg = plt.legend(["%i" %(detectors[row][col])], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
						for item in leg.legendHandles:
						    item.set_visible(False)	
						plt.xticks([])
						plt.yticks([])
					else:
						plt.subplot2grid((rows,cols), (row, col*12-6), colspan=12)
						plt.plot(x, y[0][0][detectors[row][col]][:], "b")	
						plt.plot(x, y[0][0][detectors[row][col]][:])
						leg = plt.legend(["%i" %(detectors[row][col])], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
						for item in leg.legendHandles:
						    item.set_visible(False)	
						plt.xticks([])
						plt.yticks([])
					#plt.subplot2grid((rows,cols), (row, col), colspan=12)
					#plt.plot(x, y[0][0][detectors[row][col]][:])	
				#if row in of_rows:
				#	plt.subplot2grid((rows,cols), (row, col))
				#	plt.plot(x, y[0][0][detectors[row][col]][:])	

		plt.tight_layout()
		plt.show()


	"""
	exit()
	
	fig, axes = plt.subplots(5, 5, sharex = True, sharey = True)#, subplot_kw=dict(projection='aitoff'))
	detectors = [[0, 12, 11, 10, 0], [0, 13, 4, 3, 9], [14, 5, 1, 2, 8], [15, 6, 7, 19, 0], [0, 16, 17, 18, 0]]

	for row in range(5):
		for col in range(5):
			index = detectors[row][col]
			# Plotting all frequencies right now
			if index != 0:
				axes[row, col].plot(x, y[0][0][detectors[row][col]][:])
			else:
				axes[row,col].set_visible(False)
			if row == 0:
				plt.subplots_adjust(left=0.8)
	plt.xlabel("time")
	plt.ylabel("sample")
	plt.show()
	"""
plot()
	
	