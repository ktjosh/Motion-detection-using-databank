import pickle
import socket
from databank.py import *

import databank


def unit(lst=None):
    return lst


def main():
    HOST = "localhost"
    PORT = 2000

    # print("Enter host IP:")
    # HOST = input()

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

    node.set_operator(op)
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



if __name__ == "__main__":
    main()
