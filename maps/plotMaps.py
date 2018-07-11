import numpy as np
import h5py
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from matplotlib import animation, rc
from mpl_toolkits.axes_grid1 import make_axes_locatable
plt.switch_backend('agg')

scan_id = sys.argv[1]

#if sys.argv[2] == 'add':
#        add = True
#else:
#        add = False

if sys.argv[2] == 'one':
        sb = int(sys.argv[3])
        freq = int(sys.argv[4])
        lim = int(sys.argv[5])


'''
Contains:

readMap(prefix) # Reads a h5 file with map and hitmap
swap_xy(2darray) # Swaps the axes of the 2darray (y,x) -> (x,y)

makeMap_one(x, y, mapData, hitData, mapname) # Plots one map
makeMap_noise(x, y, mapData, hitData, mapname, limit) # plots one map with noise
makeMap_sb(x, y, A_lsb, A_usb, B_lsb, B_usb, hitData, mapname) # Plots each sideband in a grid
makeMap_gif(x, y, maps, hitData, mapname) # makes a gif of all frequency maps 

setup_one(prefix, sb, freq) # one plot for given sb and freq
setup_add1(prefix) # one plot in total
setup_add4(prefix) # one plot per sb
setup_dif(prefix) # difference between two sb, currently B_lsb and B_usb
setup_gif(prefix) # gif of one plot per freq

'''





def readMap(pre):
        if sys.argv[2] == 'gif':
                filename = pre + '_1024.h5'
        else:
                filename = pre + '_map.h5'
        dfile = h5py.File(filename,'r')
        nx = dfile['n_x']; nx = np.array(nx).astype(int) 
        ny = dfile['n_y']; ny = np.array(ny).astype(int)
        x = dfile['x']; x = np.array(x[:]).astype(float)
        y = dfile['y']; y = np.array(y[:]).astype(float)
        maps = dfile['map'];  maps = np.array(maps[...]).astype(float)
        hit = dfile['nhit']; hit = np.array(hit[...]).astype(float)

        return x, y, maps, hit

def swap_xy(my_array):
        my_array[:, 0], my_array[:, 1] = my_array[:, 1], my_array[:, 0].copy()
        return my_array
   




def makeMap_one(x, y, mapData, hitData, mapname):

        cm.viridis.set_bad('w',1.) #color of masked elements
        mapData = np.ma.masked_where(hitData < 1., mapData)
        #hitData = np.ma.masked_where(hitData < 1., hitData)
 
        x_min = x[1]
        x_max = x[-1] + (x[1]-x[0])
        y_min = y[1]
        y_max = y[-1] + (y[1]-y[0])
        #myax = [x_min, x_max, y_min, y_max]

        # True position of Jupiter
        x_true = 225.197
        y_true = -15.769

        #print np.argwhere(mapData=max(mapData))

        #maxVal = 9.6e4  # max value for color plot
        #minVal = -9.6e4 # min value for color plot

        fig = plt.figure()

        plt.imshow(mapData, extent=(x_min,x_max,y_min,y_max), interpolation='nearest',cmap=plt.cm.viridis,origin='lower')
        #plt.imshow(mapData, interpolation='nearest',cmap=plt.cm.viridis,origin='lower')
        #plt.plot(x_true,y_true,'wo')
        plt.ylabel('Declination [deg]')
        plt.xlabel('Right Ascension [deg]')
        #plt.title('')
        plt.colorbar()

	plt.savefig(mapname)#,bbox_inches='tight')
        plt.close(fig)

def makeMap_noise(x,y, mapData, hitData, mapname, limit):


        cm.viridis.set_bad('w',1.) #color of masked elements
        mapData = np.ma.masked_where(hitData < 1., mapData)
        #hitData = np.ma.masked_where(hitData < 1., hitData)
        
        x_min = x[1]
        x_max = x[-1] + (x[1]-x[0])
        y_min = y[1]
        y_max = y[-1] + (y[1]-y[0])
        #myax = [x_min, x_max, y_min, y_max]

        maxVal = limit  # max value for color plot
        minVal = -limit # min value for color plot

        fig = plt.figure()

        plt.imshow(mapData, extent=(x_min,x_max,y_min,y_max), interpolation='nearest',cmap=plt.cm.viridis,vmin=minVal,vmax=maxVal)
        plt.ylabel('Declination [deg]')
        plt.xlabel('Right Ascension [deg]')
        #plt.title('')
        plt.colorbar()

	plt.savefig(mapname)#,bbox_inches='tight')
        plt.close(fig)



