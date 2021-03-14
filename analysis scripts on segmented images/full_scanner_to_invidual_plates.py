#circle_container = circleLog[1][0]
import os
import numpy as np
import cv2
import copy

#get the circle
segmented_dirs = os.listdir("/home/lpe/Desktop/segmented/")
print(segmented_dirs)

segmented_directory = "/home/lpe/Desktop/segmented/"
raw_dir_circ = "/home/lpe/Desktop/segment_me/"





circle_list = []


#Compute circles for each directory /experiment

for directory in os.listdir(segmented_directory):
    circle_find = raw_dir_circ + directory
    firs_circ = os.listdir(circle_find)
    res = [k for k in firs_circ if '.png' in k]
    sorted_dir_listy0 = sorted(res, key=lambda item: (int(item.partition('-')[1]) if item[1].isdigit() else float('inf'), item))#
    circular_image = (  raw_dir_circ + directory +  "/" +sorted_dir_listy0[0])
    #circular_image = (raw_dir_circ + sorted_dir_list0[0])
    print(circular_image)

#base_n_list = [base_dir + s for s in the_dirs]

    image = cv2.imread(circular_image)
    mask = cv2.threshold(image, 35,150, cv2.THRESH_BINARY)[1]
    #plt.figure(figsize=(50, 20))

    #edges = mask[:,:,1]
    edges = image[:,:,1]

    circles = None

    minimum_circle_size = 174      #this is the range of possible circle in pixels you want to find
    maximum_circle_size = 176     #maximum possible circle size you're willing to find in pixels

    guess_dp = 1.0

    number_of_circles_expected = 6          #we expect to find six cirlcles
    breakout = False

    #hand tune this
    max_guess_accumulator_array_threshold = 40     #minimum of 1, no maximum, (max 300?) the quantity of votes 
                                                    #needed to qualify for a circle to be found.
    circleLog = []

    guess_accumulator_array_threshold = max_guess_accumulator_array_threshold

    while guess_accumulator_array_threshold > 1 and breakout == False:
        #start out with smallest resolution possible, to find the most precise circle, then creep bigger if none found
        guess_dp = 1.0
        #rint("resetting guess_dp:" + str(guess_dp))
        while guess_dp < 5.5 and breakout == False:
            guess_radius = maximum_circle_size
            #rint("setting guess_radius: " + str(guess_radius))
            #rint(circles is None)
            while True:

                #HoughCircles algorithm isn't strong enough to stand on its own if you don't
                #know EXACTLY what radius the circle in the image is, (accurate to within 3 pixels) 
                #If you don't know radius, you need lots of guess and check and lots of post-processing 
                #verification.  Luckily HoughCircles is pretty quick so we can brute force.

                circles = cv2.HoughCircles(edges, 
                    cv2.HOUGH_GRADIENT, 
                    dp=guess_dp,               #resolution of accumulator array.
                    minDist=330,                #number of pixels center of circles should be from each other, hardcode
                    param1=30,
                    param2= guess_accumulator_array_threshold,
                    minRadius=(guess_radius-3),    #HoughCircles will look for circles at minimum this size
                    maxRadius=(guess_radius+3)     #HoughCircles will look for circles at maximum this size
                    )

                if circles is not None:
                    if len(circles[0]) == number_of_circles_expected:
                        #rint("len of circles: " + str(len(circles)))
                        circleLog.append(copy.copy(circles))
                        #rint("k1")
                    break
                    circles = None
                guess_radius -= 5 
                if guess_radius < 174:
                    break

            guess_dp += 1.5

        guess_accumulator_array_threshold -= 2

    #Return the circleLog with the highest accumulator threshold

    # ensure at least some circles were found
    for cir in circleLog:
        # convert the (x, y) coordinates and radius of the circles to integers
        #output = np.copy(orig_image)

        if (len(cir) > 1):
            #rint("FAIL before")
            exit()

        #rint(cir[0, :])

        cir = np.round(cir[0, :]).astype("int")

    circle_list = np.append(circle_list, circleLog[1])



    circle_container = circleLog[1][0]




#Iterate through the Directory and crop scanners to individual plasmodia

    for seg_image in sorted_dir_listy0:

        seg_img_npath = segmented_directory  +directory + "/" +  (seg_image[:-6]) +"-unet_segmented.tiff"
        print(seg_img_npath)
        #CUT DA PLATE
        counter = 0
        
        platess = sorted(circle_container, key = lambda x: (x[1], x[0]))

        
        for circle in  platess:
            radis = circle[2]


            im = cv2.imread(seg_img_npath)
            x = int(round(circle[0]))

            y = int(round(circle[1]))

            radius = int(round(radis))

            first_x = x - radius 
            first_y = y - radius 


            second_x = x + radius 
            second_y = y + radius
            crop_img1 = im[y - radius:y  + radius,x - radius: x + radius]

            new_img = (segmented_directory  +directory + "/" +"chopt" + "_" +directory + "/" +  (seg_image[:-5])+"-" + str(counter) + "-" + "unet_segmented.png")
            #print(segmented_directory  +directory + "/" + chopped_up + "/")
            counter = counter + 1
            cv2.imwrite(new_img, crop_img1[:,:,0]) 
    
