import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys
import getopt
import textwrap
import operator
import FileDialog
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_pdf import PdfPages

"""
TO DO:
Fix so that detectors that does not exist shows blank even if non-all plots and histograms 
"""



class h5_plot:

	def __init__(self):
		try: 
			self.infile = sys.argv[1]
		except IndexError:
			print "Infile location needed"
			sys.exit()

		opts = []
		try:
			opts, args = getopt.getopt(sys.argv[2:], 'o:x:y:s:d:n:l:u:x:h:t:f:p:b:', ["outf=", "xpar=", "ypar=", "sb=", "det=", "nu=", "low=", "up=", "text=", "help=", "time=", "freq=", "plot", "bins="])
		except getopt.GetoptError:
			self.usage()

		print ""

		# default values
		self.outfile 	= "outfile.txt"
		self.x1 		= "time"
		self.y1 		= "tod"
		self.sb1 		= "[1]"
		self.det1 		= "[all]"
		self.freq1 		= "[16]"
		self.time1 		= "[1]"
		self.plot 		= "graph"
		self.bins 		= "fd"

		self.y_lim 		= False
		help 			= False
		self.save_plot 	= False
		self.lim_count 	= 0
		self.avg 		= False
		self.png 		= False
		self.pdf 		= False
		self.set_x1		= False
		self.set_y1		= False
		self.set_sb1	= False
		self.set_freq1	= False
		self.set_det1	= False
		self.set_time1	= False


		for opt, arg in opts:
			if opt in ('-o', '--outf'):
				self.save_plot 	= True
				self.outfile = arg
				if self.outfile[-3:] == "png":
					self.png 	= True
				elif self.outfile[-3:] == "pdf":
					self.pdf 	= True
				else:
					print "Outfile name needs to end with .png or .pdf."
					sys.exit()

			elif opt in ('-x', '--xpar'):
				self.x1 		= arg
				self.set_x1		= True
			elif opt in ('-y', '--ypar'):
				self.y1 		= arg
				self.set_y1		= True
			elif opt in ('-s', '--sb'):
				self.sb1 		= arg
				self.set_sb1	= True
			elif opt in ('-d', '--det'):
				self.det1 		= arg
				self.set_det1	= True
			elif opt in ('-n', '--nu'):			
				self.freq1 		= arg
				self.set_freq1	= True
			elif opt in ('-f', '--freq'):			
				self.avg = True
				self.avg_freq1 = arg
			elif opt in ('-l', '--low'):
				self.lim_count += 1
				self.y_min 	= float(arg)
			elif opt in ('-u', '--up'):
				self.lim_count += 1
				self.y_max 	= float(arg)
			elif opt in ('-p', '--plot'):
				self.plot 	= arg
			elif opt in ('-b', '--bins'):
				self.bins 	= arg
			elif opt in ('-t', '--time'):
				if self.y1 != "tod":
					print "Only tod has time dependence, please select an other y-variable or remove the time values."
					sys.exit()
				else:
					self.time1 		= arg				
					self.set_time1	= True

			elif opt in ('-h', '--help'):
				help 	= True
			else:
				self.usage()

			if help:
				self.usage()

	def usage(self):
		prefix = " "
		preferredWidth = 80
		wrapper = textwrap.TextWrapper(initial_indent=prefix, width=preferredWidth,subsequent_indent=' '*len(prefix))
		m2 = "  (outfile name, either .png or .dpf. Default none) "
		m3 = "  (x parameter, default time) "
		m4 = "  (y parameter, default tod)"
		m5 = "    (side band number 0-3 as a list (no spacings), default [1]) "
		m6 = "   (detector number 0-19 as a list (no spacings), default [0]) "
		m7 = "    (frequency number 0-33 as a list (no spacings), default [16]) "
		m8 = "   (ymin, default none) "
		m9 = "    (ymax, default none) "
		m10= "  (graph or hist, default graph"
		m11 ="  (help) "
		m12 ="  (time) " 
		m13 ="  (low/high frequencies to find avg frequency, default [0,0]) " 
		m14 ="  (bin-type from numpy.histogram, default fd) " 
		print "\nThis is the usage function\n"
		print 'Usage: plot_try1.py -flag '
		print "Flags:"
		print "-o ----> optional --outf", wrapper.fill(m2)
		print "-x ----> optional --xpar", wrapper.fill(m3)
		print "-y ----> optional --ypar", wrapper.fill(m4)
		print "-s ----> optional --sb", wrapper.fill(m5)
		print "-d ----> optional --det", wrapper.fill(m6)
		print "-n ----> optional --nu", wrapper.fill(m7)
		print "-f ----> optional --freq", wrapper.fill(m13)
		print "-t ----> optional --time", wrapper.fill(m12)
		print "-l ----> optional --low", wrapper.fill(m8)
		print "-u ----> optional --up", wrapper.fill(m9)
		print "-b ----> optional --bins", wrapper.fill(m14)
		print "-p ----> optional --plot", wrapper.fill(m10)
		print "-h ----> optional --help", wrapper.fill(m11)
		print ""	
		sys.exit()


	def set_params(self):
		try:
			f = h5py.File(self.infile, "r")
		except IOError:
			print "File not located"
			print "Make sure you have provided the correct location and filename"
			sys.exit()

		group_keys 		= list(f.keys())

		###### THIS ONE TAKES TIME ######
		self.times 			= list(f[group_keys[group_keys.index("time")]])

		self.detectors 		= [[0, 12, 11, 10, 0], [0, 13, 4, 3, 9], [14, 5, 1, 2, 8], [0, 15, 6, 7, 19], [0, 16, 17, 18, 0]]
		self.freq_flags 	= [[16], "[all]"]
		self.det_choices 	= [1, 2, 4, "all"]
		self.freq_choices 	= [1, 2, 4, "all"]
		self.plot_choices 	= ["graph", "hist"]
		self.sb_choices		= [1, 2, 4, "all"]
		self.time_choices 	= [1, 2, 4, "all"]
		self.det_list		= [1, 12]
		df = 0.0625
		self.frequencies	= [list(np.linspace(26, 28-df, 32)), list(np.linspace(28, 30-df, 32)), list(np.linspace(30, 32-df, 32)), list(np.linspace(32, 34-df, 32))] #list(f[group_keys[7]])


		if self.plot in self.plot_choices:
			pass
		else:
			print "The only plot choices are 'graph' or 'hist'."
			print "Make sure your plot choice exists and is spelled correctly"
			sys.exit()

		if self.lim_count == 1:
			print "Both y-limits needs to be set"
			sys.exit()
		if self.lim_count == 2:
			self.y_lim 		= True

		self.all_det 		= False
		self.all_freq 		= False
		self.all_sb 		= False
		self.all_times 		= False
		self.det_values 	= range(0, 19)
		self.time_values	= range(0, 61392)
		
		self.sb_values 		= range(0, 4)
		self.freq_values 	= range(0, 32)


		index = group_keys.index("gain")

		if self.time1 == "[all]":
			self.all_times = True
			self.time = self.time_values

		else:
			try:
				self.time = eval(self.time1)
			except SyntaxError:
				print "SyntaxError"
				print "Make sure the input is a list without spacings; ie. [28,2000]"
				sys,exit() 

			if len(self.time) in self.time_choices:
				pass
			else:
				print "Your time selection was not valid, make sure you have the correct amount of times (1, 2, 4 or all)" 
				sys.exit()
			for i in range(len(self.time)):
				if 1 <= self.time[i] <= 61392:
					pass
				else:
					print "Your time selection was not valid."
					print "Make sure you provide the correct time number (1-61392)"
					sys.exit()


		if self.avg:
			try:
				self.avg_freq = eval(self.avg_freq1)
			except SyntaxError:
				print "SyntaxError"
				print "Make sure the input is a list without spacings; ie. [28,2000]"
				sys,exit() 


			if self.avg_freq[0] < self.frequencies[0][0]:
				print "The low frequency is too low."
				print "Please select frequencies inside the range (26-34 Hz)"
				sys.exit()

			if self.avg_freq[1] > (self.frequencies[-1][-1] + df):
				print "The high frequency is too high."
				print "Please select frequencies inside the range (26-34 Hz)"
				sys.exit()

			self.avg_freq = np.average(self.avg_freq)
			
			freq_dist 		= 1e10
			closest_freq	= 1e10
			closest_band	= 1e10

			for i in range(len(self.frequencies)):
				for j in range(len(self.frequencies[i])):			
					if abs(self.avg_freq - self.frequencies[i][j]) < freq_dist:
						freq_dist 		= abs(self.avg_freq - self.frequencies[i][j])
						closest_band	= i
						closest_freq 	= j

			self.sb 	= str([closest_band])
			self.freq 	= str([closest_freq])
			print "Average frequency chosen: %.3f" % self.frequencies[closest_band][closest_freq]


		if self.freq1 == "[all]":
			self.all_freq = True
			self.freq = self.freq_values

		else:
			try:
				self.freq = eval(self.freq1)
			except SyntaxError:
				print "SyntaxError"
				print "Make sure the input is alist without spacings; ie. [28,2000]"
				sys,exit() 

			if len(self.freq) in self.freq_choices:
				pass
			else:
				print "Your frequency selection was not valid, make sure you have the correct amount of frequencies (1, 2, 4 or all)" 
				sys.exit()
			for i in range(len(self.freq)):
				if self.freq[i] in self.freq_values[:][:]:
					pass
				else:
					print "Your frequency selection was not valid."
					print "Make sure you provide the correct frequency number (1-32)"
					sys.exit()


		if self.det1 == "[all]":
			self.all_det = True
			self.det = self.det_values
			if self.set_x1:
				if self.x1 == "time":
					if self.set_time1:
						print "No time slots available when plotting over time"
						sys.exit()
					elif self.set_freq1:									
						if self.freq1 == "[all]":
							print "For all detectors over all times, only one frequency is possible"
							sys.exit()
						elif len(self.freq) != 1:
							print "For all detectors over all times, only one frequency is possible"
							sys.exit()
						else:
							pass

					elif self.set_sb1:									
						if self.sb1 == "[all]":
							print "For all detectors over all times, only one side band is possible"
							sys.exit()
						elif len(self.sb) != 1:
							print "For all detectors over all times, only one side band is possible"
							sys.exit()
						else:
							pass
					else:
						pass

				elif self.x1 == "nu":
					if self.set_freq1:
						print "No time slots available when plotting over time"
						sys.exit()
					elif self.set_time1:									
						if self.time1 == "[all]":
							print "For all detectors over all frequencies, only one time slot is possible"
							sys.exit()
						elif len(self.time) != 1:
							print "For all detectors over all frequencies, only one time slot is possible"
							sys.exit()
						else:
							pass
				else:
					pass
		else:
			# comment in when all det's are available
			try:
				self.det = eval(self.det1)
				for i in range(len(self.det)):
					self.det[i] -= 1
			except SyntaxError:
				print "SyntaxError"
				print "Make sure the input is alist without spacings; ie. [28,2000]"
				sys,exit() 

			if len(self.det) in self.freq_choices:
				pass
			else:
				print "Your frequency selection was not valid, make sure you have the correct amount of frequencies (1, 2, 4 or all)" 
				sys.exit()

			for i in range(len(self.det)):
				if self.det[i] in self.det_values:
					pass
				else:
					print "Your detector selection was not valid."
					print "Make sure you provide the correct detector number (1-19)"
					sys.exit()



		if self.sb1 == "[all]":
			self.all_sb = True
			self.sb = [0, 1, 2, 3]
		else:
			try:
				self.sb = eval(self.sb1)
			except SyntaxError:
				print "SyntaxError"
				print "Make sure the input is alist without spacings; ie. [28,2000]"
				sys,exit() 

			if len(self.sb) in self.sb_choices:
				pass
			else:
				print "Your sb selection was not valid, make sure you have the correct amount of side bands (1, 2, or 4)" 
				sys.exit()
			for i in range(len(self.sb)):
				if self.sb[i] in self.sb_values[:][:]:
					continue
				else:
					print "Your sb selection was not valid."
					print "Make sure you provide the correct sb number (1-4)"
					sys.exit()

		if ((self.set_freq1) or (self.set_sb1)):
			if self.freq1 == "[all]":
				if self.sb1 != "[all]":
					print "You need to specify the same amount of side bands as frequencies"
					print "One side band pr. frequency"
					print "ie. -s [1,1,1,2] -f [1,12,15,29]"
					sys.exit()

			elif self.sb1 == "[all]":
				if self.freq1 != "[all]":
					print "You need to specify the same amount of side bands as frequencies"
					print "One side band pr. frequency"
					print "ie. -s [1,1,1,2] -f [1,12,15,29]"
					sys.exit()

			elif len(self.freq) != len(self.sb):
				print "You need to specify the same amount of side bands as frequencies"
				print "One side band pr. frequency"
				print "ie. -s [1,1,1,2] -f [1,12,15,29]"
				sys.exit()

			else:
				pass

		if self.y1 in group_keys:
			index = group_keys.index(self.y1)
			self.y = list(f[group_keys[index]])	
			if self.y1 == "tod":
				index = group_keys.index("gain")
				self.gain = list(f[group_keys[index]])

				self.y=list(np.asarray(self.y)/np.asarray(self.gain))
			else:
				pass

		else:
			print "The y object could not be found." 
			print "Make sure the object name is spelled correctly and exists,"
			sys.exit()

		if self.x1 in group_keys:
			index = group_keys.index(self.x1)
			self.x = list(f[group_keys[index]])	
		else:
			print "The x object could not be found." 
			print "Make sure the object name is spelled correctly and exists,"
			sys.exit()

		if self.x1 == "time":
			if self.y1 != "tod":
				print "The y object is a function of frequency." 
				print "Make sure the object name is spelled correctly and exists,"
				print "For y = tod only nu and time are available x-values"
				sys.exit()	
				#elif self.freq1 == "[all]":
				#	print 


		if self.x1 == "nu":
			self.x = self.frequencies
			if self.freq in self.freq_flags:
				pass
			else:
				print "All frequencies are automatically selected when plotting with frequencies on x-axis."
				print "Plot over time for different frequencies instead."
				sys.exit()

		self.set_sb1	= False
		self.set_freq1	= False
		self.set_det1	= False
		self.set_time1	= False

		if self.plot == "hist":
			if ((len(self.freq )!= 1) or (len(self.time) != 1)):
				print "When plotting histogram only 1 histogram per plot is available."
				print "Make sure you have not requested several time slots or frequencies"
				sys.exit()
			else:
				pass

	def plot_graph(self):
		if self.y1 == "tod":
			legends = []
			if self.x1 == "time":
				self.x -= self.x[0]	# time since start
				self.x *= 24*60*60 	# time in seconds
				if self.all_det:
					rows = 5
					cols = 60
					gridspec.GridSpec(rows, cols)
					end_rows = [0, 4]
					
					for row in range(5):
						for col in range(5):
							index = self.detectors[row][col]
							if index != 0:
								if row in end_rows:
									if index in self.det_list:

										# change when more detectors are available

										if index == 12:
											index = 2
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.plot(self.x, self.y[index-1][self.sb[0]][self.freq[0]][:], "b")
										if self.y_lim:
											plt.ylim(self.y_min, self.y_max)
										# change 12 to index when more detectors are available
										leg = plt.legend(["det %i" %(12)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
										for item in leg.legendHandles:
										    item.set_visible(False)	
										#plt.legend(["(%i)" %(detectors[row][col])], loc="upper right", markerscale=0)
										plt.xticks([])
										plt.yticks([])

									elif index == 17:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.yticks([]) 
									else:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.xticks([])
										plt.yticks([])

								elif row == 2:
									if index in self.det_list:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.plot(self.x, self.y[index-1][self.sb[0]][self.freq[0]][:], "b")	
										if self.y_lim:
											plt.ylim(self.y_min, self.y_max)
										leg = plt.legend(["det %i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
										for item in leg.legendHandles:
										    item.set_visible(False)	
										plt.xticks([])
										plt.yticks([])
									elif index == 14:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.xticks([])
										
																			
									else:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.xticks([])
										plt.yticks([])
								else:
									if index in self.det_list:
										plt.subplot2grid((rows,cols), (row, col*12-6), colspan=12)
										plt.plot(self.x, self.y[index-1][self.sb[0]][self.freq[0]][:], "b")	
										if self.y_lim:
											plt.ylim(self.y_min, self.y_max)
										leg = plt.legend(["det %i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
										for item in leg.legendHandles:
										    item.set_visible(False)	
										plt.xticks([])
										plt.yticks([])
									else:
										plt.subplot2grid((rows,cols), (row, col*12-6), colspan=12)
										plt.xticks([])
										plt.yticks([])
					
					plt.text(-0.45, 6., 'tod', ha='center', va='center', fontsize=20)
					plt.text(-0.45, -0.3, '--------------------------Time [s from first data]-------------------------->', ha='center', va='center', fontsize=16)
					plt.text(-3.50, 3., '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', rotation='vertical', fontsize=16)
					plt.subplots_adjust(wspace= 1) 

				elif len(self.det) == 1:
					fig, ax = plt.subplots(1, 1)
					for k in range(len(self.freq)):
						if len(self.freq) > 1:
							ax.set_title("det %i" % (self.det[0] + 1))
							legends.append("%.2f [Hz]" % self.frequencies[self.sb[k]][self.freq[k]])
						else:
							ax.set_title("det %i, freq %.2f [Hz]"% ((self.det[0]+1), self.frequencies[self.sb[k]][self.freq[k]]))
						ax.grid()
						ax.plot(self.x, self.y[self.det[0]][self.sb[k]][self.freq[k]])
					if len(self.freq) > 1:
						plt.legend(legends, loc=2, bbox_to_anchor=(1.0, 0.55), fancybox=True, shadow=True, fontsize=12)

					fig.text(0.5, 0.95, 'tod', ha='center', va='center', fontsize=20)
					fig.text(0.5, 0.03, '--------------------------Time [s from first data]-------------------------->', ha='center', va='center', fontsize=16)
					fig.text(0.06, 0.5, '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', rotation='vertical', fontsize=16)
					
				elif len(self.det) == 2:
					fig, ax = plt.subplots(2, 1)
					for i in range(2):
						for k in range(len(self.freq)):
							if len(self.freq) > 1:
								ax[i].set_title("det %i" % (self.det[i]+1))
								legends.append("%.2f [Hz]" % self.frequencies[self.sb[k]][self.freq[k]])
							else:
								ax[i].set_title("det %i, freq %.2f [Hz]"% ((self.det[i]+1), self.frequencies[self.sb[k]][self.freq[k]]))
							ax[i].grid()
							ax[i].plot(self.x, self.y[self.det[i]-1][self.sb[k]][self.freq[k]])

					if len(self.freq) > 1:
						plt.legend(legends, loc=2, bbox_to_anchor=(1.0, 1.2), fancybox=True, shadow=True, fontsize=12)

					fig.text(0.5, 0.95, 'tod', ha='center', va='center', fontsize=20)
					fig.text(0.5, 0.03, '--------------------------Time [s from first data]-------------------------->', ha='center', va='center', fontsize=16)
					fig.text(0.06, 0.5, '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', rotation='vertical', fontsize=16)

				else:
					fig, ax = plt.subplots(2, 2)
					count = 0
					for i in range(2):
						for j in range(2):
							for k in range(len(self.freq)):
								if len(self.freq) > 1:
									ax[i, j].set_title("det %i" % (self.det[count]+1))
									legends.append("%.2f Hz" % self.frequencies[self.sb[k]][self.freq[k]])
								else:
									ax[i, j].set_title("det %i, freq %.2f Hz"% ((self.det[count]+1), self.frequencies[self.sb[k]][self.freq[k]]))
								ax[i, j].grid()
								ax[i, j].plot(self.x, self.y[self.det[count]][self.sb[k]][self.freq[k]])
							count += 1
					if len(self.freq) > 1:
						plt.legend(legends, loc=2, bbox_to_anchor=(1.0, 1.2), fancybox=True, shadow=True, fontsize=12)

					fig.text(0.5, 0.95, 'tod', ha='center', va='center', fontsize=20)
					fig.text(0.5, 0.03, '--------------------------Time [s from first data]-------------------------->', ha='center', va='center', fontsize=16)
					fig.text(0.06, 0.5, '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', rotation='vertical', fontsize=16)
	

			#freq
			else:

				self.x = sum(self.x, [])
				if self.all_det:
					rows = 5
					cols = 60
					gridspec.GridSpec(rows, cols)
					end_rows = [0, 4]
					for row in range(5):
						for col in range(5):
							index = self.detectors[row][col]
							if index != 0:
								if row in end_rows:
									if index in self.det_list:
										if index == 12:
											index = 2

										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)	
										y = self.y[index-1]

										y = list(y[0][:, self.time[0]]) + list(y[1][:, self.time[0]]) + list(y[2][:, self.time[0]]) + list(y[3][:, self.time[0]])
										plt.plot(self.x, y, "b")

										if self.y_lim:
											plt.ylim(self.y_min, self.y_max)
										leg = plt.legend(["det %i" %(12)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
										for item in leg.legendHandles:
										    item.set_visible(False)	
										#plt.legend(["(%i)" %(detectors[row][col])], loc="upper right", markerscale=0)
										plt.xticks([])
										plt.yticks([])

									elif index == 17:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.yticks([]) 

									else:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.xticks([])
										plt.yticks([])
								elif row == 2:
									if index in self.det_list:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										y = self.y[index-1]
										y = list(y[0][:,self.time[0]]) + list(y[1][:,self.time[0]]) + list(y[2][:,self.time[0]]) + list(y[3][:,self.time[0]])
										plt.plot(self.x, y, "b")
										if self.y_lim:
											plt.ylim(self.y_min, self.y_max)
										leg = plt.legend(["det %i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
										for item in leg.legendHandles:
										    item.set_visible(False)	
										plt.xticks([])
										plt.yticks([])
									elif index == 14:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.xticks([])
										
									else:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.xticks([])
										plt.yticks([])
								else:
									if index in self.det_list:
										plt.subplot2grid((rows,cols), (row, col*12-6), colspan=12)
										y = self.y[index-1]
										y = list(y[0][:,self.time[0]]) + list(y[1][:,self.time[0]]) + list(y[2][:,self.time[0]]) + list(y[3][:,self.time[0]])
										plt.plot(self.x, y, "b")
										if self.y_lim:
											plt.ylim(self.y_min, self.y_max)
										leg = plt.legend(["det %i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
										for item in leg.legendHandles:
										    item.set_visible(False)	
										plt.xticks([])
										plt.yticks([])
									else:
										plt.subplot2grid((rows,cols), (row, col*12-6), colspan=12)
										plt.xticks([])
										plt.yticks([])

					plt.text(-0.45, 6., 'tod', ha='center', va='center', fontsize=20)
					plt.text(-0.45, -0.3, '--------------------------Frequency [Hz]-------------------------->', ha='center', va='center', fontsize=16)
					plt.text(-3.50, 3., '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', rotation='vertical', fontsize=16)
					plt.subplots_adjust(wspace= 1) 

				elif len(self.det) == 1:
					fig, ax = plt.subplots(1, 1)
					for k in range(len(self.time)):
						if len(self.time) > 1:
							ax.set_title("det %i" % (self.det[0]+1))
							legends.append("%.2f [s from first data]" % ((self.times[self.time[k]] - self.times[self.time[0]])*24*60*60))
						else:
							ax.set_title("det %i, time %.2f [s from first data]"% ((self.det[0]+1), (self.times[self.time[k]] - self.times[self.time[0]])*24*60*60))
						ax.grid()
						y = self.y[self.det[0]]
						y = list(y[0][:, self.time[k]]) + list(y[1][:, self.time[k]]) + list(y[2][:, self.time[k]]) + list(y[3][:,self.time[k]])
						ax.plot(self.x, y)
					if len(self.time) > 1:
						plt.legend(legends, loc='upper center', bbox_to_anchor=(0.5, -0.02), fancybox=True, shadow=True, ncol=5)
					fig.text(0.5, 0.95, 'tod', ha='center', va='center', fontsize=20)
					fig.text(0.5, 0.015, '--------------------------Frequency [Hz]-------------------------->', ha='center', va='center', fontsize=16)
					fig.text(0.06, 0.5, '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', rotation='vertical', fontsize=16)

				elif len(self.det) == 2:
					fig, ax = plt.subplots(2, 1)
					for i in range(2):
						for k in range(len(self.time)):
							if len(self.time) > 1:
								ax[i].set_title("det %i" % (self.det[i]+1))
								legends.append("%.2f [s from first data]" % ((self.times[self.time[k]] - self.times[self.time[0]])*24*60*60))
							else:
								ax[i].set_title("det %i, time %.2f [s from first data]"% ((self.det[i]+1), (self.times[self.time[k]] - self.times[self.time[0]])*24*60*60))
							ax[i].grid()
							y = self.y[self.det[i]]
							y = list(y[0][:,self.time[k]]) + list(y[1][:,self.time[k]]) + list(y[2][:,self.time[k]]) + list(y[3][:,self.time[k]])
							ax[i].plot(self.x, y)
					if len(self.time) > 1:
						plt.legend(legends, loc='upper center', bbox_to_anchor=(0.5, -0.02), fancybox=True, shadow=True, ncol=5)
					fig.text(0.5, 0.95, 'tod', ha='center', va='center', fontsize=20)
					fig.text(0.5, 0.015, '--------------------------Frequency [Hz]-------------------------->', ha='center', va='center', fontsize=16)
					fig.text(0.06, 0.5, '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', rotation='vertical', fontsize=16)

				else:
					fig, ax = plt.subplots(2, 2)
					count = 0
					for i in range(2):
						for j in range(2):
							for k in range(len(self.time)):
								if len(self.time) > 1:
									ax[i, j].set_title("det %i" % (self.det[count]+1))
									legends.append("%.2f [s from first data]" % ((self.times[int(self.time[k])] - self.times[0])*24*60*60))
								else:
									ax[i, j].set_title("det %i, time %.2f [s from first data]"% ((self.det[count]+1), (self.times[self.time[k]] - self.times[0])*24*60*60))
								ax[i, j].grid()
								y = self.y[self.det[count]]
								y = list(y[0][:,self.time[k]]) + list(y[1][:,self.time[k]]) + list(y[2][:,self.time[k]]) + list(y[3][:,self.time[k]])
								ax[i, j].plot(self.x, y)
							count += 1
					if len(self.time) > 1:
						plt.legend(legends, loc='upper center', bbox_to_anchor=(-0.1, -0.045), fancybox=True, shadow=True, ncol=5)
					fig.text(0.5, 0.95, 'tod', ha='center', va='center', fontsize=20)
					fig.text(0.5, 0.015, '--------------------------Frequency [Hz]-------------------------->', ha='center', va='center', fontsize=16)
					fig.text(0.06, 0.5, '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', rotation='vertical', fontsize=16)

		else:
			self.x = sum(self.x, [])
			if self.all_det:
				rows = 5
				cols = 60
				gridspec.GridSpec(rows, cols)
				end_rows = [0, 4]
				y = self.y
				for row in range(5):
					for col in range(5):
						index = self.detectors[row][col]
						if index != 0:
							if row in end_rows:
								if index in self.det_list:
									if index == 12:
										index = 2
									plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
									y = self.y[index-1]
									y = list(y[0][:]) + list(y[1][:]) + list(y[2][:]) + list(y[3][:])
									plt.plot(self.x, y, "b")
									if self.y_lim:
										plt.ylim(self.y_min, self.y_max)
									leg = plt.legend(["%i" %(12)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
									for item in leg.legendHandles:
									    item.set_visible(False)	
									#plt.legend(["(%i)" %(detectors[row][col])], loc="upper right", markerscale=0)
									plt.xticks([])
									plt.yticks([])
								elif index == 17:
									plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
									plt.yticks([]) 
								else:
									plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
									plt.xticks([])
									plt.yticks([])
							elif row == 2:
								if index in self.det_list:
									plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
									y = self.y[index-1]
									y = list(y[0][:]) + list(y[1][:]) + list(y[2][:]) + list(y[3][:])
									plt.plot(self.x, y, "b")	
									if self.y_lim:
										plt.ylim(self.y_min, self.y_max)
									leg = plt.legend(["%i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
									for item in leg.legendHandles:
									    item.set_visible(False)	
									plt.xticks([])
									plt.yticks([])
								elif index == 14:
									plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
									plt.xticks([])
								else:
									plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
									plt.xticks([])
									plt.yticks([])
							else:
								if index in self.det_list:
									plt.subplot2grid((rows,cols), (row, col*12-6), colspan=12)
									y = self.y[index-1]
									y = list(y[0][:]) + list(y[1][:]) + list(y[2][:]) + list(y[3][:])
									plt.plot(self.x, y, "b")	
									if self.y_lim:
										plt.ylim(self.y_min, self.y_max)
									leg = plt.legend(["%i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
									for item in leg.legendHandles:
									    item.set_visible(False)	
									plt.xticks([])
									plt.yticks([])
								else:
									plt.subplot2grid((rows,cols), (row, col*12-6), colspan=12)
									plt.xticks([])
									plt.yticks([])

				plt.text(-0.45, 6., self.y1, ha='center', va='center', fontsize=20)
				plt.text(-0.45, -0.3, '--------------------------Frequency [Hz]-------------------------->', ha='center', va='center', fontsize=16)
				plt.text(-3.50, 3., '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', rotation='vertical', fontsize=16)
				plt.subplots_adjust(wspace= 1) 



			elif len(self.det) == 1:
				fig, ax = plt.subplots(1, 1)
				ax.set_title("det %i"% (self.det[0]+1))
				ax.grid()
				y = self.y[self.det[0]]
				y = list(y[0]) + list(y[1]) + list(y[2]) + list(y[3])
				ax.plot(self.x, y)
				fig.text(0.51, 0.95, self.y1, ha='center', va='center', fontsize=20)
				fig.text(0.52, 0.03, '--------------------------Frequency [Hz]-------------------------->', ha='center', va='center', fontsize=16)
				fig.text(0.06, 0.5, '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', rotation='vertical', fontsize=16)

			elif len(self.det) == 2:
				fig, ax = plt.subplots(2, 1)
				for i in range(2):
					ax[i].set_title("det %i"% (self.det[i]+1))
					ax[i].grid()
					y = self.y[self.det[i]]
					y = list(y[0]) + list(y[1]) + list(y[2]) + list(y[3])
					ax[i].plot(self.x, y)
				fig.text(0.51, 0.95, self.y1, ha='center', va='center', fontsize=20)
				fig.text(0.52, 0.015, '--------------------------Frequency [Hz]-------------------------->', ha='center', va='center', fontsize=16)
				fig.text(0.06, 0.5, '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', rotation='vertical', fontsize=16)


			else:
				fig, ax = plt.subplots(2, 2)
				count = 0
				for i in range(2):
					for j in range(2):
						ax[i, j].set_title("det %i"% (self.det[count]+1))
						ax[i, j].grid()
						y = self.y[self.det[count]]
						y = list(y[0]) + list(y[1]) + list(y[2]) + list(y[3])
						ax[i, j].plot(self.x, y)
						count += 1
				fig.text(0.51, 0.95, self.y1, ha='center', va='center', fontsize=20)
				fig.text(0.52, 0.015, '--------------------------Frequency [Hz]-------------------------->', ha='center', va='center', fontsize=16)
				fig.text(0.06, 0.5, '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', rotation='vertical', fontsize=16)

		mng = plt.get_current_fig_manager()
		mng.full_screen_toggle()
		if self.save_plot == False:
			plt.show()
		elif self.png:
			fig = plt.gcf()
			fig.set_size_inches((15, 11), forward=False)
			plt.savefig(self.outfile, dpi=500, format="png")
		else:
			fig = plt.gcf()
			fig.set_size_inches((15, 11), forward=False)
			plt.savefig(self.outfile, dpi=500, format="pdf")

	def plot_hist(self):
		if self.y1 == "tod":
			legends = []
			if self.x1 == "time":
				self.x -= self.x[0]	# time since start
				self.x *= 24*60*60 	# time in seconds
				if self.all_det:
					rows = 5
					cols = 60
					gridspec.GridSpec(rows, cols)
					end_rows = [0, 4]
					
					for row in range(5):
						for col in range(5):
							index = self.detectors[row][col]
							if index != 0:
								if row in end_rows:
									if index in self.det_list:

										# change when more detectors are available

										if index == 12:
											index = 2
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.hist(self.y[index-1][self.sb[0]][self.freq[0]][:], bins = "fd")

										# change 12 to index when more detectors are available
										leg = plt.legend(["det %i" %(12)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
										for item in leg.legendHandles:
										    item.set_visible(False)	
										#plt.legend(["(%i)" %(detectors[row][col])], loc="upper right", markerscale=0)
										plt.xticks([])
										plt.yticks([])

									elif index == 17:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.yticks([]) 
									else:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.xticks([])
										plt.yticks([])

								elif row == 2:
									if index in self.det_list:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.hist(self.y[index-1][self.sb[0]][self.freq[0]][:], bins = "fd")	
										if self.y_lim:
											plt.ylim(self.y_min, self.y_max)
										leg = plt.legend(["det %i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
										for item in leg.legendHandles:
										    item.set_visible(False)	
										plt.xticks([])
										plt.yticks([])
									elif index == 14:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.xticks([])
										
																			
									else:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.xticks([])
										plt.yticks([])
								else:
									if index in self.det_list:
										plt.subplot2grid((rows,cols), (row, col*12-6), colspan=12)
										plt.hist(self.y[index-1][self.sb[0]][self.freq[0]][:], bins = "fd")	
										if self.y_lim:
											plt.ylim(self.y_min, self.y_max)
										leg = plt.legend(["det %i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
										for item in leg.legendHandles:
										    item.set_visible(False)	
										plt.xticks([])
										plt.yticks([])
									else:
										plt.subplot2grid((rows,cols), (row, col*12-6), colspan=12)
										plt.xticks([])
										plt.yticks([])
					
					plt.text(-0.45, 6., 'tod', ha='center', va='center', fontsize=20)
					plt.text(-0.45, -0.3, '--------------------------Detector readings [$\\mu K$]-------------------------->', ha='center', va='center', fontsize=16)
					plt.text(-3.50, 3., '--------------------------Count at frequency %.2f-------------------------->' % self.frequencies[self.sb[0]][self.freq[0]], ha='center', va='center', rotation='vertical', fontsize=16)
					plt.subplots_adjust(wspace= 1) 

				elif len(self.det) == 1:
					fig, ax = plt.subplots(1, 1)
					for k in range(len(self.freq)):
						ax.set_title("det %i"% (self.det[0]+1))
						ax.grid()
						ax.hist(self.y[self.det[0]][self.sb[k]][self.freq[k]], bins="fd")
					fig.text(0.5, 0.95, 'tod', ha='center', va='center', fontsize=20)
					fig.text(0.5, 0.03, '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', fontsize=16)
					fig.text(0.06, 0.5, '-----------------Count at frequency %.2f----------------->' % self.frequencies[self.sb[0]][self.freq[0]], ha='center', va='center', rotation='vertical', fontsize=16)
					
				elif len(self.det) == 2:
					fig, ax = plt.subplots(2, 1)
					for i in range(2):
						for k in range(len(self.freq)):
							ax[i].set_title("det %i"% (self.det[i]+1))
							ax[i].grid()
							ax[i].hist(self.y[self.det[i]-1][self.sb[k]][self.freq[k]], bins="fd")
					fig.text(0.5, 0.95, 'tod', ha='center', va='center', fontsize=20)
					fig.text(0.5, 0.03, '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', fontsize=16)
					fig.text(0.06, 0.5, '-----------------Count at frequency %.2f----------------->' % self.frequencies[self.sb[0]][self.freq[0]], ha='center', va='center', rotation='vertical', fontsize=16)

				else:
					fig, ax = plt.subplots(2, 2)
					count = 0
					for i in range(2):
						for j in range(2):
							for k in range(len(self.freq)):
								ax[i, j].set_title("det %i"% (self.det[count]+1))
								ax[i, j].grid()
								ax[i, j].hist(self.y[self.det[count]][self.sb[k]][self.freq[k]], bins="fd")
							count += 1
					fig.text(0.5, 0.95, 'tod', ha='center', va='center', fontsize=20)
					fig.text(0.5, 0.03, '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', fontsize=16)
					fig.text(0.06, 0.5, '-----------------Count at frequency %.2f----------------->' % self.frequencies[self.sb[0]][self.freq[0]], ha='center', va='center', rotation='vertical', fontsize=16)
	

			#freq
			else:

				self.x = sum(self.x, [])
				if self.all_det:
					rows = 5
					cols = 60
					gridspec.GridSpec(rows, cols)
					end_rows = [0, 4]
					for row in range(5):
						for col in range(5):
							index = self.detectors[row][col]
							if index != 0:
								if row in end_rows:
									if index in self.det_list:
										if index == 12:
											index = 2

										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)	
										y = self.y[index-1]
										y = list(y[0][:, self.time[0]]) + list(y[1][:, self.time[0]]) + list(y[2][:, self.time[0]]) + list(y[3][:, self.time[0]])
										plt.hist(y, bins="fd")

										leg = plt.legend(["det %i" %(12)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
										for item in leg.legendHandles:
										    item.set_visible(False)	
										#plt.legend(["(%i)" %(detectors[row][col])], loc="upper right", markerscale=0)
										plt.xticks([])
										plt.yticks([])

									elif index == 17:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.yticks([]) 

									else:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.xticks([])
										plt.yticks([])
								elif row == 2:
									if index in self.det_list:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										y = self.y[index-1]
										y = list(y[0][:,self.time[0]]) + list(y[1][:,self.time[0]]) + list(y[2][:,self.time[0]]) + list(y[3][:,self.time[0]])
										plt.hist(y, bins="fd")
										leg = plt.legend(["det %i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
										for item in leg.legendHandles:
										    item.set_visible(False)	
										plt.xticks([])
										plt.yticks([])
									elif index == 14:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.xticks([])
										
									else:
										plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
										plt.xticks([])
										plt.yticks([])
								else:
									if index in self.det_list:
										plt.subplot2grid((rows,cols), (row, col*12-6), colspan=12)
										y = self.y[index-1]
										y = list(y[0][:,self.time[0]]) + list(y[1][:,self.time[0]]) + list(y[2][:,self.time[0]]) + list(y[3][:,self.time[0]])
										plt.hist(y, bins="fd")
										leg = plt.legend(["det %i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
										for item in leg.legendHandles:
										    item.set_visible(False)	
										plt.xticks([])
										plt.yticks([])
									else:
										plt.subplot2grid((rows,cols), (row, col*12-6), colspan=12)
										plt.xticks([])
										plt.yticks([])

					plt.text(-0.45, 6., 'tod', ha='center', va='center', fontsize=20)
					plt.text(-0.45, -0.3, '--------------------------Detector readings [$\\mu K$]-------------------------->', ha='center', va='center', fontsize=16)
					plt.text(-3.50, 3., '--------------------Count at time %.2f [s after first data]-------------------->' % ((self.times[self.time[0]] - self.times[0])*24*60*60), ha='center', va='center', rotation='vertical', fontsize=16)
					plt.subplots_adjust(wspace= 1) 

				elif len(self.det) == 1:
					fig, ax = plt.subplots(1, 1)
					for k in range(len(self.time)):
						ax.set_title("det %i, time %.2f [s from first data]"% ((self.det[0]+1), (self.times[self.time[k]] - self.times[0])*24*60*60))
						ax.grid()
						y = self.y[self.det[0]]
						y = list(y[0][:, self.time[k]]) + list(y[1][:, self.time[k]]) + list(y[2][:, self.time[k]]) + list(y[3][:,self.time[k]])
						ax.hist(y, bins="fd")
					fig.text(0.5, 0.95, 'tod', ha='center', va='center', fontsize=20)
					fig.text(0.5, 0.03, '--------------------Detector readings [$\\mu K$]-------------------->', ha='center', va='center', fontsize=16)
					fig.text(0.06, 0.5, '----------Count at time %.2f [s after first data]---------->' % ((self.times[self.time[0]] - self.times[0])*24*60*60), ha='center', va='center', rotation='vertical', fontsize=16)

				elif len(self.det) == 2:
					fig, ax = plt.subplots(2, 1)
					for i in range(2):
						for k in range(len(self.time)):
							ax[i].set_title("det %i"% (self.det[i]+1))
							ax[i].grid()
							y = self.y[self.det[i]]
							y = list(y[0][:,self.time[k]]) + list(y[1][:,self.time[k]]) + list(y[2][:,self.time[k]]) + list(y[3][:,self.time[k]])
							ax[i].hist(y, bins="fd")
					fig.text(0.5, 0.95, 'tod', ha='center', va='center', fontsize=20)
					fig.text(0.5, 0.03, '--------------------Detector readings [$\\mu K$]-------------------->', ha='center', va='center', fontsize=16)
					fig.text(0.06, 0.5, '----------Count at time %.2f [s after first data]---------->' % ((self.times[self.time[0]] - self.times[0])*24*60*60), ha='center', va='center', rotation='vertical', fontsize=16)

				else:
					fig, ax = plt.subplots(2, 2)
					count = 0
					for i in range(2):
						for j in range(2):
							for k in range(len(self.time)):
								ax[i, j].set_title("det %i"% (self.det[count]+1))
								ax[i, j].grid()
								y = self.y[self.det[count]]
								y = list(y[0][:,self.time[k]]) + list(y[1][:,self.time[k]]) + list(y[2][:,self.time[k]]) + list(y[3][:,self.time[k]])
								ax[i, j].hist(y, bins="fd")
							count += 1
					fig.text(0.5, 0.95, 'tod', ha='center', va='center', fontsize=20)
					fig.text(0.5, 0.03, '----------Detector readings [$\\mu K$]---------->', ha='center', va='center', fontsize=16)
					fig.text(0.06, 0.5, '----------Count at time %.2f [s after first data]---------->' % ((self.times[self.time[0]] - self.times[0])*24*60*60), ha='center', va='center', rotation='vertical', fontsize=16)

		else:
			self.x = sum(self.x, [])
			if self.all_det:
				rows = 5
				cols = 60
				gridspec.GridSpec(rows, cols)
				end_rows = [0, 4]
				y = self.y
				for row in range(5):
					for col in range(5):
						index = self.detectors[row][col]
						if index != 0:
							if row in end_rows:
								if index in self.det_list:
									if index == 12:
										index = 2
									plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
									y = self.y[index-1]
									y = list(y[0][:]) + list(y[1][:]) + list(y[2][:]) + list(y[3][:])
									plt.hist(y, bins="fd")									
									leg = plt.legend(["%i" %(12)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
									for item in leg.legendHandles:
									    item.set_visible(False)	
									#plt.legend(["(%i)" %(detectors[row][col])], loc="upper right", markerscale=0)
									plt.xticks([])
									plt.yticks([])
								elif index == 17:
									plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
									plt.yticks([]) 
								else:
									plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
									plt.xticks([])
									plt.yticks([])
							elif row == 2:
								if index in self.det_list:
									plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
									y = self.y[index-1]
									y = list(y[0][:]) + list(y[1][:]) + list(y[2][:]) + list(y[3][:])
									plt.hist(y, bins="fd")
									leg = plt.legend(["%i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
									for item in leg.legendHandles:
									    item.set_visible(False)	
									plt.xticks([])
									plt.yticks([])
								elif index == 14:
									plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
									plt.xticks([])
								else:
									plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
									plt.xticks([])
									plt.yticks([])
							else:
								if index in self.det_list:
									plt.subplot2grid((rows,cols), (row, col*12-6), colspan=12)
									y = self.y[index-1]
									y = list(y[0][:]) + list(y[1][:]) + list(y[2][:]) + list(y[3][:])
									plt.hist(y, bins="fd")
									leg = plt.legend(["%i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
									for item in leg.legendHandles:
									    item.set_visible(False)	
									plt.xticks([])
									plt.yticks([])
								else:
									plt.subplot2grid((rows,cols), (row, col*12-6), colspan=12)
									plt.xticks([])
									plt.yticks([])

				plt.text(-0.45, 6., self.y1, ha='center', va='center', fontsize=20)
				plt.text(-0.45, -0.3, '--------------------------Detector readings [$\\mu K$]-------------------------->', ha='center', va='center', fontsize=16)
				plt.text(-3.50, 3., '-------------------------------Count------------------------------->', ha='center', va='center', rotation='vertical', fontsize=16)
				plt.subplots_adjust(wspace= 1) 



			elif len(self.det) == 1:
				fig, ax = plt.subplots(1, 1)
				ax.set_title("det %i"% (self.det[0]+1))
				ax.grid()
				y = self.y[self.det[0]]
				y = list(y[0]) + list(y[1]) + list(y[2]) + list(y[3])
				ax.hist(y, bins="fd")
				fig.text(0.51, 0.95, self.y1, ha='center', va='center', fontsize=20)
				fig.text(0.5, 0.03, '------------------------------Detector readings [$\\mu K$]------------------------------>', ha='center', va='center', fontsize=16)
				fig.text(0.06, 0.5, '------------------------------Count------------------------------>', ha='center', va='center', rotation='vertical', fontsize=16)

			elif len(self.det) == 2:
				fig, ax = plt.subplots(2, 1)
				for i in range(2):
					ax[i].set_title("det %i"% (self.det[i]+1))
					ax[i].grid()
					y = self.y[self.det[i]]
					y = list(y[0]) + list(y[1]) + list(y[2]) + list(y[3])
					ax[i].hist(y, bins="fd")
				fig.text(0.51, 0.95, self.y1, ha='center', va='center', fontsize=20)
				fig.text(0.5, 0.03, '------------------------------Detector readings [$\\mu K$]------------------------------>', ha='center', va='center', fontsize=16)
				fig.text(0.06, 0.5, '------------------------------Count------------------------------>', ha='center', va='center', rotation='vertical', fontsize=16)


			else:
				fig, ax = plt.subplots(2, 2)
				count = 0
				for i in range(2):
					for j in range(2):
						ax[i, j].set_title("det %i"% (self.det[count]+1))
						ax[i, j].grid()
						y = self.y[self.det[count]]
						y = list(y[0]) + list(y[1]) + list(y[2]) + list(y[3])
						ax[i, j].hist(y, bins="fd")
						count += 1
				fig.text(0.51, 0.95, self.y1, ha='center', va='center', fontsize=20)
				fig.text(0.5, 0.03, '------------------------------Detector readings [$\\mu K$]------------------------------>', ha='center', va='center', fontsize=16)
				fig.text(0.06, 0.5, '------------------------------Count------------------------------>', ha='center', va='center', rotation='vertical', fontsize=16)

		mng = plt.get_current_fig_manager()
		mng.full_screen_toggle()
		if self.save_plot == False:
			plt.show()
		elif self.png:
			fig = plt.gcf()
			fig.set_size_inches((15, 11), forward=False)
			plt.savefig(self.outfile, dpi=500, format="png")
		else:
			fig = plt.gcf()
			fig.set_size_inches((15, 11), forward=False)
			plt.savefig(self.outfile, dpi=500, format="pdf")

	def main(self):
		self.set_params()
		if self.plot == "graph":
			self.plot_graph()
		else:
			self.plot_hist()

if __name__ == "__main__":
	f = h5_plot()
	f.main()