def makeMap_sb(x, y, mapData_0, mapData_1, mapData_2, mapData_3, hitData, mapname):

	cm.viridis.set_bad('w',1.) #color of masked elements
        mapData_0 = np.ma.masked_where(hitData < 1., mapData_0)
        mapData_1 = np.ma.masked_where(hitData < 1., mapData_1)
        mapData_2 = np.ma.masked_where(hitData < 1., mapData_2)
        mapData_3 = np.ma.masked_where(hitData < 1., mapData_3)
        hitData = np.ma.masked_where(hitData < 1., hitData)

        fig = plt.figure(figsize = (15,45), dpi=150)
	#fig = plt.figure(figsize = (15,45), dpi=150)
	gs1 = gridspec.GridSpec(2, 2)
	gs1.update(wspace=0.20, hspace=-0.83) # set the spacing between axes. 
        # hspace = -1 is overlapping figures
        
	x_min = x[1]
	x_max = x[-1] + (x[1]-x[0])
	y_min = y[1]
	y_max = y[-1] + (y[1]-y[0])
	myax = [x_min, x_max, y_min, y_max]

        maxVal = 100000  # max value for color plot
        minVal = -100000 # min value for color plot

        # A LSB
        #print '1/4 ...' 
	ax1 = fig.add_subplot(gs1[0])#,figsize=(10,10))#,aspect='equal')
        #ax1.set_aspect('equal')
	im1 = ax1.imshow(mapData_0, extent=(x_min, x_max, y_min, y_max),interpolation='nearest',cmap=plt.cm.viridis)#,vmin=minVal, vmax=maxVal)
	plt.axis(myax)
	ax1.xaxis.set_visible(False)
	#plt.xlabel('Right Ascension [deg]')
	plt.ylabel('Declination [deg]')
	plt.title(r'A LSB')# [$\mu$K]')
	divider = make_axes_locatable(ax1)
	cax1 = divider.append_axes("right", size="5%", pad=0.05)
	plt.colorbar(im1, ax=ax1, cax=cax1)
        
        # A USB
        #print '2/4 ...'
        #maxVal = 80000
	ax2 = fig.add_subplot(gs1[1])#,aspect='equal')
	im2 = ax2.imshow(mapData_1, extent=(x_min, x_max, y_min, y_max),interpolation='nearest',cmap=plt.cm.viridis)#,vmin=-maxVal, vmax=maxVal)
	plt.axis(myax)
	ax2.yaxis.set_visible(False)
	ax2.xaxis.set_visible(False)
	#plt.xlabel('Right Ascension [deg]')
	#plt.ylabel('Declination [deg]')
	plt.title(r'A USB')# [$\sigma$]')
	divider = make_axes_locatable(ax2)
	cax2 = divider.append_axes("right", size="5%", pad=0.05)
	plt.colorbar(im2, ax=ax2, cax=cax2)

        # B LSB
        #print '3/4 ...'
	#maxVal = 40000
	ax3 = fig.add_subplot(gs1[2])
	im3 = ax3.imshow(mapData_2, extent=(x_min, x_max, y_min, y_max),interpolation='nearest',cmap=plt.cm.viridis)#,vmin=-maxVal, vmax=maxVal)
	plt.axis(myax)
	plt.xlabel('Right Ascension [deg]')
	plt.ylabel('Declination [deg]')
	plt.title(r'B LSB')# [$\mu$K]')
	divider = make_axes_locatable(ax3)
	cax3 = divider.append_axes("right", size="5%", pad=0.05)
	plt.colorbar(im3, ax=ax3, cax=cax3)

        # B USB
        #print '4/4 ...'
	ax4 = fig.add_subplot(gs1[3])
	im4 = ax4.imshow(mapData_3, extent=(x_min, x_max, y_min, y_max),interpolation='nearest',cmap=plt.cm.viridis)#,vmin=-maxVal, vmax=maxVal)
	ax4.yaxis.set_visible(False)
	plt.axis(myax)
	plt.xlabel('Right Ascension [deg]')
	#plt.ylabel('Declination [deg]')
	plt.title('B USB')
	divider = make_axes_locatable(ax4)
	cax4 = divider.append_axes("right", size="5%", pad=0.05)
	plt.colorbar(im4, ax=ax4, cax=cax4)
        
        #fig.suptitle(str(scan_id))
        #fig.subplots_adjust(top=0.88)

	plt.savefig(mapname,bbox_inches='tight')
	plt.show()
        plt.close(fig)
        

