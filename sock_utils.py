import socket as s, pickle, struct

#SOCKET CREATION UTILS

def gethostip():
    host = s.gethostname()
    host = s.gethostbyname(host)
    print "Host IP is * ", host

    return host

def create_tcp_server_socket(address, port, queue_size):
    """
    """
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        sock.bind((address, port))
        sock.listen(queue_size)
        print "** Started listening for connections on IP:",address," Port:",port

    except s.error as error:
        print "Failed to create sock: ", error
        exit(1)
    return sock



def create_tcp_client_socket(address, port):
    """
    """
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.connect((address, port))
        print "connected to ", address

    except s.error as error:
        print "Failed to create sock: ", error
        exit(1)

    return sock

#SOCKET CREATION UTILS

#MESSAGE PROCESSING UTILS

def serialize(item):
    """
    Serialize an item using pickle
    """
    msg_bytes= pickle.dumps(item,-1)
    return msg_bytes

def deserialize(item):
    """
    Deserialize an item using pickle
    """
    return pickle.loads(item)

def msg_length(item):
    """
    Get a serialized message size
    """
    return struct.pack('!i',len(item))

def size_unpack(size):
    return struct.unpack('!i',size)[0]


#MESSAGE PROCESSING UTILS

#SEND AND RECEVEIVE UTILS

def receive_all(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    try:
        data = ''
        while len(data) < n:
            print "Recv Packet: ", data
            packet = sock.recv(n - len(data))
            if not packet:
                return "None"

            data += packet
        return data
    except StandardError as e:
        print "Error receiving data from socket: ", e
        exit(1)

def serial_send(socket, item):
    "Serialize and send an item"
    #Serialization
    prepared = serialize(item)
    #Get item size
    itemsize = msg_length(prepared)
    #Send size
    socket.sendall(itemsize)
    #Send item
    socket.sendall(prepared)
