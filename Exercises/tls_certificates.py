import ssl
import pprint
import socket

HOSTNAME = 'faculty-web.msoe.edu'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

# Disable SSL Version 2 - SSLv2 considered harmful
# - https://www.rfc-editor.org/rfc/rfc6176
context.options |= ssl.OP_NO_SSLv2

# Disable SSL Version 3 - SSLv3 considered insecure to the POODLE attack
# - https://en.wikipedia.org/wiki/POODLE
context.options |= ssl.OP_NO_SSLv3

for s in dir(ssl):
    if s.startswith('PROTOCOL_'):
        print(s)

# Disable compression to prevent CRIME attacks (OpenSSL 1.0+)
# - https://en.wikipedia.org/wiki/CRIME
context.options |= ssl.OP_NO_COMPRESSION

# Verify certificates and host name in client mode
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True

# Use root CA certificates for server authentication
context.load_default_certs(ssl.Purpose.SERVER_AUTH)

ssl_socket = context.wrap_socket(sock, server_hostname=HOSTNAME)
ssl_socket.connect((HOSTNAME, 443))

print(pprint.pformat(ssl_socket.getpeercert()))