def makeMap_gif(x, y, maps, hitData, mapname):

        cm.viridis.set_bad('w',1.) #color of masked elements
        nsb = 1#maps.shape[0]
        nfreq = 100#maps.shape[1]
        
        x_min = x[1]
        x_max = x[-1] + (x[1]-x[0])
        y_min = y[1]
        y_max = y[-1] + (y[1]-y[0])
        #myax = [x_min, x_max, y_min, y_max]
        #maxVal = 9.6e4  # max value for color plot
        #minVal = -9.6e4 # min value for color plot
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #div = make_axes_locatable(ax)
        #cax = div.append_axes('right', '5%', '5%')
        plt.ylabel('Declination [deg]')
        plt.xlabel('Right Ascension [deg]')
        frame = []
        ims = []
        for sb in range(nsb):
                for freq in range(nfreq):
                        mapData = maps[sb,freq,:,:]; mapData = np.swapaxes(mapData,0,1)
                        mapData = np.ma.masked_where(hitData < 1., mapData)
                        frame.append(mapData)
                        
        f0 = frame[0]
        vmax = np.max(f0); vmin = np.min(f0)
        im = ax.imshow(f0, extent=(x_min,x_max,y_min,y_max), interpolation='nearest',cmap=plt.cm.viridis, animated=True, vmin=vmin, vmax=vmax)
        cb = plt.colorbar(im)
        title = plt.text(0.5,1.01, 'sb 1, freq 1', ha='center', va='bottom',transform=ax.transAxes)
        ims.append([im,title,])
        #tx = ax.set_title('sb 1, freq 1')
        #tx = ax.text('sb 1, freq 1')
        i = 1
        for sb in range(nsb):
                print 'sb', sb+1
                for freq in range(nfreq):
                        if (sb == 0 and freq == 0):
                                continue
                        if ((freq+1)%10 == 0): print 'freq', freq+1
                        #mapData = maps[sb,freq,:,:]; mapData = np.swapaxes(mapData,0,1)
                        #mapData = np.ma.masked_where(hitData < 1., mapData)
                        #im = plt.imshow(mapData, extent=(x_min,x_max,y_min,y_max), interpolation='nearest',cmap=plt.cm.viridis, animated=True)
                        im = ax.imshow(frame[i], extent=(x_min,x_max,y_min,y_max), interpolation='nearest',cmap=plt.cm.viridis, animated=True, vmin=vmin, vmax=vmax)
                        #vmax = np.max(frame[i]); vmin = np.min(frame[i])
                        #cb = plt.colorbar(im)#, cax=cax)
                        #im.set_clim(vmin,vmax)
                        title = plt.text(0.5, 1.01, 'sb {}, freq {}'.format(sb+1,freq+1), ha='center', va='bottom',transform=ax.transAxes)
                        ims.append([im,title,])
                        #tx.set_text('sb {}, freq {}'.format(sb+1,freq+1))
                        i = i + 1


        anim = animation.ArtistAnimation(fig, ims, interval=500)#, blit=True)#, repeat_delay=1000)
        anim.save(mapname,writer='imagemagick', fps=2)
        #plt.show()
        #plt.close(fig)






# Set up functions, could possibly be added to the makeMap functions

