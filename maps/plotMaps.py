import numpy as np
import h5py
import sys
import getopt
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from matplotlib import animation, rc
from mpl_toolkits.axes_grid1 import make_axes_locatable
import textwrap
import random
from mpl_toolkits.axes_grid1 import make_axes_locatable

def usage():
    prefix = " "

    #"f:l:p:d:s:", ["freq=", "lim=", "plot =", "data=", "sb="
    preferredWidth = 150
    wrapper = textwrap.TextWrapper(initial_indent=prefix, width=preferredWidth,subsequent_indent=' '*len(prefix))
    m1 = "  (Frequency, given as a list with [sideband,frequency] as values. Default none) "
    m2 = "  (Plot type, either one (1 plot), four (4 plots), diff (a difference plot) or gif. Default four) "
    m3 = "  (Data type, either map (the map), rms (root mean square), map/rms or all (all 3 + hit count). Default map)"
    m4 = "    (Side band for difference plot as a list, ie. [1,4]. Default none) "
    print "\nThis is the usage function\n"
    print "Flags:"
    print "-f ----> optional --freq", wrapper.fill(m1)
    print "-p ----> optional --plot", wrapper.fill(m2)
    print "-d ----> optional --data", wrapper.fill(m3)
    print "-s ----> optional --sb", wrapper.fill(m4)
    print ""    
    sys.exit()


plt.switch_backend('agg')

if len(sys.argv[1]) == 3:
    scan_id = sys.argv[1]
    filename = "files/patch1_" + str(scan_id) + "_map.h5"   
else:
    filename = sys.argv[1] 

#if sys.argv[2] == 'add':
#        add = True

#else:
#        add = False

try:
    opts, args = getopt.getopt(sys.argv[2:],"f:l:p:d:s:", ["freq=", "lim=", "plot =", "data=", "sb="])
except getopt.GetoptError:
    usage()


# default values
freq            = 2
sb              = 1
lim             = None
set_sb          = False
set_freq        = False
data            = "map"      
plot            = "four"
plot_choices    = ["one", "four", "diff", "gif"]
freq_choices    = ["all", "s1", "s2", "s3", "s4"]
s_choices       = ["s1", "s2", "s3", "s4"]
data_choices    = ["all", "rms", "map", "map/rms"]
set_freq        = False
set_sb          = False
for opt, arg in opts:
    if opt in ("-f", "--freq"):
        if arg in freq_choices:
            freq = arg
        elif ((type(eval(arg)) == list) and (len(eval(arg)) == 2)):
            set_freq = True
            freq    = eval(arg)          
        else:
            print "The frequency choice must either be all, s1, s2, s3 or a list specifying side band and frequency, ie. [1,22] for side band 1 and frequency 22."
            print "See -h or the README file for more information"
            sys.exit()
        if freq == "all":
            pass
        elif freq in s_choices:
            pass
        else:
            if (1 > freq[0]) or (freq[1] > 4):
                print "The side band index needs to be in the range 1-4"
                sys.exit() 

            if (1 > freq[1]) or (freq[1] > 32):
                print "The frequency index needs to be in the range 1-32"
                sys.exit() 

    elif opt in ('-l', '--lim'):
        lim     = int(arg)

    elif opt in ('-s', '--sb'):
        set_sb = True
        sb    = eval(arg)   
        if len(sb) == 2:
            pass    
        else:
            print "You need to specify 2 side bands in a list to plot the difference between them, ie. [1,4]. See -h or the README file for more information"
            sys.exit()


    elif opt in ('-p', '--plot'):
        if arg in plot_choices:
            plot    = arg
        else:
            print "The plot choice need to be either one, four, diff or gif. See -h or the README file for more information"
            sys.exit()
    elif opt in ('-d', '--data'):
        if arg in data_choices:
            data = arg
        else:
            print "The data choice needs to be map, rms, map/rms or all."
            sys.exit()
    elif opt in ('-h', '--help'):
        usage()
        sys.exit()
    else:
        usage()

if plot_choices == "one":
    if data_choices == "all":
        print "For one plot only map, rms and map/rms are available data choices"
        sys.exit()
    else:
        pass

if set_sb:
    if plot == "diff":
        pass
    else:
        print "The side band flag is only used for difference plots."

