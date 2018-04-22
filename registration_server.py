import pickle
import socket


def main():
    """
    main function that reads the toplogy of all the nodes int the system.
    once topology is read, it sends the information about the neighbors, their IP address, number of incomig an
    outgoing edge information to each node as it connects to the registration server.
    :return:
    """

    print("My IP:", socket.gethostbyname(socket.gethostname()))
    graph = {}
    nodes = set()
    file = open("input.txt")

    content = file.readline()
    first_line = content.split()
    operator_no = int(first_line[0])
    connections = int(first_line[1])

    operator = {}

    # For each line, store the operator of the node
    for _ in range(operator_no):
        content = file.readline()
        lst = content.strip().split()
        operator[lst[0]] = lst[1]

    # For each line, store the neighbors of the node
    for _ in range(connections):
        content = file.readline()
        lst = content.strip().split()

        if lst[0] not in graph:
            nodes.add(lst[0])
            graph[lst[0]] = []

        for i in range(1, len(lst)):
            nodes.add(lst[i])
            graph[lst[0]].append(lst[i])

    incoming_count = {}

    # For each line, store the count of incoming edges of the node
    for _ in range(int(operator_no)):
        content = file.readline()
        lst = content.strip().split()

        incoming_count[lst[0]] = lst[1]

    print(graph, operator, incoming_count)

    # create server socket, bind it and listen for connections
    PORT = 2000
    WINDOW_SIZE = 1024
    server_sock = socket.socket()
    server_sock.bind(("", PORT))
    server_sock.listen(10)

    # a dictionary is generated to map each id of the node to its corresponding ip address.
    id2ip = {}

    # the loop is run until all the nodes have connected and sent information
    while True:
        soc, addr = server_sock.accept()

        # id of each node will be receieved here.
        received = soc.recv(WINDOW_SIZE)
        received_id = received.decode("utf-8")

        print(received_id, "connected")
        id2ip[received_id] = addr
        nodes.remove(received_id)

        # send the neighbor id
        if received_id not in graph:
            nbr_to_node = []
        else:
            nbr_to_node = graph[received_id]

        operator_to_node = operator[received_id]
        in_edge_to_node = incoming_count[received_id]

        soc.sendall(
            pickle.dumps((nbr_to_node, operator_to_node, in_edge_to_node)))
        soc.close()


        if len(nodes) == 0:
            break

    print(id2ip)
    RECEIVE_PORT = 10000

    # once all the nodes are connected and all the ips are receieved, each node will be sent all the necessary
    # information
    for id in id2ip:
        addr = id2ip[id][0]
        soc1 = socket.socket()
        soc1.connect((addr, RECEIVE_PORT + int(id)))
        nbr_addr_lst = []

        if id in graph:
            for item in graph[id]:
                nbr_addr_lst.append(id2ip[item][0])

        # Send the neighbor address to the node
        soc1.sendall(pickle.dumps(nbr_addr_lst))
        print(nbr_addr_lst, "sent to", id)
        soc1.close()

    server_sock.close()
    file.close()


if __name__ == "__main__":
    main()
