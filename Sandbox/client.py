import pickle
import socket

import cv2
import random

def client():
    # ATTEMPT TO TRANSFER IMAGE

    HOST = "localhost"
    PORT = 9000
    WINDOW_SIZE = 4096
    id = random.randint(10,20)
    print(id)

    img_list = []
    path = "Experiment.mp4"
    vid = cv2.VideoCapture(path)

    while vid.isOpened():
        # frame by frame is read here
        _, frame = vid.read()

        try:
            if _ == True:
                #gray_frame = GrayScale(frame)
                img_list.append(frame)

            else:
                break

        # Error encountered on the last frame: None is sent
        except TypeError:
            print("type+error")
            break

    print("Video Done")

    # Sending the img_list to the server

    # # If you want to send the whole img_lst

    # # Define socket and connect to server
    # soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # soc.connect((HOST, PORT))

    # image_serial = pickle.dumps(img_list)
    # start = 0
    # end = WINDOW_SIZE
    # content = image_serial[start:end]
    #
    # while content:
    #     soc.send(content)
    #     start += WINDOW_SIZE
    #     end += WINDOW_SIZE
    #     content = image_serial[start:end]

    # If you want send 10 images at a time

    IMAGE_BURST = len(img_list)
    buffer_list = []

    for i in range(len(img_list)+1):

        if i != len(img_list):
            buffer_list.append(img_list[i])

        if (i+1) % IMAGE_BURST == 0:  # or i == len(img_list):

            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.connect((HOST, PORT))
            soc.send(pickle.dumps(id))

            file = pickle.dumps(buffer_list)
            start = 0
            end = WINDOW_SIZE
            content = file[start:end]

            while content:

                soc.send(content)
                start += WINDOW_SIZE
                end += WINDOW_SIZE
                content = file[start:end]

            print("Sent", len(buffer_list))
            buffer_list= []

            # Close socket
            soc.close()



def GrayScale(input_image):
    """
    Converts a colored image to gray-scale
    :param input_image: input will be a numpy array of colored image
    :return:
    """

    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    return gray_image


if __name__ == "__main__":
    client()
