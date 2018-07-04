import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys
import getopt
import textwrap
import operator

class h5_plot:

	def __init__(self):
		try:
			opts, args = getopt.getopt(sys.argv[1:], 'i:o:x:y:s:d:f:l:u:t:h', ["inf=", "outf=", "xpar=", "ypar=", "sb=", "det=", "freq=", "low=", "up=", "text=", "help="])
		except getopt.GetoptError:
			usage()

		print ""

		# default values
		self.infile 	= "patch1_573_32.h5"
		self.outfile = "outfile.txt"
		self.x1 		= "time"
		self.y1 		= "tod"
		self.sb 		= "[0]"
		self.det 	= "[0]"
		self.freq 	= "[0]"

		self.y_lim = False
		help = False
		self.lim_count = 0

		for opt, arg in opts:
			if opt in ('-i', '--inf'):
				self.infile 	= arg
			elif opt in ('-o', '--outf'):
				self.outfile = arg
			elif opt in ('-x', '--xpar'):
				self.x1 		= arg
			elif opt in ('-y', '--ypar'):
				self.y1 		= arg
			elif opt in ('-s', '--sb'):
				self.sb 		= arg
			elif opt in ('-d', '--det'):
				self.det 	= arg
			elif opt in ('-f', '--freq'):			
				self.freq 	= arg
			elif opt in ('-l', '--low'):
				self.lim_count += 1
				self.y_min 	= float(arg)
			elif opt in ('-u', '--up'):
				self.lim_count += 1
				self.y_max 	= float(arg)
			elif opt in ('-h', '--help'):
				help 	= True
			else:
				self.usage()
				sys.exit(2)

			if help:
				self.usage()
				exit()

	def usage(self):
		prefix = " "
		preferredWidth = 80
		wrapper = textwrap.TextWrapper(initial_indent=prefix, width=preferredWidth,subsequent_indent=' '*len(prefix))
		m1 = "   (infile name, default patch1_573_32.h5) "
		m2 = "  (outfile name, default none) "
		m3 = "  (x parameter, default time) "
		m4 = "  (y parameter, default tod)"
		m5 = "    (side band number 0-3 as a list (no spacings), default [0]) "
		m6 = "   (detector number 0-19 as a list (no spacings), default [0]) "
		m7 = "  (frequency number 0-33 as a list (no spacings), default [0]) "
		m8 = "   (ymin, default none) "
		m9 = "    (ymax, default none) "
		m10 ="  (legend location, defaul none) "
		m11 ="  (help) "
		print "\nThis is the usage function\n"
		print 'Usage: plot_try1.py -flag '
		print "Flags:"
		print "-i ----> optional --inf", wrapper.fill(m1)
		print "-o ----> optional --outf", wrapper.fill(m2)
		print "-x ----> optional --xpar", wrapper.fill(m3)
		print "-y ----> optional --ypar", wrapper.fill(m4)
		print "-s ----> optional --sb", wrapper.fill(m5)
		print "-d ----> optional --det", wrapper.fill(m6)
		print "-f ----> optional --freq", wrapper.fill(m7)
		print "-l ----> optional --low", wrapper.fill(m8)
		print "-u ----> optional --up", wrapper.fill(m9)
		print "-t ----> optional --text", wrapper.fill(m10)
		print "-h ----> optional --help", wrapper.fill(m11)
		print ""	



	def set_params(self):

		try:
			f = h5py.File(self.infile, "r")
		except IOError:
			print "File not located"
			print "Make sure you have provided the correct location and filename"
			exit()

		group_keys 		= list(f.keys())
		self.detectors 		= [[0, 12, 11, 10, 0], [0, 13, 4, 3, 9], [14, 5, 1, 2, 8], [0, 15, 6, 7, 19], [0, 16, 17, 18, 0]]

		self.det_choices 	= ["all", 1, 2, 4]
		self.freq_choices 	= ["all", 1, 2, 4]
		self.sb_choices		= [1, 2, 4, "all"]

		df = 0.0625
		self.frequencies	= [list(np.linspace(26, 28-df, 32)), list(np.linspace(28, 30-df, 32)), list(np.linspace(30, 32-df, 32)), list(np.linspace(32, 34-df, 32))] #list(f[group_keys[7]])


		if self.lim_count == 1:
			print "Both y-limits needs to be set"
			exit()
		if self.lim_count == 2:
			self.y_lim 		= True

		self.all_det 		= False
		self.all_freq 		= False
		self.all_sb 		= False

		self.det_values 	= range(0, 19)
		self.sb_values 		= range(0, 4)
		self.freq_values 	= range(0, 32)


		#self.sb = eval(self.sb)
		

		if self.freq == "[all]":
			self.all_freq = True
			self.freq = self.frequencies

		else:
			self.freq = eval(self.freq)
			if len(self.freq) in self.freq_choices:
				pass
			else:
				print "Your frequency selection was not valid, make sure you have the correct amount of frequencies (1, 2, 4 or all)" 
				exit()
			for i in range(len(self.freq)):
				if self.freq[i] in self.freq_values[:][:]:
					pass
				else:
					print "Your frequency selection was not valid."
					print "Make sure you provide the correct frequency number (0-32)"
					exit()



		if self.det == "[all]":
			self.all_det = True
			self.det = self.det_values
			if self.freq == "[all]":
				print "For all detectors, only one frequency is possible"
				exit()
			elif len(self.freq) != 1:
				print "For all detectors, only one frequency is possible"
				exit()
			else:
				pass
		else:
			self.det = eval(self.det)
			if len(self.det) in self.freq_choices:
				pass
			else:
				print "Your frequency selection was not valid, make sure you have the correct amount of frequencies (1, 2, 4 or all)" 
				exit()

			for i in range(len(self.det)):
				if self.det[i] in self.det_values:
					pass
				else:
					print "Your detector selection was not valid."
					print "Make sure you provide the correct detector number (0-18)"
					exit()



		if self.sb == "[all]":
			self.all_sb = True
			self.sb = [0, 1, 2, 3]
		else:
			self.sb = eval(self.sb)
			if len(self.sb) in self.sb_choices:
				pass
			else:
				print "Your sb selection was not valid, make sure you have the correct amount of side bands (1, 2, or 4)" 
				exit()
			for i in range(len(self.sb)):
				if self.sb[i] in self.sb_values[:][:]:
					continue
				else:
					print "Your sb selection was not valid."
					print "Make sure you provide the correct sb number (0-3)"
					exit()


		if len(self.freq) != len(self.sb):
			print "You need to specify the same amount of side bands as frequencies"
			print "One side band pr. frequency"
			print "ie. -s [0,0,1,2] -f [0,12,15,29]"
			exit()


		if self.y1 in group_keys:
			index = group_keys.index(self.y1)
			self.y = list(f[group_keys[index]])	
		else:
			print "The y object could not be found." 
			print "Make sure the object name is spelled correctly and exists,"
			exit()

		if self.x1 in group_keys:
			index = group_keys.index(self.x1)
			self.x = list(f[group_keys[index]])	
		else:
			print "The x object could not be found." 
			print "Make sure the object name is spelled correctly and exists,"
			exit()

		if self.x1 == "time":
			if self.y1 != "tod":
				print "The y object is a function of frequency." 
				print "Make sure the object name is spelled correctly and exists,"
				print "For y = tod only nu and time are available x-values"
				exit()	

		if self.x1 == "nu":
			self.x = self.frequencies













	def plot(self):
		if self.x1 == "time":
			legends = []
			if self.all_det:
				print "All detectors does not work now, need more detectors available"
				exit()
				"""
				All detectors does not work now.
				Indices in y are wrong, but want all detectors available to finish up
				"""
				if self.y1 == "tod":
					rows = 5
					cols = 60
					gridspec.GridSpec(rows, cols)
					end_rows = [0, 4]
					for row in range(5):
						for col in range(5):
							index = self.detectors[row][col]
							if index != 0:
								if row in end_rows:
									plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
									plt.plot(self.x, self.y[0][0][index][:], "b")
									if self.y_lim:
										plt.ylim(self.y_min, self.y_max)
									plt.xlabel(self.x1)
									plt.ylabel(self.y1)
									leg = plt.legend(["%i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
									for item in leg.legendHandles:
									    item.set_visible(False)	
									#plt.legend(["(%i)" %(detectors[row][col])], loc="upper right", markerscale=0)
									plt.xticks([])
									plt.yticks([])
								elif row == 2:
									plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
									plt.plot(self.x, self.y[0][0][index][:], "b")	
									if y_lim:
										plt.ylim(self.y_min, self.y_max)
									plt.xlabel(self.x1)
									plt.ylabel(self.y1)
									leg = plt.legend(["%i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
									for item in leg.legendHandles:
									    item.set_visible(False)	
									plt.xticks([])
									plt.yticks([])
								else:
									plt.subplot2grid((rows,cols), (row, col*12-6), colspan=12)
									plt.plot(self.x, self.y[0][0][index][:], "b")	
									if self.y_lim:
										plt.ylim(self.y_min, self.y_max)
									plt.xlabel(self.x1)
									plt.ylabel(self.y1)
									leg = plt.legend(["%i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
									for item in leg.legendHandles:
									    item.set_visible(False)	
									plt.xticks([])
									plt.yticks([])

					plt.tight_layout()
					plt.show()

			elif len(self.det) == 1:
				for j in range(len(self.freq)):
					plt.plot(self.x, self.y[self.det[0]][self.sb[j]][self.freq[j]])
					legends.append("%.2f Hz" % self.freq[j])
					if self.y_lim:
						plt.ylim(self.y_min, self.y_max)
				plt.legend(legends, prop={'size': 12})
				plt.xlim(min(self.x), max(self.x) + (max(self.x)-min(self.x))*0.15)
				plt.xlabel(self.x1)
				plt.ylabel(self.y1)
				plt.title("det %i" % self.det[0])
				plt.show()

			elif len(self.det) == 2:
				for i in range(len(self.det)):
					plt.subplot(1, 2, i+1)
					for j in range(len(self.freq)):
						plt.plot(self.x, self.y[self.det[i]][self.sb[j]][self.freq[j]])
						legends.append("%.2f Hz" % self.freq[j])
						if self.y_lim:
							plt.ylim(self.y_min, self.y_max)
					plt.legend(legends, prop={'size': 12})
					plt.xlabel(self.x1)
					plt.ylabel(self.y1)
					plt.xlim(min(self.x), max(self.x) + (max(self.x)-min(self.x))*0.35)
					plt.title("det %i" % self.det[i])
				plt.show()
			else:
				for i in range(2):
					plt.subplot(2, 2, i+1)
					for j in range(len(self.freq)):
						legends.append("%.2f Hz" % self.freq[j])
						plt.plot(self.x, self.y[self.det[i]][self.sb[j]][self.freq[j]])
						if self.y_lim:
							plt.ylim(self.y_min, self.y_max)
					plt.legend(legends, prop={'size': 8})
					plt.xlim(min(self.x), max(self.x) + (max(self.x)-min(self.x))*0.2)
					plt.xlabel(self.x1)
					plt.ylabel(self.y1)
					plt.title("det %i" % self.det[i])
				
				for j in range(2, 4, 1):
					plt.subplot(2, 2, j+1)
					for k in range(len(self.freq)):
						legends.append("%.2f Hz" % self.freq[j])
						plt.plot(self.x, self.y[self.det[j]][self.sb[k]][self.freq[k]])
						if self.y_lim:
							plt.ylim(self.y_min, self.y_max)
					plt.legend(legends, prop={'size': 8})
					plt.xlim(min(self.x), max(self.x) + (max(self.x)-min(self.x))*0.2)
					plt.xlabel(self.x1)
					plt.ylabel(self.y1)
					plt.title("det %i" % self.det[j])
				plt.show()

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
							y = self.y[0]
							y = list(y[0]) + list(y[1]) + list(y[2]) + list(y[3])

							if row in end_rows:
								plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
								
								plt.plot(self.x, y, "b")
								if self.y_lim:
									plt.ylim(self.y_min, self.y_max)
								leg = plt.legend(["%i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
								for item in leg.legendHandles:
								    item.set_visible(False)	
								#plt.legend(["(%i)" %(detectors[row][col])], loc="upper right", markerscale=0)
								plt.xticks([])
								plt.yticks([])
							elif row == 2:
								plt.subplot2grid((rows,cols), (row, col*12), colspan=12)
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
								plt.plot(self.x, y, "b")	
								if self.y_lim:
									plt.ylim(self.y_min, self.y_max)
								leg = plt.legend(["%i" %(index)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
								for item in leg.legendHandles:
								    item.set_visible(False)	
								plt.xticks([])
								plt.yticks([])

				plt.tight_layout()
				plt.show()
			elif len(self.det) == 1:
				plt.plot(self.x, self.y)
				if self.y_lim:
					plt.ylim(self.y_min, self.y_max)
				plt.xlim(min(self.x), max(self.x) + (max(self.x)-min(self.x))*0.15)
				plt.xlabel(self.x1)
				plt.ylabel(self.y1)
				plt.title("det %i" % self.det[0])
				plt.show()

			elif len(self.det) == 2:
				for i in range(len(self.det)):
					plt.subplot(1, 2, i+1)
					for j in range(len(self.sb)):
						plt.plot(self.x, self.y)
						if self.y_lim:
							plt.ylim(self.y_min, self.y_max)
					plt.xlabel(self.x1)
					plt.ylabel(self.y1)
					plt.legend(["det %i" % self.det[i]])
				plt.show()
			else:
				for i in range(2):
					plt.subplot(2, 2, i+1)
					for j in range(len(self.freq)):
						plt.plot(self.x, self.y)
						if self.y_lim:
							plt.ylim(self.y_min, self.y_max)
					plt.xlabel(self.x1)
					plt.ylabel(self.y1)
					plt.legend(["det %i" % self.det[i]])
				
				for j in range(2, 4, 1):
					plt.subplot(2, 2, j+1)
					for k in range(len(self.freq)):
						plt.plot(self.x, self.y)
						if self.y_lim:
							plt.ylim(self.y_min, self.y_max)
					plt.xlabel(self.x1)
					plt.ylabel(self.y1)
					plt.legend(["det %i" % self.det[i]])
				plt.show()

		"""

		rows = 2
		cols = 2
		gridspec.GridSpec(rows, cols)
		for i in range(19):
			for j in range(2):
				for k in range(2):
					plt.subplot2grid((j, k), (j, k))
					plt.plot(x, y[i][sd[j]][freq[k]][:], "b")	
					leg = plt.legend(["%i" %(i)], handlelength=0, handletextpad=0, fancybox=True, fontsize="small")
					for item in leg.legendHandles:
					    item.set_visible(False)	
					plt.xticks([])
					plt.yticks([])


		"""	
	def main(self):
		self.set_params()
		self.plot()



f = h5_plot()
f.main()