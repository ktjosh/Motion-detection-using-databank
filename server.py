import socket
import pickle
import cv2

def server():
    WINDOW_SIZE = 1024
    PORT = 9000

    # Received image will be stored in:
    receivedImage = "test.png"
    new_file = open(receivedImage,'wb')

    # Open the server socket and bind it and listening for request
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.bind(('', PORT))
    serverSock.listen(10)

    while True:

        soc, addr = serverSock.accept()

        # On receiving the data, it is written to file
        content = soc.recv(WINDOW_SIZE)
        by = bytearray()
        print(by)
        while (content):
            by.extend(content)
            content = soc.recv(WINDOW_SIZE)

        print("image created")
        by = pickle.loads(by)
        print(by)
        print(by.shape)

        # cv2.imshow("123454321",by)
        # cv2.waitKey(0)

        # Close file and socket
        soc.close()
        new_file.close()

if __name__ == "__main__":
    server()
