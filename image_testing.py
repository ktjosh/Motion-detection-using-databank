import cv2
import numpy as np


def img_process():
    ret, camera_image = cv2.VideoCapture(0).read()
    img1= cv2.cvtColor(camera_image, cv2.COLOR_BGR2LAB)
    img1 = img1[:,:,2]
    img1 = im2double(img1)
    for i in range(4):

        ret,camera_image = cv2.VideoCapture(0).read()


        lab_image = cv2.cvtColor(camera_image, cv2.COLOR_BGR2LAB)


        lab_image = lab_image[:,:,2]
        lab_image=im2double(lab_image)
        img1 = cv2.add(img1, lab_image)

    img1 = img1/4
    img_name = "opencv_frame_{}.png".format(0)

    cv2.imshow('ImageWindow', img1)
    cv2.waitKey()
    cv2.imwrite(img_name, img1)
    print("{} written!".format(img_name))

    #camera_image.release()

    cv2.destroyAllWindows()


def im2double(im):
    min_val = np.min(im.ravel())
    max_val = np.max(im.ravel())
    out = (im.astype('float') - min_val) / (max_val - min_val)
    return out





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