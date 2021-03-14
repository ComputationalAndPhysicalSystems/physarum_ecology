import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d as gaus_1d
from scipy.ndimage.filters import uniform_filter as mean_filter
import glob
from scipy.ndimage import binary_dilation as dilate

#Function to threshold invidial plasmodia semantic segmentations and append images to arr. You can set thresh to a certain value if you wish to not do thresholding
def dir_to_XYT_img_arr(director,images, x_dim,y_dim, thresh):
    counter = 0
    img_ar = np.zeros(shape=(x_dim,y_dim,len(images)))

    for z in images:

        image_in = cv.imread(director +"/" + z)

        #filter_img = image_in[:,:,0]
        if (thresh == 1303):
            img_ar_filtered = image_in[:,:,0]
        else:
            filter_img = image_in[:,:,0]
            filter_img[filter_img != thresh] = 0
            img_ar_filtered = mean_filter(filter_img, size = 5, mode="constant")

        if (img_ar_filtered.shape == (x_dim,y_dim)):
            img_ar[:,:,counter] = img_ar_filtered
        else:
            print(z.split("-")[1],counter)

        counter = counter + 1
    return(img_ar)

img_adr = ('-5-unet','-4-unet','-3-unet','-2-unet','-1-unet','-0-unet')
img_dirs = glob.glob("/home/lpe/Desktop/segmented/**/*chopt*")
img_dirs = img_dirs[11:]
for chopt in img_dirs:
    for adress in img_adr:
# look thru directories/experiments, and sort them with linux time stamp/img adress
#Threshold them
        directoy_adress = os.listdir(chopt)
        
        print(adress)
        result = [r for r in directoy_adress if adress in r]
        sorted_dir_list0 = sorted(result, key=lambda item: (int(item.partition('-')[1]) if item[1].isdigit() else float('inf'), item))#
        print(len(sorted_dir_list0))
        if (len(sorted_dir_list0) > 0):
            image_in = cv.imread(chopt+"/" + sorted_dir_list0[0])
            im_dim = image_in.shape
            print(im_dim)
            directory = sorted_dir_list0
            x_dim_enter = im_dim[0]
            y_dim_enter = im_dim[1]

            yeast_ar = dir_to_XYT_img_arr(chopt, directory,x_dim_enter,y_dim_enter,209)
            phy_ar = dir_to_XYT_img_arr(chopt,directory,x_dim_enter,y_dim_enter,150)

            time_smooth_physarum = gaus_1d(phy_ar, sigma= 3, axis = 2)
            time_smooth_yeast =  gaus_1d(yeast_ar, sigma= 3, axis = 2)

            time_arr = np.sum(time_smooth_yeast, axis=2)
            time_arr_phy = np.sum(time_smooth_physarum, axis=2)
#Compute a mask of areas in which Physarum and yeast both occur over the course of the whole time series
            cert_thresh = 5
            time_arr[(time_arr/time_smooth_physarum.shape[2] > cert_thresh)  & (time_arr_phy/time_smooth_physarum.shape[2] >cert_thresh)] = 422
            time_arr[time_arr != 422] = 0

            time_mask = (time_arr > 0)
            new_mask = dilate(time_mask, iterations= 10)
            time_mask = new_mask

            yeast_ar = []
            phy_ar = []

#With the time mask generated geneate untrheshed ecology array that has all values
            eco_ar = dir_to_XYT_img_arr(chopt, directory,x_dim_enter,y_dim_enter,1303)

            indices_from_bool = np.where(time_mask)


            time_list = []
# Only measure components of array that are within the eco_ar mask
            for x,y in zip(indices_from_bool[0],indices_from_bool[1]):
                #print(x,y)

                time_ac = eco_ar[x,y,:]
                time_list.append(time_ac)

#Measure Physarum and yeast in the the intecation zone/eco ar mask and Physarum and yeast outside of the eco ar mask. Write these measurements for individual plates / plasmodia to a file
            print(len(time_list))
            tlist_out = np.asarray(time_list)###################################

            if (len(tlist_out) > 0): 
                the_time = np.zeros(tlist_out.shape[1])
                pl1 = np.zeros(tlist_out.shape[1])
                pl2 = np.zeros(tlist_out.shape[1])
                pl3 = np.zeros(tlist_out.shape[1])
                pl4 = np.zeros(tlist_out.shape[1])
                pl5 = np.zeros(tlist_out.shape[1])

                pl6 = np.zeros(tlist_out.shape[1])
                for i in range(0, tlist_out.shape[1]):
                    # go through a list of all x,y coords in slice time-z
                    # Then we count 
                    #count_1 = sum((tlist_out[:,i] == 125.) * 1)
                    count_2 = sum((tlist_out[:,i] == 150.) * 1) #/ len(time_list)
                    #count_3 = sum((tlist_out[:,i] == 160.) * 1)
                    count_4 = sum((tlist_out[:,i] == 209.) * 1) #/len(time_list)
                    count_5 = sum((tlist_out[:,i] == 255.) * 1) #/len(time_list)

                    all_physarum= eco_ar[:,:,i].ravel()

                    all_phy = sum((all_physarum == 150.) * 1)
                    all_yeast = sum((all_physarum == 209.) * 1)
                    pl6[i] = all_phy #all phy
                    pl1[i] = all_yeast #all yeast
                    pl2[i] = count_2 #active physarum
                    #pl3[i] = count_3
                    pl4[i] =count_4 #yeast
                    pl5[i] = count_5 #inactive yeast
                    the_time[i] = i
                #fig = plt.figure(figsize= (30,10))
                #axis1 = fig.add_subplot(211)
                #axis1.plot(the_time, pl2 , c = 'orange') # active
                #axis1.plot(the_time, pl4, c = 'red') # yeast
                #axis1.plot(the_time, pl5, c = 'blue') # inactive
                #axis1.set_title(str(chopt[:-1].split('/')[-1]) + str(adress) + "\n Red:Yeast, Blue:Inactive plasmodia, Orange: Active", fontsize = 40)

                #axis2 = fig.add_subplot(212)
                #axis2.plot(the_time, pl6, c = 'orange') # all Physarum

                #save_it_plot = str(chopt[:-1].split('/')[-1]) + str(adress)
                #t("/home/lpe/Desktop/" + save_it_plot)
                #plt.close()

                np_out = np.vstack([pl2,pl4,pl6,pl1,the_time]).T #active physarum in cline, yeast in cline,all physarum, all yeast, time

                phy_pink = str("/home/lpe/Desktop/"+"ts_out" + save_it_plot + ".txt")
                np.savetxt(phy_pink,np_out,delimiter= '\t',fmt= '%10.0f', header="active physarum in cline, yeast in cline,all physarum, all yeast, time")
            else:
                print("oops")
