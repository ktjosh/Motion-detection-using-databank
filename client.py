import socket
import pickle
import cv2


def client():
    # ATTEMPT TO TRANSFER IMAGE

    HOST = "localhost"
    PORT = 9000
    BUFFER_SIZE = 4096

    # Define socket and connect to server
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((HOST, PORT))

    img_list = []

    path = "Experiment.mp4"
    vid = cv2.VideoCapture(path)

    while vid.isOpened():
        # frame by frame is read here
        _, frame = vid.read()
        try:
            if len(frame) > 0:
                gray_frame = GrayScale(frame)
                img_list.append(gray_frame)

        # Error encountered on the last frame: None is sent
        except TypeError:
            break

    print("Video Done", len(img_list))

    # Sending the imd_list to the server

    # If you want to send the whole img_lst
    image_serial = pickle.dumps(img_list)
    start = 0
    end = BUFFER_SIZE
    content = image_serial[start:end]

    while content:
        soc.send(content)
        start += BUFFER_SIZE
        end += BUFFER_SIZE
        content = image_serial[start:end]

    # # If you want send 10 images at a time
    # buffer_list = []
    #
    # for i in range(len(img_list)):
    #
    #     buffer_list.append(img_list[i])
    #     if (i+1) % 10 == 0:
    #         file = pickle.dumps(buffer_list)
    #         start = 0
    #         end = BUFFER_SIZE
    #         content = file[start:end]
    #         while content:
    #             i += 1
    #             print(i)
    #             soc.send(content)
    #             start += BUFFER_SIZE
    #             end += BUFFER_SIZE
    #             content = file[start:end]
    #     buffer_list= []
    #     exit(251)
    #
    # # Close file and socket
    # soc.close()


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
