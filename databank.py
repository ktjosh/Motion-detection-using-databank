import pickle
import socket


class databank:
    """
    The databank class is present at each node in the data-flow graph
    It is used to route the data to different nodes for processing

    output: The output buffer to be sent to the next node
    input: The dictionary containing key as the source node id and
            value as the output buffer of the source
    incoming_edge_count: Number of incoming edges into the node
    id: Node id
    operator: operator of the node
    """

    __slots__ = "output", "incoming_edge_count", "id", \
                "operator", "input"

    def __init__(self, id, operator=None):
        """
        The constructor of databank class
        :param id: Node id
        :param operator: Operator of databank class
        """

        self.output = []
        self.input = {}
        self.incoming_edge_count = {}
        self.id = id
        self.operator = operator

    def set_operator(self, operator):
        """
        Setting the operator of databank
        :param operator: operator to be set
        :return: None
        """
        self.operator = operator

    def set_incoming_edges(self, count):
        """
        Setting the incoming edges at the node of databank
        :param count: Count of incoming edges
        :return: None
        """
        self.incoming_edge_count = count

    def use_operator(self):
        """
        Apply the operator on the input to get the output
        :return: None
        """
        self.output = self.operator(self.input)

    def receiver(self):
        """
        The code to receive the buffer from the source node
        and save it in the input dictionary
        :return: None
        """

        WINDOW_SIZE = 4096
        PORT = 9000 + int(self.id)

        # Open the receiver socket and bind it and listening for request
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSock.bind(('', PORT))
        serverSock.listen(10)
        conn_count = 0

        while conn_count != self.incoming_edge_count:
            print("**Waiting for new connection")

            soc, addr = serverSock.accept()
            conn_count += 1

            # Receive the ID of the user
            id = pickle.loads(soc.recv(WINDOW_SIZE))
            print("Received connection from", id)

            if id not in self.input:
                self.input[id] = []
            try:

                content = soc.recv(WINDOW_SIZE)
                by = bytearray()

                while content:
                    by.extend(content)
                    content = soc.recv(WINDOW_SIZE)

                    if len(content) == 0:
                        img_lst = pickle.loads(by)
                        self.input[id].extend(img_lst)
                        break

            except EOFError:
                print("EOFError")

            print("Input received")

            # Close file and socket
            soc.close()

    def sender(self, host, host_id):
        """
        The code to send the output buffer to the host

        :param host: The id of the receiver
        :param host_id: The address of the receiver
        :return: None
        """

        WINDOW_SIZE = 4096
        port = 9000
        HOST = host
        PORT = port + int(host_id)

        # Get the length of your output buffer
        IMAGE_BURST = len(self.output)
        buffer_list = []

        for i in range(IMAGE_BURST + 1):

            if i != IMAGE_BURST:
                buffer_list.append(self.output[i])

            if (i + 1) % IMAGE_BURST == 0:  # or i == len(img_list):

                soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                soc.connect((HOST, PORT))

                # Send ID
                soc.send(pickle.dumps(self.id))

                # Send the Buffer
                np_serial = pickle.dumps(buffer_list)
                start = 0
                end = WINDOW_SIZE

                # Read bytes from file and send until the end of file
                content = np_serial[start:end]

                while content:
                    soc.send(content)
                    start += WINDOW_SIZE
                    end += WINDOW_SIZE
                    content = np_serial[start:end]
                buffer_list = []

                print("*Buffer Sent")

                # Close socket
                soc.close()