def setup_one(pre, sb, freq, limit):
        print 'Plotting map for sb ', sb, ', freq ', freq
        x, y, maps, hit = readMap(pre)

        #max_val = maps[sb-1,freq-1,:,:].max()
        #print np.where(maps[sb-1,freq-1,:,:]==(max_val))

        mapname = pre + '_sb' + str(sb) + '_' + str(freq) + '_map.png'

        mapData = maps[sb-1,freq-1,:,:]#; mapData = np.swapaxes(mapData,0,1)
        hitData = hit[sb-1,freq-1,:,:]#;  hitData = np.swapaxes(hitData,0,1)

        mapData = swap_xy(mapData)
        hitData = swap_xy(hitData)

        #print mapData.shape
        #makeMap_noise(x, y, mapData, hitData, mapname, limit)
        makeMap_one(x, y, mapData, hitData, mapname)
        print 'Done!'


def setup_add4(pre):
        print 'Adding all frequencies per sb'
        x, y, maps, hit = readMap(pre)
        hitData = hit[0,0,:,:];  hitData = swap_xy(hitData)
        #print maps.shape
        nx = len(x); ny = len(y)
        #print nx, ny
        mapData_0 = np.zeros((nx,ny))
        mapData_1 = np.zeros((nx,ny))
        mapData_2 = np.zeros((nx,ny))
        mapData_3 = np.zeros((nx,ny))
        nfreq = maps.shape[1]
        for i in range(nx):
                for j in range(ny):
                        mapData_0[i,j] = sum(maps[0,:,j,i])/nfreq
                        mapData_1[i,j] = sum(maps[1,:,j,i])/nfreq
                        mapData_2[i,j] = sum(maps[2,:,j,i])/nfreq
                        mapData_3[i,j] = sum(maps[3,:,j,i])/nfreq
        mapname = pre + '_sbs_map.png'
        makeMap_sb(x, y, mapData_0, mapData_1, mapData_2, mapData_3, hitData, mapname)
        print 'Done'


def setup_add1(pre):
        print 'Adding all frequencies in one plot'
        x, y, maps, hit = readMap(pre)
        hitData = hit[0,0,:,:];  hitData = swap_xy(hitData)
        nx = len(x); ny = len(y)
        mapData = np.zeros((nx,ny))
        nsb = maps.shape[0]
        nfreq = maps.shape[1]
        for i in range(nx):
                for j in range(ny):
                        mapData[i,j] = sum(sum(maps[:,:,j,i]))/(nfreq*nsb)
        mapname = pre + '_map.png'
        makeMap_one(x, y, mapData, hitData, mapname)
        print 'Done!'

def setup_diff(pre):
        print "Plotting the difference between two sb"
        x, y, maps, hit = readMap(pre)
        hitData = hit[0,0,:,:];  hitData = swap_xy(hitData)
        nx = len(x); ny = len(y)
        mapData = np.zeros((nx,ny))
        nfreq = maps.shape[1]
        for i in range(nx):
                for j in range(ny):
                        mapData[i,j] = (sum(maps[2,:,j,i])-sum(maps[3,:,j,i]))/nfreq
        mapname = pre + '_diff_map.png'
        makeMap_noise(x, y, mapData, hitData, mapname, 20000)
        print 'Done'

def setup_gif(pre):
        print "Plotting a gif"
        x, y, maps, hit = readMap(pre)
        hitData = hit[0,0,:,:];  hitData = swap_xy(hitData)
        nx = len(x); ny = len(y)
        mapData = np.zeros((nx,ny))
        mapname = pre + '_map.gif'
        makeMap_gif(x, y, maps, hitData, mapname)
        print 'Done'



pre = "files/patch1_" + str(scan_id)

if sys.argv[2] == 'sb':
        setup_add4(pre)
if sys.argv[2] == 'add':
        setup_add1(pre)
if sys.argv[2] == 'one':
        setup_one(pre, int(sb), int(freq), int(lim))
if sys.argv[2] == 'diff':
        setup_diff(pre)
if sys.argv[2] == 'gif':
        setup_gif(pre)