if plot == "diff":
    if set_sb:
        pass
    else:
        print "You need to specify the side bands you want to take the difference between using the -s flag"
        sys.exit()

'''
Contains:

usage()         # prints usage of flags
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


def readMap(filename):
        dfile   = h5py.File(filename,'r')
        nx      = dfile['n_x'];      nx  = np.array(nx).astype(int) 
        ny      = dfile['n_y'];      ny  = np.array(ny).astype(int)
        x       = dfile['x'];         x  = np.array(x[:]).astype(float)
        y       = dfile['y'];         y  = np.array(y[:]).astype(float)
        maps    = dfile['map'];    maps  = np.array(maps[...]).astype(float)
        hit     = dfile['nhit'];    hit  = np.array(hit[...]).astype(float)
        rms     = dfile['rms'];     rms  = np.array(rms[...]).astype(float)

        return x, y, maps, hit, rms

def swap_xy(my_array):

        new_array = np.zeros((len(my_array[0]), len(my_array)))
        #my_array[:, 0], my_array[:, 1] = my_array[:, 1], my_array[:, 0].copy()
        for i in range(len(my_array[0])):
            new_array[i, :] = my_array[:, i]
        return new_array
   




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
        mapData_0ata = np.ma.masked_where(hitData < 1., mapData)
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



def makeMap_sb(x, y, mapData_0, mapData_1, mapData_2, mapData_3, hitData, mapname, titles):

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
    plt.title(titles[0])# [$\mu$K]')
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
    plt.title(titles[1])# [$\sigma$]')
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
    plt.title(titles[2])# [$\mu$K]')
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
    plt.title(titles[3])
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
        nsb = 1
        nfreq = 32
        
        x_min = x[1]
        x_max = x[-1] + (x[1]-x[0])
        y_min = y[1]
        y_max = y[-1] + (y[1]-y[0])
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.ylabel('Declination [deg]')
        plt.xlabel('Right Ascension [deg]')
                        
        frame = []
        ims = []
        i = 0
        for sb in range(nsb):
                for freq in range(nfreq):
                        if i > 1:
                            for k in range(145):
                                for j in range(130):
                                    maps[sb,freq,k,j] = maps[sb, freq-1, k, j]*random.random()
                            mapData = maps[sb,freq,:,:] 
                            mapData = np.swapaxes(mapData,0,1)
                            mapData = np.ma.masked_where(hitData < 1., mapData)
                            frame.append(mapData)
                        else:
                            mapData = maps[sb,freq,:,:] 
                            mapData = np.swapaxes(mapData,0,1)
                            mapData = np.ma.masked_where(hitData < 1., mapData)
                            frame.append(mapData)
                        i+=1

        cv0 = frame[0]
        div = make_axes_locatable(ax)
        cax = div.append_axes('right', '5%', '5%')
        im = ax.imshow(cv0, origin='lower') # Here make an AxesImage rather than contour
        cb = fig.colorbar(im,cax=cax)
        tx = ax.set_title('Frame 0')
        def animate(i):
            arr = frame[i]
            vmax     = np.max(arr)
            vmin     = np.min(arr)
            im.set_data(arr)
            im.set_clim(vmin, vmax)
            tx.set_text('Frame {0}'.format(i))

        ani = animation.FuncAnimation(fig, animate, frames=32)
        ani.save(mapname,writer='imagemagick', fps=2)





# Set up functions, could possibly be added to the makeMap functions

def setup_one(filename, sb, freq, limit):
        print 'Plotting map for sb ', sb, ', freq ', freq
        x, y, maps, hit, rms= readMap(filename)

        #max_val = maps[sb-1,freq-1,:,:].max()
        #print np.where(maps[sb-1,freq-1,:,:]==(max_val))

        mapname = filename[0:-7] + "_" + data + '_sb' + str(sb) + '_f' + str(freq) + '_map.png'
        if data == "map":
            print "Data type 'map' selected"
            var = maps[sb-1,freq-1,:,:]
        elif data == "rms":
            print "Data type 'rms' selected"
            var = rms[sb-1,freq-1,:,:]
        else:
            print "Data type 'map/rms' selected"
            print "rms data not available, rms and map/rms set to 0"
            var = np.zeros((len(maps[0,0]), len(maps[0,0,0])))
            #var = maps[sb-1,freq-1,:,:]/rms[sb-1,freq-1,:,:]            

        hitData = hit[sb-1,freq-1,:,:]#;  hitData = np.swapaxes(hitData,0,1)

        var = swap_xy(var)
        hitData = swap_xy(hitData)

        makeMap_one(x, y, var, hitData, mapname)
        print 'Done!'

def setup_all_all_freq(filename):
        print 'Adding all frequencies per sb'
        x, y, maps, hit, rms = readMap(filename)
        hitData = hit[0,0,:,:];  hitData = swap_xy(hitData)
        titles = ["map", "rms", "map/rms", "hitCount"]
        #print maps.shape
        nx = len(x); ny = len(y)
        #print nx, ny
        nfreq = maps.shape[1]
        nsb = maps.shape[0]
        mapData_0 = np.zeros((nx,ny))
        mapData_1 = np.zeros((nx,ny))
        mapData_2 = np.zeros((nx,ny))
        mapData_3 = np.zeros((nx,ny))

        print "rms data not available, rms and map/rms set to 0"
        for i in range(nx):
             #print i
             for j in range(ny):
                        #print j
                        mapData_0[i,j] = sum(sum(maps[:,:,j,i]))/nfreq/nsb
                        mapData_1[i,j] = sum(sum(rms[:,:,j,i]))/nfreq/nsb
                        if hitData[i, j] == 0: 
                            mapData_2[i,j] = 0
                        else:    
                            #mapData_2[i,j] = (sum(sum(maps[:,:,j,i]))/sum(sum(rms[:,:,j,i])))/nfreq/nsb
                            mapData_2[i, j] = 0
                        mapData_3[i,j] = sum(sum(hit[:,:,j,i]))/nfreq/nsb

        mapname = filename[0:-7] + '_4_all_map.png'
        makeMap_sb(x, y, mapData_0, mapData_1, mapData_2, mapData_3, hitData, mapname, titles)
        print 'Done'


def setup_all_one_freq(filename, sb, freq):
        print 'Plotting maps for sb ', sb, ', freq ', freq
        print "rms data not available, rms and map/rms set to 0"
        x, y, maps, hit, rms= readMap(filename)
        titles = ["map: sb %i, freq %i" %(sb, freq), "rms: sb %i, freq %i" %(sb, freq), "map/rms: sb %i, freq %i" %(sb, freq), "hitCount: sb %i, freq %i" %(sb, freq)]

        #max_val = maps[sb-1,freq-1,:,:].max()
        #print np.where(maps[sb-1,freq-1,:,:]==(max_val))

        mapname = filename[0:-7] + "_" + data + '_sb' + str(sb) + '_f' + str(freq) + 'all_map.png'
        x, y, maps, hit, rms = readMap(filename)
        hitData = hit[sb-1,freq-1,:,:];  hitData = swap_xy(hitData)
        titles = ["map", "rms", "map/rms", "hitCount"]
        #print maps.shape
        nx = len(x); ny = len(y)
        #print nx, ny
        nfreq = maps.shape[1]
        nsb = maps.shape[0]
        mapData_0 = maps[sb-1, freq-1,:,:]
        mapData_1 = rms[sb-1, freq-1,:,:]
        mapData_2 = np.zeros((ny, nx))#maps[sb-1, freq-1,:,:]/rms[sb-1, freq-1,:,:]
        mapData_3 = hitData
        mapData_0, mapData_1, mapData_2 = swap_xy(mapData_0), swap_xy(mapData_1), swap_xy(mapData_2)
        makeMap_sb(x, y, mapData_0, mapData_1, mapData_2, mapData_3, hitData, mapname, titles)
        print 'Done'

def setup_all_sb(filename, sb):
        print 'Adding all frequencies for sb', sb
        print "rms data not available, rms and map/rms set to 0"
        x, y, maps, hit, rms = readMap(filename)
        hitData = hit[sb-1,0,:,:];  hitData = swap_xy(hitData)
        #print maps.shape
        titles = ["map: sb %i" %sb, "rms: sb %i" %sb, "map/rms: sb %i" %sb, "hitCount: sb %i" %sb]
        nx = len(x); ny = len(y)
        #print nx, ny
        mapData_0 = np.zeros((nx,ny))
        mapData_1 = np.zeros((nx,ny))
        mapData_2 = np.zeros((nx,ny))
        mapData_3 = np.zeros((nx,ny))
        nsb = maps.shape[0]

        for i in range(nx):
                for j in range(ny):
                        mapData_0[i,j] = sum(maps[sb-1,:,j,i])/nsb
                        mapData_1[i,j] = sum(rms[sb-1,:,j,i])/nsb
                        mapData_2[i,j] = 0 #sum(maps[sb-1,:,j,i]/rms[sb-1,:,j,i])/nsb
                        mapData_3[i,j] = sum(hit[sb-1,:,j,i])/nsb
        mapname = filename[0:-7] + '_sb' + str(sb) + '_map.png'
        makeMap_sb(x, y, mapData_0, mapData_1, mapData_2, mapData_3, hitData, mapname, titles)
        print 'Done'


def setup_add4(filename):
        print 'Adding all frequencies per sb'
        x, y, maps, hit, rms = readMap(filename)
        hitData = hit[0,0,:,:];  hitData = swap_xy(hitData)
        #print maps.shape
        titles = ["A LSB", "A USB", "B LSB", "B USB"]
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
        mapname = filename[0:-7] + '_sbs_map.png'
        makeMap_sb(x, y, mapData_0, mapData_1, mapData_2, mapData_3, hitData, mapname, titles)
        print 'Done'


def setup_add1(filename):
        print 'Adding all frequencies in one plot'
        x, y, maps, hit, rms = readMap(filename)
        hitData = hit[0,0,:,:];  hitData = swap_xy(hitData)
        nx = len(x); ny = len(y)
        mapData = np.zeros((nx,ny))
        nsb = maps.shape[0]
        nfreq = maps.shape[1]
        for i in range(nx):
                for j in range(ny):
                        mapData[i,j] = sum(sum(maps[:,:,j,i]))/(nfreq*nsb)
        mapname = filename[0:-7] + '_all_freq' + '_map.png'
        #mapname = pre + '_map.png'
        makeMap_one(x, y, mapData, hitData, mapname)
        print 'Done!'

def setup_diff(filename, sb):
        print "Plotting the difference between sb %i and sb %i" %(sb[0], sb[1])
        x, y, maps, hit, rms = readMap(filename)

        hitData = hit[0,0,:,:]
 
        hitData = swap_xy(hitData)

        nx = len(x); ny = len(y)
        mapData = np.zeros((nx,ny))
        nfreq = maps.shape[1]
        for i in range(nx):
                for j in range(ny):
                        mapData[i,j] = (sum(maps[sb[0]-1,:,j,i])-sum(maps[sb[1]-1,:,j,i]))/nfreq
        mapname = filename[0:-7] + '_diff_map.png' 
        makeMap_noise(x, y, mapData, hitData, mapname, 20000)
        print 'Done'

def setup_gif(filename):
        print "Plotting a gif"
        x, y, maps, hit, rms = readMap(filename)
        hitData = hit[0,0,:,:];  hitData = swap_xy(hitData)
        nx = len(x); ny = len(y)
        mapData = np.zeros((nx,ny))
        mapname = filename[0:-7] + '_map.gif'
        makeMap_gif(x, y, maps, hitData, mapname)
        print 'Done'

if plot == 'one':
    if set_freq:
        setup_one(filename, freq[0], freq[1], lim)
    else:
        setup_add1(filename)
elif plot == "four":
    if data == "all":
        if freq == "all":
            setup_all_all_freq(filename)
        elif type(freq) == list:
            setup_all_one_freq(filename, freq[0], freq[1])
        else:
            if freq == "s1":
                setup_all_sb(filename, 1)
            elif freq == "s2":
                setup_all_sb(filename, 2)
            elif freq == "s3":
                setup_all_sb(filename, 3)
            else:
                setup_all_sb(filename, 4)
    else:
        setup_add4(filename)
elif plot == 'diff':
    setup_diff(filename, sb)
else:
    setup_gif(filename)

"""
plot_choices    = ["one", "four", "diff", "gif"]
freq_choices    = ["all", "s1", "s2", "s3", "s4"]
data_choices    = ["all", "rms", "map", "map/rms"]
"""