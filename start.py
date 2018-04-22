import pickle
import socket

import image_operations as img_op

import databank


def assign_operator(op):
    if op == "capture":
        return img_op.VideoCapture
    if op == "grey_scale":
        return img_op.GrayScale
    if op == "binarize":
        return img_op.imBinarize


def main():
    HOST = input("Enter IP: ")
    PORT = 2000

    print("Enter ID:")
    id = input()
    node = databank.databank(id)

    soc = socket.socket()
    soc.connect((HOST, PORT))
    soc.send(bytes(id, "utf-8"))

    print(id, "sent to server")

    # get the tuple of (nbr, operator, incoming_count)
    tuple = pickle.loads(soc.recv(2048))
    neighbors = tuple[0]
    op = tuple[1]
    incoming_count = int(tuple[2])

    # Set the operator of the node
    node.set_operator(assign_operator(op))

    # Set the incoming count of the node
    node.set_incoming_edges(incoming_count)

    soc.close()

    # Connection for getting the IP
    RECEIVE_PORT = 10000
    soc = socket.socket()

    soc.bind(('', RECEIVE_PORT + int(id)))
    soc.listen(5)

    soc_from_server, addr = soc.accept()
    nbr_addr = soc_from_server.recv(1024)
    nbr_addr = pickle.loads(nbr_addr)

    print(nbr_addr, "are my neighbors")

    node.server()
    node.use_operator()

    # Send data to ALL neighbors require FOR LOOP IN FUTURE
    if len(neighbors) != 0:
        print("Sending data to", neighbors[0])
        node.client(nbr_addr[0], int(neighbors[0]))

    # if node.id == '3':
    #     for frame in node.output:
    #         cv2.imshow('hey',frame)
    #         cv2.waitKey(1)

    """
    code to perform operations based on th
    """


if __name__ == "__main__":
    main()
