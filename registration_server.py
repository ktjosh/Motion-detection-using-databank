import socket
import pickle

def main():

    graph = {}
    nodes = set()
    file = open("input.txt")

    content = file.readline()
    first_line = content.split()
    operator_no = first_line[0]
    connections = first_line[1]

    operator ={}
    for _ in range(int(operator_no)):
        content = file.readline()
        lst = content.split()

        operator[lst[0]] = lst[1]

    for _ in range(int(connections)):
        content = file.readline()
        lst = content.split()

        if lst[0] not in graph:
            nodes.add(lst[0])
            graph[lst[0]] = []

        for i in range(1,len(lst)):
            nodes.add(lst[i])
            graph[lst[0]].append(lst[i])

    print(graph, operator)

    PORT = 2000
    WINDOW_SIZE = 1024
    server_sock = socket.socket()
    server_sock.bind(("", PORT))
    server_sock.listen(10)

    id2ip = {}
    while True:
        soc, addr = server_sock.accept()
        received = soc.recv(WINDOW_SIZE)
        received_id = received.decode("utf-8")
        id2ip[received_id] = addr
        nodes.remove(received_id)
        if received_id not in graph:
            temp = pickle.dumps([])
        else:
            temp = pickle.dumps(graph[received_id])
        soc.sendall(temp)
        soc.sendall(pickle.dumps(operator[received_id]))
        soc.close()

        if len(nodes)==0:
            break

    print(id2ip)
    RECEIVE_PORT = 10000
    for id in id2ip:
        addr = id2ip[id][0]
        soc1 = socket.socket()
        soc1.connect((addr,RECEIVE_PORT + int(id)))
        nbr_addr_lst = []

        if id in graph:
            for item in graph[id]:
                nbr_addr_lst.append(id2ip[item][0])

        data = pickle.dumps(nbr_addr_lst)
        soc1.sendall(data)
        print(nbr_addr_lst, "sent to", id)



if __name__ == "__main__":
    main()
