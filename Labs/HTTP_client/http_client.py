"""
- NOTE: REPLACE 'N' Below with your section, year, and lab number
- CS2911 - 0NN
- Fall 202N
- Lab N
- Names:
  - 
  - 

An HTTP client

Introduction: (Describe the lab in your own words)




Summary: (Summarize your experience with the lab, what you learned, what you liked,what you disliked, and any suggestions you have for improvement)





"""

import socket
import re
import ssl


def main():
    """
    Tests the client on a variety of resources
    """

    # These resource request should result in "Content-Length" data transfer
    get_http_resource('https://www.httpvshttps.com/check.png', 'check.png')

    # this resource request should result in "chunked" data transfer
    get_http_resource('https://www.httpvshttps.com/','index.html')

    # this resource request should result in "chunked" data transfer
    #get_http_resource('https://www.youtube.com/', 'youtube.html')

    # If you find fun examples of chunked or Content-Length pages, please share them with us!


def get_http_resource(url, file_name):
    """
    Get an HTTP resource from a server
           Parse the URL and call function to actually make the request.

    :param url: full URL of the resource to get
    :param file_name: name of file in which to store the retrieved resource

    (do not modify this function)
    """

    protocol = 'https'
    default_port = 443

    # Parse the URL into its component parts using a regular expression.
    if not url.startswith('https://'):
        print('Request URL must start with https://')
        return

    url_match = re.search(protocol + '://([^/:]*)(:\d*)?(/.*)', url)
    url_match_groups = url_match.groups() if url_match else []
    #    print 'url_match_groups=',url_match_groups
    if len(url_match_groups) == 3:
        host_name = url_match_groups[0]
        host_port = int(url_match_groups[1][1:]) if url_match_groups[1] else default_port
        host_resource = url_match_groups[2]
        print('host name = {0}, port = {1}, resource = {2}'.
              format(host_name, host_port, host_resource))
        status_string = do_http_exchange(host_name, host_port,
                                         host_resource, file_name)
        print('get_http_resource: URL="{0}", status="{1}"'.format(url, status_string))
    else:
        print('get_http_resource: URL parse failed, request not sent')


def setup_connection(host, port):
    """
    Sets up the TCP connection to the given host at the given port using HTTPS (TLS)
    :param str host: host name to connect to
    :param int port: port number for the connection
    :return: TCP socket

    (do not modify this function)
    """

    # Set up the TCP connection
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((host, port))

    # Wrap the socket in an SSL connection
    context = ssl.create_default_context()
    ssl_socket = context.wrap_socket(tcp_socket, server_hostname=host)
    tcp_socket.close()

    # Return the socket
    return ssl_socket


def do_http_exchange(host, port, resource, file_name):
    """
    Get an HTTP resource from a server

    :param str host: the ASCII domain name or IP address of the server machine (i.e., host) to connect to
    :param int port: port number to connect to on server host
    :param str resource: the ASCII path/name of resource to get. This is everything in the URL after the domain name,
           including the first /.
    :param file_name: string (str) containing name of file in which to store the retrieved resource
    :return: the status code
    :rtype: int
    :author: Jack Rosenbecker
    """

    # Setup the TCP connection
    tcp_socket = setup_connection(host, port)

    # Request the resource and write the data to the file

    # Don't forget to close the tcp_socket when finished
 
    return 500  # Replace this "server error" with the actual status code

# Define additional functions here as necessary
# Don't forget docstrings and :author: tags


def next_bytes(data_socket, n_bytes=1):
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
    return data_socket.recv(n_bytes)


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
    return status[0], status[1], status[2], key_values


def read_line(data_socket):
    """
    Reads bytes in line until a CRLF is hit

    :param: data_socket: The socket to read from. The data_socket argument should be an open tcp
                    data connection (either a client socket or a server data socket), not a tcp
                    server's listening socket.]
    :returns: bytes object containing all bytes in the line except the CRLF
    :author: Lucas Peterson
    """
    return bytes()


def parse_status_line(line_bytes):
    """
    Reads the status line of the HTTP response.

    :param: line_bytes: The bytes within the line
    :returns: tuple containing the version, status code, and status message.
    :author: Lucas Peterson
    """
    return '', 0, ''


def parse_key_value(line_bytes):
    """
    Reads a key value line of the HTTP response.

    :param: line_bytes: The bytes within the line
    :returns: tuple containing the key and value.
    :author: Jack Rosenbecker
    """
    return '', ''


def is_chunked(key_values):
    """
    Checks if response is chunked

    :param: key_values: The dictionary of key value pairs in the response header
    :returns: True if message is chunked, else False.
    :author: Jack Rosenbecker
    """
    return False


def get_content_length(key_values):
    """
    Gets the content length from key values

    :param: key_values: The dictionary of key value pairs in the response header
    :returns: The content length of the data.
    :author: Jack Rosenbecker
    """
    return 0


def read_body(data_socket, key_values):
    """
    Reads the body

    :param: data_socket: The socket to read from. The data_socket argument should be an open tcp
                    data connection (either a client socket or a server data socket), not a tcp
                    server's listening socket.]
    :returns: the data within the body.
    :author: Kade Swenson
    """
    message = b''
    if is_chunked(key_values):
        size = read_chunk_length(data_socket)
        while size > 0:
            message += next_bytes(data_socket, size)

            # This line throws away the carriage return line feed at the end of data
            next_bytes(data_socket, 2)
            size = read_chunk_length(data_socket)
    else:
        message = next_bytes(data_socket, get_content_length(key_values))
    return message


def read_chunk_length(data_socket):
    """
    Reads the chunk length

    :param: data_socket: The socket to read from. The data_socket argument should be an open tcp
                    data connection (either a client socket or a server data socket), not a tcp
                    server's listening socket.]
    :returns: the length of the chunk
    :author: Kade Swenson
    """
    size_in_bytes = read_line(data_socket)
    size_in_text = size_in_bytes.decode("ASCII")
    size_in_int = int(size_in_text, 16)
    return size_in_int


def read_data(data_socket, content_length):
    """
    Reads the data within an entire message.

    :param: data_socket: The socket to read from. The data_socket argument should be an open tcp
                    data connection (either a client socket or a server data socket), not a tcp
                    server's listening socket.]
    :param: content_length: The number of bytes in the message
    :returns: data within the message.
    :author: Kade Swenson
    """

    # After talking with the group this function is not needed because read_body does the function of this



main()
