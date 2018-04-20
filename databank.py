import socket

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
        receivedImage = file_name
        new_file = open(receivedImage, 'wb')

        # Open the server socket and bind it and listening for request
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSock.bind(('', PORT))
        serverSock.listen(10)

        while True:

            soc, addr = serverSock.accept()

            # On receiving the data, it is written to file
            content = soc.recv(WINDOW_SIZE)
            while (content):
                new_file.write(content)
                content = soc.recv(WINDOW_SIZE)

            print("image created")

            # Close file and socket
            soc.close()
            new_file.close()

    def client(self, host, port, _name, host_id):

        WINDOW_SIZE = 1024
        HOST = host
        PORT = port + host_id
        file_name = _name

        # Open in 'b' because image reading in binary mode
        file = open(file_name, 'rb')

        # Define socket and connect to server
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((HOST, PORT))

        # Read bytes from file and send until the end of file
        content = file.read(WINDOW_SIZE)
        while content:
            soc.send(content)
            content = file.read(WINDOW_SIZE)

        # Close file and socket
        soc.close()
        file.close()
