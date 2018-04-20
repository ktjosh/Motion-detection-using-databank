import socket
import numpy as np
import pickle
import cv2
import math
from sys import getsizeof
import time
def client():


    # ATTEMPT TO TRANSFER IMAGE

    WINDOW_SIZE = 1024
    HOST = "localhost"
    PORT = 9000
    Buffer_size = 4096
    file_name = "cat.png"
    # Open in 'b' because image reading in binary mode
    # file = open(file_name, 'rb')





    # Define socket and connect to server
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((HOST, PORT))



    path = "Experiment.mp4"
    Vid = cv2.VideoCapture(path)
    i=0
    while (Vid.isOpened()):
        # frame by frame is read here
        _,frame = Vid.read()

        file1 = GrayScale(frame)

        #file1 = np.zeros((640,640))
        #cv2.imshow('hey', file1)
        #cv2.waitKey(1)
        #print(file1)
        #exit(5)
        file = pickle.dumps(file1)
        #leng = math.ceil(len(file)/Buffer_size )
        #print(leng)
        #soc.send(pickle.dumps(leng))
        #
        #soc.send(file)

        x = 0
        y = Buffer_size

        content = file[x:y]
        while content:
            i += 1
            print(i)
            soc.send(content)
            x += Buffer_size
            y += Buffer_size
            content = file[x:y]
        #time.sleep(0.5)
        #
        # b = bytearray(Buffer_size)
        # word_dump = pickle.dumps(b)
        # soc.send(word_dump)

    #print(file1.shape)

    # Read bytes from file and send until the end of file
    # content = file.read(WINDOW_SIZE)
    # while content:
    #     soc.send(content)
    #     content = file.read(WINDOW_SIZE)

    # Close file and socket
    soc.close()
    # file.close()


def GrayScale(input_image):
    """
    Converts a colored image to grayscale
    :param input_image: input will be a numpy array of coloed image
    :return:
    """
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    return gray_image
if __name__ == "__main__":
    client()