"""
- NOTE: REPLACE 'N' Below with your section, year, and lab number
- CS2911 - 0NN
- Fall 202N
- Lab N
- Names:
  - 
  - 

A Trivial File Transfer Protocol Server

Introduction: (Describe the lab in your own words)




Summary: (Summarize your experience with the lab, what you learned, what you liked,what you disliked, and any suggestions you have for improvement)





"""

"""
Complete the script:

1. Receive a request from the client
2. Parse the request and verify that it is a read request
3. Send the data blocks to the client one by one waiting for an acknowledgement after each data message
4. Don’t forget to handle error messages as well as acknowledgements for blocks that need to be 
retransmitted.
5. Close the socket after successfully receiving an acknowledgement for the last block
6. Cleanly exit the program

For this lab you will be writing the Python code for a TFTP server.

- TFTP uses User Datagram Protocol (UDP) as the transport layer, so you will need to use a DGRAM socket in 
your Python code.
- Your TFTP server must send and receive data on port 69.
- While TFTP supports both read and write requests, your TFTP server must only support read (GET) requests 
(see extra credit below for write requests)

The TFTP RFC defines 5 messages used by TFTP.

1. Read Request
2. Write Request
3. Data Message
4. Acknowledgement Message
5. Error Message

The first message that the server receives is a request (either a read or a write). Your server will only have 
to support read requests. The RFC defines a request as follows:

           2 bytes     string    1 byte     string   1 byte
            ------------------------------------------------
           | Opcode |  Filename  |   0  |    Mode    |   0  |
            ------------------------------------------------

Data blocks are sent to the client one at a time using a data message which is formatted as follows:

                   2 bytes     2 bytes      n bytes
                   ----------------------------------
                  | Opcode |   Block #  |   Data     |
                   ----------------------------------

Once the server sends the first data block to the client, it must wait for an acknowledgement. An acknowledgement 
is sent from the client using the following message format:

                         2 bytes     2 bytes
                         ---------------------
                        | Opcode |   Block #  |
                         ---------------------

Here is the format for an error message:

               2 bytes     2 bytes      string    1 byte
               -----------------------------------------
              | Opcode |  ErrorCode |   ErrMsg   |   0  |
               -----------------------------------------

The TFTP RFC defines a set of error codes and what they mean:

   Value     Meaning
   0         Not defined, see error message (if any).
   1         File not found.
   2         Access violation.
   3         Disk full or allocation exceeded.
   4         Illegal TFTP operation.
   5         Unknown transfer ID.
   6         File already exists.
   7         No such user.

There could be situations where the client sends an error to the server. If your script receives an error message 
from the client, print out the error code, print the error message, and quit.
"""


import socket
import os
import math

# Helpful constants used by TFTP
TFTP_PORT = 69
TFTP_BLOCK_SIZE = 512
MAX_UDP_PACKET_SIZE = 65536


def main():
    """
    Processes a single TFTP request
    """

    client_socket = socket_setup()

    print("Server is ready to receive a request")

    ####################################################
    # Your code starts here                            #
    #   Be sure to design and implement additional     #
    #   functions as needed                            #
    ####################################################




    ####################################################
    # Your code ends here                              #
    ####################################################

    client_socket.close()


def get_file_block_count(filename):
    """
    Determines the number of TFTP blocks for the given file
    :param filename: THe name of the file
    :return: The number of TFTP blocks for the file or -1 if the file does not exist
    """
    try:
        # Use the OS call to get the file size
        #   This function throws an exception if the file doesn't exist
        file_size = os.stat(filename).st_size
        return math.ceil(file_size / TFTP_BLOCK_SIZE)
    except:
        return -1


def get_file_block(filename, block_number):
    """
    Get the file block data for the given file and block number
    :param filename: The name of the file to read
    :param block_number: The block number (1 based)
    :return: The data contents (as a bytes object) of the file block
    """
    # Open the file for reading
    file = open(filename, 'rb')
    block_byte_offset = (block_number-1) * TFTP_BLOCK_SIZE
    file.seek(block_byte_offset)

    # Read and return the block
    block_data = file.read(TFTP_BLOCK_SIZE)
    file.close()
    return block_data


def put_file_block(filename, block_data, block_number):
    """
    Writes a block of data to the given file
    :param filename: The name of the file to save the block to
    :param block_data: The bytes object containing the block data
    :param block_number: The block number (1 based)
    :return: Nothing
    """
    # Try to create the file if it doesn't exist
    try:
        with open(filename, 'x') as f:
            pass
    except FileExistsError:
        pass

    # Open the file for updating
    file = open(filename, 'r+b')
    block_byte_offset = (block_number-1) * TFTP_BLOCK_SIZE
    file.seek(block_byte_offset)

    # Write and close the file
    file.write(block_data)
    file.close()


def socket_setup():
    """
    Sets up a UDP socket to listen on the TFTP port
    :return: The created socket
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', TFTP_PORT))
    return s


####################################################
# Write additional helper functions starting here  #
####################################################

def opcode(code):
    pass

main()
