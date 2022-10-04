import socket
import time

"""
- NOTE: REPLACE 'N' Below with your section, year, and lab number
- CS2911 - 011
- Fall 2022
- Lab 2
- Names:
  - Jack Rosenbecker
  - Lucas Peterson

A simple TCP server/client pair.

The application protocol is a simple format: For each file uploaded, the client first sends four (big-endian) bytes indicating the number of lines as an unsigned binary number.

The client then sends each of the lines, terminated only by '\\n' (an ASCII LF byte).

The server responds with 'A' when it accepts the file.

Then the client can send the next file.


Introduction: (Describe the lab in your own words)
In this lab we're taking a protocol and creating a TCP server which follows that protocol for a given client.



Summary: (Summarize your experience with the lab, what you learned, what you liked, what you disliked, and any suggestions you have for improvement)
Creating and utilizing a network protocol is super fun. It's awesome to see the logic you built for communications
come together and work. I didn't like having to use your code but I understand why it was done, to make sure the
standard was met, it's an easy way to make sure your code is working. Personally I would either change the fact that
we use your code, or include it in the introduction as we had to change the way our functions worked once we learned
about the tcp_receive() function.
"""

# Port number definitions
# (May have to be adjusted if they collide with ports in use by other programs/services.)
TCP_PORT = 12100

# Address to listen on when acting as server.
# The address '' means accept any connection for our 'receive' port from any network interface
# on this system (including 'localhost' loopback connection).
LISTEN_ON_INTERFACE = ''

# Address of the 'other' ('server') host that should be connected to for 'send' operations.
# When connecting on one system, use 'localhost'
# When 'sending' to another system, use its IP address (or DNS name if it has one)
# OTHER_HOST = '155.92.x.x'
OTHER_HOST = 'localhost'


def main():
    """
    Allows user to either send or receive bytes
    """
    # Get chosen operation from the user.
    action = input('Select "(1-TS) tcpsend", or "(2-TR) tcpreceive":')
    # Execute the chosen operation.
    if action in ['1', 'TS', 'ts', 'tcpsend']:
        tcp_send(OTHER_HOST, TCP_PORT)
    elif action in ['2', 'TR', 'tr', 'tcpreceive']:
        tcp_receive(TCP_PORT)
    else:
        print('Unknown action: "{0}"'.format(action))


def tcp_send(server_host, server_port):
    """
    - Send multiple messages over a TCP connection to a designated host/port
    - Receive a one-character response from the 'server'
    - Print the received response
    - Close the socket

    :param: str server_host: name of the server host machine
    :param: int server_port: port number on server to send to
    """
    print('tcp_send: dst_host="{0}", dst_port={1}'.format(server_host, server_port))
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((server_host, server_port))

    num_lines = int(input('Enter the number of lines you want to send (0 to exit):'))

    while num_lines != 0:
        print('Now enter all the lines of your message')
        # This client code does not completely conform to the specification.
        #
        # In it, I only pack one byte of the range, limiting the number of lines this
        # client can send.
        #
        # While writing tcp_receive, you will need to use a different approach to unpack to meet the specification.
        #
        # Feel free to upgrade this code to handle a higher number of lines, too.
        tcp_socket.sendall(b'\x00\x00')
        time.sleep(1)  # Just to mess with your servers. :-)
        tcp_socket.sendall(b'\x00' + bytes((num_lines,)))

        # Enter the lines of the message. Each line will be sent as it is entered.
        for line_num in range(0, num_lines):
            line = input('')
            tcp_socket.sendall(line.encode() + b'\n')

        print('Done sending. Awaiting reply.')
        response = tcp_socket.recv(1)
        if response == b'A':  # Note: == in Python is like .equals in Java
            print('File accepted.')
        else:
            print('Unexpected response:', response)

        num_lines = int(input('Enter the number of lines you want to send (0 to exit):'))

    tcp_socket.sendall(b'\x00\x00')
    time.sleep(1)  # Just to mess with your servers. :-)  Your code should work with this line here.
    tcp_socket.sendall(b'\x00\x00')
    response = tcp_socket.recv(1)
    if response == b'Q':  # Reminder: == in Python is like .equals in Java
        print('Server closing connection, as expected.')
    else:
        print('Unexpected response:', response)

    tcp_socket.close()


