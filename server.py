import socket
import pickle
import cv2
import numpy as np


def server():
    PORT = 9000
    BUFFER_SIZE = 4096

    # Open the server socket and bind it and listening for request
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.bind(('', PORT))
    serverSock.listen(10)

    # To continously listen to new connections
    while True:
        print("Waiting for new connection")
        soc, addr = serverSock.accept()
        print("connection received")

        # On receiving the data, it is written to file

        try:

            # Not needed if sending the whole video in one go

            content = soc.recv(BUFFER_SIZE)
            by = bytearray()

            while content:
                by.extend(content)
                content = soc.recv(BUFFER_SIZE)

                if len(content) == 0:

                    img = pickle.loads(by)
                    print(len(img))
                    break

        except EOFError:
            print("EOFError")

        print("received")

        # Close file and socket
        soc.close()


if __name__ == "__main__":
    server()
