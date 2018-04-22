
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



def testing():
    output=[]
    path = "Experiment.mp4"
    Vid = cv2.VideoCapture(path)
    while (Vid.isOpened()):
        # frame by frame is read here
        rt, frame = Vid.read()
        # grayscale
        if rt != False:
            frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            output.append(frame)
        else:
            break

    print("done with video capture")
    dict ={}
    dict[1]=output
    Background_Model(dict)


"""
grayscale: converts colored image to grayscale
binary: converts a gray image to a binary image
scaletoFloat: converts a uint8 image to floating point.
imopen : morphological operations
VideoCapture: Captures the frame by frame from the prerecorded video
Blob detection: Detects blobs in binary image
Background Model
Background Subtraction
"""

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
    path = "\\Experiment.mp4"
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

def Background_Model(input_image_dct):
    """
    The function takes input as dictctionary containing lists of grayscale images
    it converts integer images to float and creates a background model depending on
    the number of frames to be taken for averaging
    :param input_image_dct: dictionary containing list of grayscaled images
    :return: list containing background model
    """


    output =[]
    back_model_size =5
    height,width = 0,0
    for keys in input_image_dct:
        for img in input_image_dct[keys]:
            height,width = img.shape
            break
    avg_img = np.zeros((height,width),dtype=float)
    for keys in input_image_dct:
        for idx  in  range (len(input_image_dct[keys])):
            img = scaletofloat(input_image_dct[keys][idx])
            avg_img = cv2.add(avg_img, img)
            if (idx+1) % back_model_size == 0:
                back_model = avg_img / back_model_size
                output.append(back_model)
                avg_img = np.zeros((height, width), dtype=float)
    # print(len(output))
    # cv2.namedWindow('ketan')
    # for images in output:
    #     cv2.imshow('ketan',images)
    #     cv2.waitKey(2)
    return output

def Background_Subtraction(input_image_dct):
    """
    fucntion takes input as a dictionary contianing list of gray scled images and background models
    it performs background subtraction and stores it in a list
    :param input_image_dct: dictionary contaning two lists 1.gray scaled images in 'uint8' format and
    background model in 'float' format
    :return: list containng background subtracked images
    """

    output =[]
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

    #back_sub = cv2.absdiff(b_lab_image, background_model)

    back_model_idx=0
    for idx in range(5,len(images)):
        img = images[idx]
        img = scaletofloat(img)
        if (back_model_idx+1)% back_model_size ==0:
            back_model_idx+=1
        back_sub = cv2.absdiff(img, back_model[back_model_idx])
        output.append(back_sub)

    return output



def justread():
    img = cv2.imread("C:\\Users\\ketan\\PycharmProjects\\untitled\\ssup\\opencv_frame_0.png")

    img = img.astype('float')
    cv2.imshow('hey', img)
    cv2.waitKey()





def main():
    testing()

    justread()
if __name__ == '__main__':
    main()