def tcp_receive(listen_port):
    """
    Author: Jack
    - Listen for a TCP connection on a designated "listening" port
    - Accept the connection, creating a connection socket
    - Print the address and port of the sender
    - Repeat until a zero-length message is received:
      - Receive a message, saving it to a text-file (1.txt for first file, 2.txt for second file, etc.)
      - Send a single-character response 'A' to indicate that the upload was accepted.
    - Send a 'Q' to indicate a zero-length message was received.
    - Close data connection.

    :param: int listen_port: Port number on the server to listen on
    """

    print('tcp_receive (server): listen_port={0}'.format(listen_port))

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('', listen_port))

    tcp_socket.listen(1)
    (data_socket, sender_address) = tcp_socket.accept()
    print('tcp_receive: Sender connected={0}:{1}'.format(sender_address[0], sender_address[1]))

    listen_loop(data_socket)

    print('tcp_receive: Connection closed={0}:{1}'.format(sender_address[0], sender_address[1]))
    data_socket.sendall(b'Q')
    data_socket.close()
    tcp_socket.close()

def read_body(data_socket) -> str:
    """
    Author: Lucas
    Reads in the body of the message based on the number of lines given by reading an int from stream.
    Uses read_int()
    Depends on read_line().
    :return: The body of the message in ASCII encoding.
    """
    lines = read_int(data_socket)
    body = ''
    for line in range(lines):
        body += read_line(data_socket)
    return body


def read_line(data_socket) -> str:
    """
    Author: Lucas
    Reads message data from a Tcp stream until a new line character is hit.
    :return: An ascii string
    """
    line = ''
    byte = b'\x00'
    while byte != b'\x0a':
        byte = next_byte(data_socket)
        line += byte.decode('ascii')
    return line


def listen_loop(data_socket):
    """
    Author: Lucas
    Begins listening for a message.
    Uses read_body() and dump_text_to_file().
    Outputs every message received as its own file with a number next to it for the message number.
    """
    n_files = 0
    while True:
        body = read_body(data_socket)

        if body != '':
            dump_text_to_file(str(n_files), body)
            n_files += 1
            data_socket.sendall(b'A')
        else:
            break


def read_int(data_socket) -> int:
    """
    Author: Lucas
    Read the next 4-byte integer from the file
    Raise an error if the file is not set or has no more data
    """
    hex_str = ''
    for i in range(4):
        byte = hex(int.from_bytes(next_byte(data_socket), 'big')).removeprefix('0x')
        if len(byte) % 2 == 1:
            byte = '0' + byte
        hex_str += byte
    return int.from_bytes(bytes.fromhex(hex_str), 'big')


def read_body(data_socket) -> str:
    """
    Author: Lucas
    Reads in the body of the message based on the number of lines given by reading an int from stream.
    Uses read_int()
    Depends on read_line().
    :return: The body of the message in ASCII encoding.
    """
    lines = read_int(data_socket)
    body = ''
    for line in range(lines):
        body += read_line(data_socket)
    return body


def dump_text_to_file(name, txt):
    """
    Author: Jack
    Dumps an ascii string to a text file.
    Names the file with the given name automatically adds the correct extension.
    Will overwrite any files with the same name.
    """
    with open(name+".txt", 'w') as f:
        f.write(txt)


def next_byte(data_socket):
    """
    Read the next byte from the socket data_socket.

    Read the next byte from the sender, received over the network.
    If the byte has not yet arrived, this method blocks (waits)
      until the byte arrives.
    If the sender is done sending and is waiting for your response, this method blocks indefinitely.

    :param: data_socket: The socket to read from. The data_socket argument should be an open tcp
                        data connection (either a client socket or a server data socket), not a tcp
                        server's listening socket.
    :return: the next byte, as a bytes object with a single byte in it
    """
    return data_socket.recv(1)


# Invoke the main method to run the program.
main()
