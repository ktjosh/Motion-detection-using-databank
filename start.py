import pickle
import socket
import cv2
import image_operations as img_op

import databank


def assign_operator(op):
    """
    Assign the operator based on its name
    :param op: name of operator
    :return: operator
    """
    if op == "capture":
        return img_op.VideoCapture
    if op == "grey_scale":
        return img_op.GrayScale
    if op == "binarize":
        return img_op.imBinarize
    if op == "display_len":
        return img_op.display_len
    if op == "bg_model":
        return  img_op.background_model
    if op == "subtraction_binarize":
        return img_op.Background_Subtraction_And_Binarize
    if op == "blob_detect":
        return img_op.Blob_Detection_and_Bounding_box


def main():
    """
    The main method.
    The databank object is assigned to the node
    The node waits for its data from other data, processes its data
    and sends the data

    :return: None
    """
    # HOST = input("Enter IP: ")
    HOST = "localhost"
    PORT = 2000

    id = input("Enter ID: ")
    node = databank.databank(id)

    soc = socket.socket()
    soc.connect((HOST, PORT))
    soc.send(bytes(id, "utf-8"))

    print(id, "sent to receiver")

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

    print("Neighbors:", neighbors)
    print("Neighbor IP", nbr_addr)

    node.receiver()
    print("Using operation:" + op)
    node.use_operator()

    # Send data to all neighbors
    if len(neighbors) != 0:
        for i in range(len(nbr_addr)):
            print("Sending data to", neighbors[i])
            node.sender(nbr_addr[i], int(neighbors[i]))

    # if node.id == '4':
    #     for frame in node.output:
    #         cv2.imshow('hey',frame)
    #         cv2.waitKey(2)


if __name__ == "__main__":
    main()
