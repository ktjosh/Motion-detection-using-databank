import socket
import pickle
import cv2

class databank:
    # Output is the shared buffer, table is the table of pointers

    __slots__ = "output", "flow_table", "id", "operator", "input"

    def __init__(self, id, operator=None):
        self.output = []
        self.input = []
        self.flow_table = {}
        self.id = id
        self.operator = operator

    def set_operator(self, operator):
        self.operator = operator

    def add_edge(self, nbr_databank):
        self.flow_table[nbr_databank.id] = nbr_databank

    def use_operator(self):
        self.output = self.operator(self.input)

    def server(self, file_name):

        WINDOW_SIZE = 1024
        PORT = 9000 + self.id

        # Received image will be stored in:
        # receivedImage = file_name
        # new_file = open(receivedImage, 'wb')

        # Open the server socket and bind it and listening for request
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSock.bind(('', PORT))
        serverSock.listen(10)

        while True:

            soc, addr = serverSock.accept()

            # On receiving the data, it is written to file
            content = soc.recv(WINDOW_SIZE)
            np_serial = bytearray()
            while content:
                np_serial.extend(content)
                content = soc.recv(WINDOW_SIZE)

            np_obj = pickle.loads(np_serial)
            print("RECEIVE COMPLETE")

            cv2.imshow("INPUT", np_obj)
            cv2.waitKey(1)
            ### SAVE np_obj in input

            # Close file and socket
            soc.close()

    def client(self, host, port, np_obj, host_id):

        WINDOW_SIZE = 1024
        HOST = host
        PORT = port + host_id

        # Define socket and connect to server
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((HOST, PORT))

        np_serial = pickle.dumps(np_obj)
        start = 0
        end = WINDOW_SIZE

        # Read bytes from file and send until the end of file
        content = np_serial[start:end]

        while content:
            soc.send(content)
            start += WINDOW_SIZE
            end += WINDOW_SIZE

            content = np_serial[start:end]

        print("SENDING COMPLETE")
        # Close file and socket
        soc.close()

