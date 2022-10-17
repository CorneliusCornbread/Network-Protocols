"""
- NOTE: REPLACE 'N' Below with your section, year, and lab number
- CS2911 - 0NN
- Fall 202N
- Lab N
- Names:
  - 
  - 

An HTTP server

Introduction: (Describe the lab in your own words)




Summary: (Summarize your experience with the lab, what you learned, what you liked,what you disliked, and any suggestions you have for improvement)





"""

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
    # TODO Create request object, creates a response object and gives it the request. Sends the response to client.
    pass  # Replace this line with your code


# ** Do not modify code below this line.  You should add additional helper methods above this line.

# Utility functions
# You may use these functions to simplify your code.


class request:
    """
    :author: Lucas Peterson
    """
    def __init__(self, request_socket):
        """
        :author: Lucas Peterson
        """
        header = self.read_header(request_socket)
        self.type : str = header[0]
        self.resource : str = header[1]
        self.version : str = header[2]
        self.headers : Dict = header[3]


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
        return request_socket.recv(n_bytes)


    def read_header(self, request_socket):
        """
        Reads header of HTTP request.

        :param: request_socket: The socket to read from. The request_socket argument should be an open tcp
            request connection (either a client socket or a server data socket), not a tcp server's
            listening socket.]
        :return: tuple containing the version, status code, status message, and a dictionary of all key value pairs read in
        the header.
        :author: Lucas Peterson
        """
        status = self.parse_status_line(read_line(request_socket))
        key_values = dict()
        line = self.read_line(request_socket)
        while len(line) > 0:
            pair = self.parse_key_value(line)
            key_values[pair[0]] = pair[1]
            line = self.read_line(request_socket)

        status_code = status[1]
        if 'uri-host' not in key_values.keys():
            status_code = 400 # (Bad Request)

        return status[0], status_code, status[2], key_values


    def read_line(self, request_socket):
        """
        Reads bytes in line until a CRLF is hit

        :param: request_socket: The socket to read from. The request_socket argument should be an open tcp
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

        :param: line_bytes: The bytes within the line
        :returns: tuple containing the version, status code, and status message.
        :author: Lucas Peterson
        """
        line = line_bytes.decode('ascii').split(' ')
        return line[0], int(line[1]), line[2]


    def parse_resource_line(line_bytes):
        """
        Reads the resource line of the HTTP response.

        :param: line_bytes: The bytes within the line
        :returns: tuple containing the type, resource, and version.
        :author: Lucas Peterson
        """
        line = line_bytes.decode('ascii').split(' ')
        return line[0], line[1], line[2]


    def parse_key_value(line_bytes):
        """
        Reads a key value line of the HTTP request.
        :param: line_bytes: The bytes within the line
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
    :authors: Lucas Peterson, Kade Swenson, and Jack Rosenbecker
    """
    def __init__(self, client_request : request):
        """
        :authors: Lucas Peterson
        """
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
        if client_request.version != "1.1":
            return 400, 'Bad Request'
        if get_file_size("." + client_request.resource) is None:
            return 404, 'Not Found'
        return 200, 'Okay'

    def add_headers(self, client_request : request) -> Dict:
        """
        :author: Kade Swenson
        """
        headers = dict()
        headers['Date'] = get_time()
        headers['Connection'] = "close"
        headers['Content-Type'] = get_mime_type("." + client_request.resource)
        headers['Content-Length'] = get_file_size("." + client_request.resource)
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
    :rtype: str or None
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
