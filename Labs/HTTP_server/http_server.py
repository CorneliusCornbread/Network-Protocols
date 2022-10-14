"""
- NOTE: REPLACE 'N' Below with your section, year, and lab number
- CS2911 - 0NN
- Fall 2022
- Lab 4
- Names:
  - Lucas Peterson
  - Jack Rosenbecker
  - Kade Swenson

An HTTP server

Introduction: (Describe the lab in your own words)




Summary: (Summarize your experience with the lab, what you learned, what you liked,what you disliked, and any suggestions you have for improvement)





"""

import re
import socket
import threading
import os
import mimetypes
import datetime
from typing import Dict


def main():
    """ Start the server """
    http_server_setup(8080)


def http_server_setup(port):
    """
    Start the HTTP server
    - Open the listening socket
    - Accept connections and spawn processes to handle requests

    :param port: listening port number
    """

    num_connections = 10
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_address = ('', port)
    server_socket.bind(listen_address)
    server_socket.listen(num_connections)
    try:
        while True:
            request_socket, request_address = server_socket.accept()
            print('connection from {0} {1}'.format(request_address[0], request_address[1]))
            # Create a new thread, and set up the handle_request method and its argument (in a tuple)
            request_handler = threading.Thread(target=handle_request, args=(request_socket,))
            # Start the request handler thread.
            request_handler.start()
            # Just for information, display the running threads (including this main one)
            print('threads: ', threading.enumerate())
    # Set up so a Ctrl-C should terminate the server; this may have some problems on Windows
    except KeyboardInterrupt:
        print("HTTP server exiting . . .")
        print('threads: ', threading.enumerate())
        server_socket.close()


def handle_request(request_socket):
    """
    Handle a single HTTP request, running on a newly started thread.

    Closes request socket after sending response.

    Should include a response header indicating NO persistent connection

    :param request_socket: socket representing TCP connection from the HTTP client_socket
    :return: None
    :author: Lucas Peterson
    """
    req = request(request_socket)
    res = response(req)
    res.send(request_socket)


# Utility functions
# You may use these functions to simplify your code.


class request:
    """
    Constructor reads a request header from a socket, and stores its context as the type, resource, version,
    and headers (key values) instance variables.

    :author: Lucas Peterson
    """
    def __init__(self, request_socket : socket):
        self.read_header(request_socket)


    def next_bytes(self, request_socket, n_bytes=1):
        """
        Read the next n bytes from the socket data_socket.

        Read the next n bytes from the sender, received over the network.
        If the bytes have not yet arrived, this method blocks (waits)
            until the bytes arrive.
        If the sender is done sending and is waiting for your response, this method blocks indefinitely.

        :param: request_socket: The socket to read from. The request_socket argument should be an open tcp
            request connection (either a client socket or a server data socket), not a tcp server's
            listening socket.]
        :param: n_bytes: The number of bytes returned by the method.
        :return: the next n bytes, as a bytes object with multiple bytes in it
        :author: Lucas Peterson
        """
        n = 0
        message = b''
        while n < n_bytes:
            message += request_socket.recv(1)
            n += 1
        return message


    def read_header(self, request_socket):
        """
        Reads header of HTTP request and assigns values to request type, resource, version, and key values.

        :param request_socket: The socket to read from. The request_socket argument should be an open tcp
            request connection (either a client socket or a server data socket), not a tcp server's
            listening socket.]
        :author: Lucas Peterson
        """
        request = self.parse_request_line(self.read_line(request_socket))
        self.headers = dict()
        line = self.read_line(request_socket)
        while len(line) > 0:
            pair = self.parse_key_value(line)
            self.headers[pair[0]] = pair[1]
            line = self.read_line(request_socket)

        self.type = request[0]
        self.resource = request[1]
        self.version = request[2]


    def read_line(self, request_socket):
        """
        Reads bytes in line until a CRLF is hit

        :param request_socket: The socket to read from. The request_socket argument should be an open tcp
            request connection (either a client socket or a server data socket), not a tcp server's
            listening socket.]
        :returns: bytes object containing all bytes in the line except the CRLF
        :author: Lucas Peterson
        """
        byte = self.next_bytes(request_socket)
        next_byte = self.next_bytes(request_socket)
        line = bytes()
        while byte + next_byte != b'\x0d\x0a':
            line = line + byte
            byte = next_byte
            next_byte = self.next_bytes(request_socket)
        return line


    def parse_request_line(line_bytes):
        """
        Reads the status line of the HTTP response.

        :param line_bytes: The bytes within the line
        :returns: tuple containing the type, resource, and version.
        :author: Lucas Peterson
        """
        line = line_bytes.decode('ascii').split(' ')
        return line[0], line[1], line[2]


    def parse_key_value(line_bytes):
        """
        Reads a key value line of the HTTP request.

        :param line_bytes: The bytes within the line
        :returns: tuple containing the key and value.
        :author: Jack Rosenbecker
        """
        line_str = line_bytes.decode("ascii")
        line_list = line_str.split(":")

        return line_list[0], ''.join(line_list[1::])


def get_time():
    """
    :author: Kade Swenson
    """
    timestamp = datetime.datetime.utcnow()
    timestamp = timestamp.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return timestamp.encode("ASCII")


class response:
    """
    Creates a server response based on a clients request. Once the response is created
    it can be sent to the client using the send() method.

    :authors: Lucas Peterson, Kade Swenson, and Jack Rosenbecker
    """
    def __init__(self, client_request : request):
        self.version = '1.1'
        status_tuple = self.get_status(client_request)
        self.status_code = status_tuple[0]
        self.status = status_tuple[1]
        self.headers = self.add_headers(client_request)


    def get_status(self, client_request : request) -> tuple:
        """
        :author: Kade Swenson
        """
        # TODO Gets status code and status message based onb client request object.
        return 400, 'Bad Request'


    def add_headers(self, client_request : request) -> Dict:
        """
        :author: Kade Swenson
        """
        headers = dict()
        timestamp_in_bytes = get_time()
        return headers


    def send(self, server_socket):
        """
        :author: Jack Rosenbecker
        """
        # TODO Sends header bytes based on object variables.
        pass


def get_mime_type(file_path):
    """
    Try to guess the MIME type of a file (resource), given its path (primarily its file extension)

    :param file_path: string containing path to (resource) file, such as './abc.html'
    :return: If successful in guessing the MIME type, a string representing the content type, such as 'text/html'
             Otherwise, None
    :rtype: int or None
    """

    mime_type_and_encoding = mimetypes.guess_type(file_path)
    mime_type = mime_type_and_encoding[0]
    return mime_type


def get_file_size(file_path):
    """
    Try to get the size of a file (resource) as number of bytes, given its path

    :param file_path: string containing path to (resource) file, such as './abc.html'
    :return: If file_path designates a normal file, an integer value representing the the file size in bytes
             Otherwise (no such file, or path is not a file), None
    :rtype: int or None
    """

    # Initially, assume file does not exist
    file_size = None
    if os.path.isfile(file_path):
        file_size = os.stat(file_path).st_size
    return file_size


main()

# Replace this line with your comments on the lab
