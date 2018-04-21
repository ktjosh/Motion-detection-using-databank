import pickle
import socket
import _thread
import databank
import image_operations as img_op

def assign_operator(op):

    if op == "capture":
        return img_op.VideoCapture
    if op == "grey_scale":
        return img_op.GrayScale
    if op == "binarize":
        return img_op.imBinarize


def main():
    HOST = "localhost"
    PORT = 2000

    print("Enter ID:")
    id = input()
    node = databank.databank(id)

    soc = socket.socket()
    soc.connect((HOST, PORT))
    soc.send(bytes(id, "utf-8"))

    print(id, "sent to server")

    neighbors = soc.recv(2048)
    neighbors = pickle.loads(neighbors)
    op = pickle.loads(soc.recv(2048))

    # Set the operator of the node
    node.set_operator(assign_operator(op))

    print(neighbors, "<- my neighbors")
    print(op, "<- operator")
    soc.close()

    # Connection for getting the IP
    RECEIVE_PORT = 10000
    soc = socket.socket()

    soc.bind(('',RECEIVE_PORT + int(id)))
    soc.listen(5)

    soc_from_server, addr = soc.accept()
    nbr_addr = soc_from_server.recv(1024)
    nbr_addr = pickle.loads(nbr_addr)

    print(nbr_addr, "are my neighbors")

    """
    code for creating thread server function in databank
    it will create a thread for server
    """
    if node.id != '1':

        _thread.start_new_thread(node.server,())

        # Wait for data to come
        while True:
            if node.trigger:
                print("WAITING")
                break

        node.use_operator()




    else:
        _capture = input("Should I capture the image? (y/n)")
        if _capture == 'y':
            node.use_operator()


    # Send data to neighbors
    if len(neighbors) != 0:
        print("Sending data to", neighbors[0])
        node.client("localhost",int(neighbors[0]))

    # TRIGGER CONDITION WHEN MET WILL
    # RESULT IN USE_UPERATOR AND SENDING THE OUTPUT








    """
    code to perform operations based on th
    """




if __name__ == "__main__":
    main()
