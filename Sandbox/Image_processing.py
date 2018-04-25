

import cv2
import numpy as np
from skimage.filters import threshold_otsu
from skimage.measure import *
from PIL import *

import psutil
import os
def Do_image_processing():

    img_counter =0

    path = "Exp2.mp4"
    capture_counter = 200
    do_subtraction = False
    avg_count = 4
    avg_image_counter = avg_count #takes averrage of those many images.
    Vid = cv2.VideoCapture(path)

    forthefirsttime = True
    structural_el = np.ones((5,5),np.float)
    i=0
    MINArea=5000
    SECONDS=1
    temp1 = 0
    temp = 0
    while (Vid.isOpened()):

        _,camera_image = Vid.read()
        # print(i)
        img_height, img_width, img_channels = camera_image.shape

        if forthefirsttime:
            """
            we need to run this if statement only once to get the height and width of the image
            """
            img_height, img_width, img_channels = camera_image.shape
            avfg_img = np.zeros((img_height, img_width), dtype=np.float)
            background_model = np.zeros((img_height, img_width), dtype=np.float)
            forthefirsttime = False

        sys_mem = psutil.virtual_memory().percent
        temp = max(temp,sys_mem)
        print('Sys_mem:',sys_mem,"max:",temp)


        #converting image to grayscale
        b_lab_image = cv2.cvtColor(camera_image, cv2.COLOR_BGR2GRAY)

        #convert image from uint8 to floating point
        b_lab_image = scaletofloat(b_lab_image)


        if do_subtraction:
            """
            code for backround subtraction
            """
            #background subtracted image
            back_sub = cv2.absdiff(b_lab_image,background_model)

            #finding the threshold to binarize the image
            thresh = threshold_otsu(back_sub)


            #binarizing it
            ret, back_sub_binary = cv2.threshold(back_sub,thresh,1,cv2.THRESH_BINARY)


            #doing im open to remove unwanted noise
            imopen_image = cv2.morphologyEx(back_sub_binary, cv2.MORPH_OPEN, structural_el)


            #finding region in an image
            Bwlabel,num_regions =label(imopen_image, neighbors=None, background=0, return_num=True, connectivity=2)


            a = cv2.Sobel(camera_image,cv2.CV_64F,1,0,ksize=5)
            b = cv2.Sobel(camera_image,cv2.CV_64F,1,0,ksize=5)
            c= cv2.Laplacian(camera_image,cv2.CV_64F)
            kernel = np.ones((5, 5), np.float32) / 25
            dst = cv2.filter2D(camera_image, -1, kernel)

            pid = os.getpid()

            py = psutil.Process(pid)
            memoryUse = py.memory_info()[0] / (2. ** 20)  # memory use in MiB
            temp1 = max(temp1, memoryUse)
            print('memoryUse:', memoryUse, "Max:", temp1)
            #print(num_regions)
            Area_region = regionprops(Bwlabel, intensity_image= None, cache=True)

            bbox_ccordinates=[]
            for labels in range (1,num_regions):
                if Area_region[labels].area >MINArea:
                    bbox_ccordinates.append(Area_region[labels].bbox)


            for points in bbox_ccordinates:
                cv2.rectangle(camera_image,(points[0],points[1]),(points[2],points[3]),(0,255,0),3)

            #print(bbox_ccordinates)










            cv2.imshow('back_image',camera_image)



            cv2.waitKey(SECONDS)



        if i > avg_image_counter:
            """
            add avg_image_counter images, take their average and that will be the background model
            """

            avg_image_counter -=1
            avfg_img= cv2.add(avfg_img,b_lab_image)


            if avg_image_counter == 0:

                do_subtraction = True
                avg_image_counter =avg_count
                background_model = avfg_img / avg_count
                #cv2.imshow('hey', background_model)
                #cv2.waitKey(4)
                avfg_img = np.zeros((img_height, img_width), dtype=float)
        i+=1

    img_save = cv2.cvtColor(camera_image, cv2.COLOR_BGR2GRAY)
    img_name = "opencv_frame_{}.png".format(img_counter)
    cv2.imwrite(img_name, img_save)
    print("{} written!".format(img_name))
    camera_image.release()

    cv2.destroyAllWindows()


def scaletofloat(img):
    pixelmin = np.min(img.ravel())
    pixelmax = np.max(img.ravel())
    rt = (img.astype('float') - pixelmin) / (pixelmax - pixelmin)
    return rt


def main():
    Do_image_processing()

if __name__=='__main__':
    main()