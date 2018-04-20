
import cv2
import numpy as np
from skimage.filters import threshold_otsu
from skimage.measure import *

def img_process():
    ret, camera_image = cv2.VideoCapture(0).read()
    img1= cv2.cvtColor(camera_image, cv2.COLOR_BGR2LAB)
    img1 = img1[:,:,2]
    img1 = scaletofloat(img1)
    for i in range(4):

        ret,camera_image = cv2.VideoCapture(0).read()


        lab_image = cv2.cvtColor(camera_image, cv2.COLOR_BGR2LAB)


        lab_image = lab_image[:,:,2]
        lab_image=scaletofloat(lab_image)
        img1 = cv2.add(img1, lab_image)

    img1 = img1/4
    img_name = "opencv_frame_{}.png".format(0)

    cv2.imshow('ImageWindow', img1)
    cv2.waitKey()
    cv2.imwrite(img_name, img1)
    print("{} written!".format(img_name))

    #camera_image.release()

    cv2.destroyAllWindows()






"""
grayscale: converts colored image to grayscale
binary: converts a gray image to a binary image
scaletoFloat: converts a uint8 image to floating point.
imopen : morphological operations
VideoCapture: Captures the frame by frame from the prerecorded video
Blob detection: Detects blobs in binary image
"""

def GrayScale(input_image):
    """
    Converts a colored image to grayscale
    :param input_image: input will be a numpy array of coloed image
    :return:
    """
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    return gray_image


def imBinarize(input_image):
    """
    The method uses otsu's method to find the threshold to convert it to a binary image.
    :param input_image:the input image will be a 2-D grayscale image
    :return:
    """
    thresh = threshold_otsu(input_image)
    ret, binarized = cv2.threshold(input_image, thresh, 1, cv2.THRESH_BINARY)
    return binarized

def scaletofloat(img):
    """
    Converts an integer image into floating point values
    :param img: the input will be a grayscaled 2D image
    :return: return a floating point scaled image
    """
    pixelmin = np.min(img.ravel())
    pixelmax = np.max(img.ravel())
    rt = (img.astype('float') - pixelmin) / (pixelmax - pixelmin)
    return rt

def imopen(Binary_image):
    """
    Takes binary image as input, perform morphological opening and returns
    Note: for simplicity stuctural element is definied in the image
    :param Binary_image: input wil be a blackand white binary image
    :return: return a noisefree image
    """
    structural_el = np.ones((10,10),np.float)
    imopen_image = cv2.morphologyEx(Binary_image, cv2.MORPH_OPEN, structural_el)
    return imopen_image

def VideoCapture():
    """
    The function reads frame from a prerecorded video frame by frame
    :return:
    """

    #this path is just for testing
    path = "..\\Experiment.mp4"
    Vid = cv2.VideoCapture(path)
    while(Vid.isOpened()):
        #frame by frame is read here
        _,frame = Vid.read()

    #code for converting it to grayscale
    #and then storing it in Databank
    #depends on the future design


def BlobDetection(Binary_image):


    MINArea = 5000
    Imopen_image = imopen(Binary_image)
    Bwlabel, num_regions = label(Imopen_image, neighbors=None, background=0, return_num=True, connectivity=2)

    # print(num_regions)
    Area_region = regionprops(Bwlabel, intensity_image=None, cache=True)

    bbox_ccordinates = []
    for labels in range(1, num_regions):
        if Area_region[labels].area > MINArea:
            bbox_ccordinates.append(Area_region[labels].bbox)

    #bbox_coordinates is a list containing tuples
    #each tuple has (x1,y1,x2,y2) coordinates of a bounding box
    #depends on the future design

def justread():
    img = cv2.imread("C:\\Users\\ketan\\PycharmProjects\\untitled\\ssup\\opencv_frame_0.png")

    img = img.astype('float')
    cv2.imshow('hey', img)
    cv2.waitKey()





def main():
    img_process()

    justread()
if __name__ == '__main__':
    main()