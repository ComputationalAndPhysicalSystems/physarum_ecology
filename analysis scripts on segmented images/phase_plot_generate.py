#This code generate the phase plot used in the paper

import numpy as np
import numpy as np
import pywt
import matplotlib.pyplot as plt
import matplotlib.pyplot as pyplot
import glob
from matplotlib import cm


home_dir = "/home/lpe/Desktop/idk_phy/*Random*"


my_files = (glob.glob(home_dir))

my_files.sort()
fig, axis1 = pyplot.subplots( constrained_layout=True,figsize= (30,18))
axis1.axhline(y=0, color='k',linestyle = "--")
axis1.axvline(x=0, color='k',linestyle = "--")


smooth_diff_phy = []
smooth_diff_yeast = []

viridis = cm.get_cmap('Dark2', 8)

def rsquared(x, y, degree):

    coeffs = numpy.polyfit(x, y, degree)
    correlation = numpy.corrcoef(x, y)[0,1]
     # r-squared
    correlation**2

    return correlation**2

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
plot_legible = 0
i = 0
for file in my_files:
    print("hi")
    file_loc = file
    
    new_file_name = str(directory_for_imgs + file.split("/")[5][:-4] + "-freq_outl-.png")    
    plate_number = new_file_name.split("/")[-1].split("-")[1]
    sst = np.genfromtxt(file_loc, skip_header=0)
    sst = (sst[:-100,1])
    sst1 = np.genfromtxt(file_loc, skip_header=0)
    sst1 = sst1[:-100,0]# / sst[:-100,

    yeast = sst1
    active_plasmodia = sst

    smoothed_yeast = moving_average(yeast,24)
    smooth_ap = moving_average(active_plasmodia,24)
    
    big_ar = np.asarray(smoothed_yeast) + np.asarray(smooth_ap) 
    
    big_ar = (np.max(big_ar))
    
    normalized_yeast =  (big_ar + smoothed_yeast)/big_ar
    normalized_physarum =  (big_ar + smooth_ap)/big_ar

    diff_ap = np.diff(normalized_physarum)
    diff_yeast = np.diff(normalized_yeast)

    
    m, b = np.polyfit(diff_ap, diff_yeast, 1)
    r2 = rsquared(diff_ap,diff_yeast,1)
    
    print(r2)
    
    smooth_diff_phy= diff_ap
    diff_yeast = diff_yeast
    
    colorused = viridis(i)
    
    
    axis1.plot(smooth_diff_phy, m*smooth_diff_phy + b, c =colorused)
    axis1.scatter(diff_ap, diff_yeast , s = 20,label = "plate number {}; $R^2$ = {:.3f}".format(plate_number,r2),color = colorused) # active
    axis1.set_ylabel('yeast growth per frame',size = 45)
    axis1.set_xlabel('P. polycephalum growth per frame',size =45)
    #axis1.set_label("plate number{}".format(plate_number))
    #np.asarray(smooth_diff_phy).flatten()
    #np.asarray(smooth_diff_yeast).flatten()

    new_file_name = str(directory_for_imgs + file.split("/")[5][:-4] + "-freq_outl-.png")
    print(new_file_name)
    plot_legible = plot_legible +.0015
    i = i + 1
    print(plot_legible)
    
leyendo = pyplot.legend(fontsize = 45)

axis1.tick_params(axis='both', which='major', labelsize=40)

for handle in leyendo.legendHandles:
    handle.set_sizes([100.0])
pyplot.savefig(new_file_name,pad_inches=0.4)
pyplot.close()

