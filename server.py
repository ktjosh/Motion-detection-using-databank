import socket
import pickle

import cv2
import numpy as np


def server():
    PORT = 9000
    WINDOW_SIZE = 4096

    # Open the server socket and bind it and listening for request
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.bind(('', PORT))
    serverSock.listen()

    # To continously listen to new connections

    source_data_dict = {}

    while True:

        print("**Waiting for new connection")
        soc, addr = serverSock.accept()
        print("connection received")

        # Receive the ID of the user
        id = pickle.loads(soc.recv(WINDOW_SIZE))

        if id not in source_data_dict:
            source_data_dict[id] = []

        try:

            content = soc.recv(WINDOW_SIZE)
            by = bytearray()

            while content:
                by.extend(content)
                content = soc.recv(WINDOW_SIZE)

                if len(content) == 0:

                    img_lst = pickle.loads(by)
                    source_data_dict[id].extend(img_lst)

                    break

        except EOFError:
            print("EOFError")

        print(len(source_data_dict[id]))
        print("\n")

        # Close file and socket
        soc.close()


if __name__ == "__main__":
    server()

