import socket

def client():


    # ATTEMPT TO TRANSFER IMAGE

    WINDOW_SIZE = 1024
    HOST = "localhost"
    PORT = 9000

    file_name = "cat.png"

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


if __name__ == "__main__":
    client()