"""
grayscale: converts colored image to grayscale
binary: converts a gray image to a binary image
scaletoFloat: converts a uint8 image to floating point.
imopen : morphological operations
VideoCapture: Captures the frame by frame from the prerecorded video
Blob detection: Detects blobs in binary image
"""

import cv2
import numpy as np
from skimage.filters import threshold_otsu
from skimage.measure import *


def display_len(input_image_dct):
    print("\tlength of input dict:", len(input_image_dct))

    for key in input_image_dct:
        print(key,"Length of the buffer",len(input_image_dct[key]),
              "Shape:", input_image_dct[key][0])

    return None

def GrayScale(input_image_dct):
    """
    Converts a colored image to grayscale
    :param input_image_dct: input will be a dictionary of source id :input image
    :return:
    """
    output = []
    for key in input_image_dct:
        for img in input_image_dct[key]:
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            output.append(gray_image)
    print("completed grayscale")
    return output


def imBinarize(input_image_dct):
    """
    The method uses otsu's method to find the threshold to convert it to a binary image.
    :param input_image_dct:the dictionary of source id :input image will be a 2-D grayscale image
    :return:
    """
    output = []

    for key in input_image_dct:
        for img in input_image_dct[key]:
            thresh = threshold_otsu(img)
            ret, binarized = cv2.threshold(img, thresh, 1, cv2.THRESH_BINARY)
            output.append(binarized)

    print("done with binarizing")
    return output


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
    structural_el = np.ones((10, 10), np.float)
    imopen_image = cv2.morphologyEx(Binary_image, cv2.MORPH_OPEN, structural_el)
    return imopen_image


def VideoCapture(dct):
    """
    The function reads frame from a prerecorded video frame by frame
    :return:
    """

    # this path is just for testing
    output = []
    path = "Experiment.mp4"
    Vid = cv2.VideoCapture(path)
    while (Vid.isOpened()):
        # frame by frame is read here
        rt, frame = Vid.read()
        # grayscale
        if rt != False:
            output.append(frame)
        else:
            break

    print("done with video capture")
    return output

    # code for converting it to grayscale
    # and then storing it in Databank
    # depends on the future design


# def BlobDetection(Binary_image):
#     """
#     Takes input as Binary image and performs blob detection
#     :param Binary_image: a black and white binary image
#     :return:
#     """
#
#     MINArea = 5000
#     Imopen_image = imopen(Binary_image)
#     Bwlabel, num_regions = label(Imopen_image, neighbors=None, background=0,
#                                  return_num=True, connectivity=2)
#
#     # print(num_regions)
#     Area_region = regionprops(Bwlabel, intensity_image=None, cache=True)
#
#     bbox_ccordinates = []
#     for labels in range(1, num_regions):
#         if Area_region[labels].area > MINArea:
#             bbox_ccordinates.append(Area_region[labels].bbox)
#
#             # bbox_coordinates is a list containing tuples
#             # each tuple has (x1,y1,x2,y2) coordinates of a bounding box
#             # depends on the future design

def Background_Subtraction_And_Binarize(input_image_dct):
    """
    fucntion takes input as a dictionary contianing list of gray scled images and background models
    it performs 'background subtraction' and stores it in a list.
    After that each background subtracted image is binarized using utsu's thresholding
    :param input_image_dct: dictionary contaning two lists 1.gray scaled images in 'uint8' format and
    background model in 'float' format.
    :return: list containng background subtracked images
    """

    Buffer_output =[]
    output=[]
    dummy =[]
    images=[]
    back_model =[]
    back_model_size = 5
    for keys in input_image_dct:
        if len(dummy)!=0:
            if len(dummy)> len(input_image_dct[keys]):
                images = dummy
                back_model = input_image_dct[keys]
            else:
                back_model=dummy
                images = input_image_dct[keys]
            break
        dummy = input_image_dct[keys]

    # print(len(images),len(back_model))
    back_model_idx=0
    for idx in range(5,len(images)):
        img = images[idx]
        img = scaletofloat(img)
        if (idx+1)% back_model_size ==0:
            back_model_idx+=1
        back_sub = cv2.absdiff(img, back_model[back_model_idx])
        Buffer_output.append(back_sub)

    for back_sub_images in Buffer_output:
        binarized_image = GRAY2BINARY(back_sub_images)
        output.append(binarized_image)

    return output



def Blob_Detection_and_Bounding_box(input_img_dct):
    """

    :param input_img_dct:
    :return:
    """
    structural_el = np.ones((5, 5), np.float)
    MINArea=5000
    colored_images=[]
    binarized_images =[]

    for keys in input_img_dct:
        if len(input_img_dct[keys][0].shape)==3:
            colored_images= input_img_dct[keys]
            print("found colored images")
        else:
            binarized_images=input_img_dct[keys]
            print("found binarized images")
    difference_in_frames = len(colored_images)-len(binarized_images)

    cv2.namedWindow('OUTPUT')
    # print(len(colored_images))
    # print(len(binarized_images))
    for img_idx in range (len(colored_images)):
        camera_image= colored_images[img_idx]

        if(img_idx>=difference_in_frames):
            # performing morphlogical opening on the image

            imopen_image = cv2.morphologyEx(binarized_images[img_idx-difference_in_frames]
                                            , cv2.MORPH_OPEN, structural_el)
            # finding region in an image
            Bwlabel, num_regions = label(imopen_image, neighbors=None, background=0, return_num=True, connectivity=2)

            # print(num_regions)
            Area_region = regionprops(Bwlabel, intensity_image=None, cache=True)

            bbox_ccordinates = []
            for labels in range(1, num_regions):
                if Area_region[labels].area > MINArea:
                    bbox_ccordinates.append(Area_region[labels].bbox)

            for points in bbox_ccordinates:
                cv2.rectangle(camera_image, (points[0], points[1]), (points[2], points[3]), (0, 255, 0), 3)

        cv2.imshow('OUTPUT',camera_image)
        cv2.waitKey(4)

def GRAY2BINARY(input_image):
    """
    The method uses otsu's method to find the threshold to convert it to a binary image.
    :param input_image:the input image will be a 2-D grayscale image
    :return:
    """
    thresh = threshold_otsu(input_image)
    ret, binarized = cv2.threshold(input_image, thresh, 1, cv2.THRESH_BINARY)
    return binarized