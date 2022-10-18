
line = b'1.0.0 69 boo\r\nplaceholder\r\n\r\n'
b = 0

def test_parse_status_line():
    s = parse_status_line(b'1.0.0 69 boo')
    if s[0] != '1.0.0':
        return False
    if s[1] != 69:
        return False
    if s[2] != 'boo':
        return False
    return True
    

def test_read_line():
    global b
    l = read_line(None)
    if l != b'1.0.0 69 boo':
        return False
    b = 0
    return True


def test_next_bytes():
    global b
    b1 = next_bytes(None, 1)
    if b1 != b'1':
        return False
    b2 = next_bytes(None, 2)
    if b2 != b'.0':
        return False
    b3 = next_bytes(None, 2)
    if b3 != b'.0':
        return False
    b = 0
    return True


def test_read_header():
    h = read_header(None)
    if h[0] != '1.0.0':
        return False
    if h[1] != 69:
        return False
    if h[2] != 'boo':
        return False
    if h[3]['uri-host'] != 'foo.com':
        return False
    return True


def main():
    if not test_next_bytes():
        print('failed next_bytes')
    elif not test_read_line():
        print('failed read_line')
    elif not test_parse_status_line():
        print('failed parse_status_line')
    elif not test_read_header():
        print('failed read_header')
    else:
        print('DONE')


def next_bytes(data_socket, n_bytes=1):
    global b
    """
    Read the next n bytes from the socket data_socket.

    Read the next n bytes from the sender, received over the network.
    If the bytes have not yet arrived, this method blocks (waits)
        until the bytes arrive.
    If the sender is done sending and is waiting for your response, this method blocks indefinitely.

    :param: data_socket: The socket to read from. The data_socket argument should be an open tcp
                    data connection (either a client socket or a server data socket), not a tcp
                    server's listening socket.
    :param: n_bytes: The number of bytes returned by the method.
    :return: the next n bytes, as a bytes object with multiple bytes in it
    :author: Lucas Peterson
    """
    i = 0
    l = b''
    while i < n_bytes:
        l = l + int.to_bytes(line[b], 1, 'big')
        b += 1
        i += 1
    return l


def read_header(data_socket):
    """
    Reads header of HTTP response.

    :param: data_socket: The socket to read from. The data_socket argument should be an open tcp data connection (
    either a client socket or a server data socket), not a tcp server's listening socket.]
    :return: tuple containing the version, status code, status message, and a dictionary of all key value pairs read in
    the header.
    :author: Lucas Peterson
    """
    status = parse_status_line(read_line(data_socket))
    key_values = dict()
    line = read_line(data_socket)
    while len(line) > 0:
        pair = parse_key_value(line)
        key_values[pair[0]] = pair[1]
        line = read_line(data_socket)

    status_code = status[1]
    if 'uri-host' not in key_values.keys():
        status_code = 400 # (Bad Request)

    return status[0], status_code, status[2], key_values


def read_line(data_socket):
    """
    Reads bytes in line until a CRLF is hit

    :param: data_socket: The socket to read from. The data_socket argument should be an open tcp
                    data connection (either a client socket or a server data socket), not a tcp
                    server's listening socket.]
    :returns: bytes object containing all bytes in the line except the CRLF
    :author: Lucas Peterson
    """
    byte = next_bytes(data_socket)
    next_byte = next_bytes(data_socket)
    line = bytes()
    while byte + next_byte != b'\x0d\x0a':
        line = line + byte
        byte = next_byte
        next_byte = next_bytes(data_socket)
    return line


def parse_status_line(line_bytes):
    """
    Reads the status line of the HTTP response.

    :param: line_bytes: The bytes within the line
    :returns: tuple containing the version, status code, and status message.
    :author: Lucas Peterson
    """
    line = line_bytes.decode('ascii').split(' ')
    return line[0], int(line[1]), line[2]


def parse_key_value(line_bytes):
    """
    Reads a key value line of the HTTP response.

    :param: line_bytes: The bytes within the line
    :returns: tuple containing the key and value.
    :author: Jack Rosenbecker
    """
    return 'uri-host', 'foo.com'

main()