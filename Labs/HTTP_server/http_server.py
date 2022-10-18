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

from email import message
import re
import socket
import threading
import os
import mimetypes
import datetime
from typing import Dict

HTTP_TEMPLATE = "HTTP/{version} {response_code} {message}\r\n" \
                "Date: {date}\r\n" \
                "Content-Length: {length}\r\n" \
                "Connection: {connection}\r\n" \
                "Content-Type: {content_type}\r\n\r\n"


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
    except:
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
    try:
        req = request(request_socket)
        res = response(req)
        res.send(request_socket, req.resource)
    except:
        print("HTTP server exiting . . .")
        print('threads: ', threading.enumerate())

    request_socket.close()
    


# Utility functions
# You may use these functions to simplify your code.


class request:
    """
    Constructor reads a request header from a socket, and stores its context as the type, resource, version,
    and headers (key values) instance variables.

    :author: Lucas Peterson
    """

    def __init__(self, request_socket: socket):
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
        line_bytes = self.read_line(request_socket)
        request = self.parse_request_line(line_bytes)
        self.headers = dict()
        line = self.read_line(request_socket)
        while len(line) > 0:
            pair = self.parse_key_value(line)
            self.headers[pair[0]] = pair[1]
            line = self.read_line(request_socket)

        self.type = request[0]
        self.resource = request[1].removeprefix('/')
        self.version = request[2].split('/')[1]

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

    def parse_request_line(self, line_bytes):
        """
        Reads the status line of the HTTP response.

        :param line_bytes: The bytes within the line
        :returns: tuple containing the type, resource, and version.
        :author: Lucas Peterson
        """
        line = line_bytes.decode('ascii').split(' ')
        return line[0], line[1], line[2]

    def parse_key_value(self, line_bytes):
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
    return timestamp.encode("ascii")


class response:
    """
    Creates a server response based on a clients request. Once the response is created
    it can be sent to the client using the send() method.

    :authors: Lucas Peterson, Kade Swenson, and Jack Rosenbecker
    """

    def __init__(self, client_request: request):
        self.version = '1.1'
        status_tuple = self.get_status(client_request)
        self.status_code = status_tuple[0]
        self.status = status_tuple[1]
        self.headers = self.add_headers(client_request)

    def get_status(self, client_request: request) -> tuple:
        """
        :author: Kade Swenson
        """
        if client_request.version != "1.1":
            return 400, 'Bad Request'
        if get_file_size(client_request.resource) is None:
            return 404, 'Not Found'
        return 200, 'Okay'

    def add_headers(self, client_request: request) -> Dict:
        """
        :author: Kade Swenson
        """
        headers = dict()
        headers['Date'] = get_time()
        headers['Connection'] = "close"
        headers['Content-Type'] = get_mime_type(client_request.resource)
        headers['Content-Length'] = get_file_size(client_request.resource)
        return headers

    def send(self, server_socket: socket, resource: str):
        """
        Creates an HTTP header plus body and sends it to the connected address.

        :param server_socket: The socket handling our current connection.
        :param resource: The requested resource from the client.
        :author: Jack Rosenbecker
        """
        headers = self.headers
        if len(headers) == 0:
            raise Exception(
                "Response must have its headers setup before it can send. Make sure you call add_headers() before send.")

        print(f"Serving resource \'{resource}\'")

        header_str = HTTP_TEMPLATE.format(
            version=self.version,
            response_code=self.status_code,
            message=self.status,
            date=headers['Date'],
            length=headers['Content-Length'],
            connection=headers['Connection'],
            content_type=headers['Content-Type']
        )

        header_bin = header_str.encode('ascii')
        server_socket.send(header_bin)
        file_bytes = bytes()

        if self.status_code == 200:
            file_bytes = get_file_bytes(resource)
        else:
            print(f"Requested resource: \'{resource}\', not found at expected location: {os.path.abspath(resource)}")

        server_socket.send(file_bytes)  # Resource data
        server_socket.send('\r\n\r\n'.encode('ascii'))  # End of stream


def get_mime_type(file_path: str):
    """
    Try to guess the MIME type of a file (resource), given its path (primarily its file extension)

    :param file_path: string containing path to (resource) file, such as './abc.html'
    :return: If successful in guessing the MIME type, a string representing the content type, such as 'text/html'
             Otherwise, None
    :rtype: str or None
    """
    abs_file_path = os.path.abspath(file_path)

    mime_type_and_encoding = mimetypes.guess_type(abs_file_path)
    mime_type = mime_type_and_encoding[0]
    return mime_type


def get_file_size(file_path: str):
    """
    Try to get the size of a file (resource) as number of bytes, given its path

    :param file_path: string containing path to (resource) file, such as './abc.html'
    :return: If file_path designates a normal file, an integer value representing the the file size in bytes
             Otherwise (no such file, or path is not a file), None
    :rtype: int or None
    """

    # Initially, assume file does not exist
    file_size = None
    abs_file_path = os.path.abspath(file_path)

    if os.path.isfile(abs_file_path):
        file_size = os.stat(abs_file_path).st_size
    return file_size


def get_file_bytes(file_path: str) -> bytes:
    """
    Get a file from the given path and return its bytes.

    :param file_path: Relative file path string.
    :return: The bytes of the given file.
    """
    abs_file_path = os.path.abspath(file_path)
    size = get_file_size(file_path)

    file = open(abs_file_path, "rb")
    return file.read(size)


main()

# Replace this line with your comments on the lab
