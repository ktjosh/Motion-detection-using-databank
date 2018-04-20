import socket
import pickle
import cv2
import numpy as np

def server():
    WINDOW_SIZE = 10240
    PORT = 9000
    Buffer_size = 4096

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
        i= 0
        while True:
            content = soc.recv(Buffer_size)
            # ws = pickle.loads(content)
            # print(ws)
            # content = soc.recv(ws+1)
            by = bytearray()
            # #print(by)
            word = "notdone"

            j=0
            while content:#word!="done":
                print(j)
                by.extend(content)
                content = soc.recv(Buffer_size)
                if (len(content)==0):
                    #print(j)
                    print("paap")
                    #exit(251)
                j+=1
                #word = pickle.loads(content)


            print(len(by))
            img = pickle.loads(by)
            i+=1
            print("image created", i)
            #print(by)
            print(img.shape)
            np.save('kt.npy',img)
            if i == 284:
                print("time to exit")
                exit(45)
            cv2.imshow("123454321",img)
            cv2.waitKey()
            print("received")
        # Close file and socket
        soc.close()
        new_file.close()

if __name__ == "__main__":
    server()
