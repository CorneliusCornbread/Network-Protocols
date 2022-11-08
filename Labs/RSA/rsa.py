"""
- NOTE: REPLACE 'N' Below with your section, year, and lab number
- CS2911 - 0NN
- Fall 202N
- Lab N
- Names:
  - Jack - Worked on simple functions
  - Lucas - Worked on complex math functions
  - Kade - Worked on questions and checksum

16-bit RSA

Introduction: (Describe the lab in your own words)





Question 1: RSA Security
In this lab, Trudy is able to find the private key from the public key. Why is this not a problem for RSA in practice?





Question 2: Critical Step(s)
When creating a key, Bob follows certain steps. Trudy follows other steps to break a key. What is the difference between Bob’s steps and Trudy’s so that Bob is able to run his steps on large numbers, but Trudy cannot run her steps on large numbers?




Checksum Activity:
Provide a discussion of your experiences as described in the activity.  Be sure to answer all questions.





Summary: (Summarize your experience with the lab, what you learned, what you liked,what you disliked, and any suggestions you have for improvement)





"""

# Use these named constants as you write your code
# To increase the key size add more 1's and 0's to these values
#   E.g. MAX_PRIME = 0b1111111111111111 <- 16 bits
#        MIN_PRIME = 0b1100000000000001 <- 16 bits


MAX_PRIME = 0b11111111  # The maximum value a prime number can have
MIN_PRIME = 0b11000001  # The minimum value a prime number can have 
PUBLIC_EXPONENT = 17  # The default public exponent


# ---------------------------------------
# Do not modify code below this line
# ---------------------------------------

def main():
    """ Provide the user with a variety of encryption-related actions """

    # Get chosen operation from the user.
    action = input("Select an option from the menu below:\n"
                   "(1-CK) create_keys\n"
                   "(2-CC) compute_checksum\n"
                   "(3-VC) verify_checksum\n"
                   "(4-EM) encrypt_message\n"
                   "(5-DM) decrypt_message\n"
                   "(6-BK) break_key\n "
                   "Please enter the option you want:\n")
    # Execute the chosen operation.
    if action in ['1', 'CK', 'ck', 'create_keys']:
        create_keys_interactive()
    elif action in ['2', 'CC', 'cc', 'compute_checksum']:
        compute_checksum_interactive()
    elif action in ['3', 'VC', 'vc', 'verify_checksum']:
        verify_checksum_interactive()
    elif action in ['4', 'EM', 'em', 'encrypt_message']:
        encrypt_message_interactive()
    elif action in ['5', 'DM', 'dm', 'decrypt_message']:
        decrypt_message_interactive()
    elif action in ['6', 'BK', 'bk', 'break_key']:
        break_key_interactive()
    else:
        print("Unknown action: '{0}'".format(action))


def create_keys_interactive():
    """
    Create new public keys

    :return: the private key (d, n) for use by other interactive methods
    """

    key_pair = create_keys()
    public_key = get_public_key(key_pair)
    private_key = get_private_key(key_pair)
    print("Public key: ")
    print(public_key)
    print("Private key: ")
    print(private_key)
    return private_key


def get_public_key(key_pair):
    """
    Pulls the public key out of the tuple structure created by
    create_keys()

    :param key_pair: (e,d,n)
    :return: (e,n)
    """

    return key_pair[0], key_pair[2]


def get_private_key(key_pair):
    """
    Pulls the private key out of the tuple structure created by
    create_keys()

    :param key_pair: (e,d,n)
    :return: (d,n)
    """

    return key_pair[1], key_pair[2]


def compute_checksum_interactive():
    """
    Compute the checksum for a message, and encrypt it
    """

    private_key = create_keys_interactive()

    message = input('Please enter the message to be checksummed: ')

    hash_code = compute_checksum(message)
    print('Hash:', format_as_hex(hash_code))
    cipher = apply_key(private_key, hash_code)
    print('Encrypted Hash:', format_as_hex(cipher))


def verify_checksum_interactive():
    """
    Verify a message with its checksum, interactively
    """

    public_key = enter_public_key_interactive()
    message = input('Please enter the message to be verified: ')
    recomputed_hash = compute_checksum(message)

    string_hash = input('Please enter the encrypted hash (in hexadecimal): ')
    encrypted_hash = int(string_hash, 16)
    decrypted_hash = apply_key(public_key, encrypted_hash)
    print('Recomputed hash:', format_as_hex(recomputed_hash))
    print('Decrypted hash: ', format_as_hex(decrypted_hash))
    if recomputed_hash == decrypted_hash:
        print('Hashes match -- message is verified')
    else:
        print('Hashes do not match -- has tampering occurred?')


def encrypt_message_interactive():
    """
    Encrypt a message
    """

    message = input('Please enter the message to be encrypted: ')
    public_key = enter_public_key_interactive()
    encrypted = ''
    for c in message:
        encrypted += format_as_hex(apply_key(public_key, ord(c)))
    print("Encrypted message:", encrypted)


def decrypt_message_interactive(private_key = None):
    """
    Decrypt a message
    """

    encrypted = input('Please enter the message to be decrypted: ')
    if private_key is None:
        private_key = enter_key_interactive('private')
    message = ''
    hex_length = get_hex_digits()
    for i in range(0, len(encrypted), hex_length):
        enc_string = encrypted[i:i + hex_length]
        enc = int(enc_string, 16)
        dec = apply_key(private_key, enc)
        if dec >= 0 and dec < 256:
            message += chr(dec)
        else:
            print('Warning: Could not decode encrypted entity: ' + enc_string)
            print('         decrypted as: ' + str(dec) + ' which is out of range.')
            print('         inserting _ at position of this character')
            message += '_'
    print("Decrypted message:", message)


def break_key_interactive():
    """
    Break key, interactively
    """

    public_key = enter_public_key_interactive()
    private_key = break_key(public_key)
    print("Private key:")
    print(private_key)
    decrypt_message_interactive(private_key)


def enter_public_key_interactive():
    """
    Prompt user to enter the public modulus.

    :return: the tuple (e,n)
    """

    print('(Using public exponent = ' + str(PUBLIC_EXPONENT) + ')')
    string_modulus = input('Please enter the modulus (decimal): ')
    modulus = int(string_modulus)
    return PUBLIC_EXPONENT, modulus


def enter_key_interactive(key_type):
    """
    Prompt user to enter the exponent and modulus of a key

    :param key_type: either the string 'public' or 'private' -- used to prompt the user on how
                     this key is interpreted by the program.
    :return: the tuple (e,n)
    """
    string_exponent = input('Please enter the ' + key_type + ' exponent (decimal): ')
    exponent = int(string_exponent)
    string_modulus = input('Please enter the modulus (decimal): ')
    modulus = int(string_modulus)
    return exponent, modulus


def compute_checksum(string):
    """
    Compute simple hash

    Given a string, compute a simple hash as the sum of characters
    in the string.

    (If the sum goes over sixteen bits, the numbers should "wrap around"
    back into a sixteen bit number.  e.g. 0x3E6A7 should "wrap around" to
    0xE6A7)

    This checksum is similar to the internet checksum used in UDP and TCP
    packets, but it is a two's complement sum rather than a one's
    complement sum.

    :param str string: The string to hash
    :return: the checksum as an integer
    """

    total = 0
    for c in string:
        total += ord(c)
    total %= 0x8000  # Guarantees checksum is only 4 hex digits
    # How many bytes is that?
    #
    # Also guarantees that that the checksum will
    # always be less than the modulus.
    return total


def get_hex_digits():
    """
    Determines the number of bits needed to represent n
      then returns this in hexadecimal digit count
    """
    # 4 bits per nibble (hex digit)
    bits_per_nibble = 4

    # Number of bits to represent n is 2 * the max prime
    bit_length = MAX_PRIME.bit_length() * 2

    # Length of n in hexadecimal digits
    return (bit_length + (bits_per_nibble - 1)) // bits_per_nibble


def format_as_hex(value):
    """
    Convert integer to a zero-padded hex string with the required number
    of characters to represent n, d, or and encrypted message.

    :param int value: to format
    :return: The formatted string
    """
    return "{:0{digits}x}".format(value, digits=str(get_hex_digits()))

# ---------------------------------------
# Do not modify code above this line
# ---------------------------------------


# ---------------------------------------
# Modify the functions below to create
#   apply, and break the RSA keys
# ---------------------------------------

def create_keys():
    """
    Create the public and private keys.

    :return: the keys as a three-tuple: (e,d,n)
    :author: Lucas
    """

    p = find_prime(MAX_PRIME, MIN_PRIME)
    q = find_prime(MAX_PRIME, MIN_PRIME)
    while p == q:
        q = find_prime(MAX_PRIME, MIN_PRIME)

    e = PUBLIC_EXPONENT

    n = p * q
    z = (p - 1) * (q - 1)

    d = factorize(e, z)

    return e, d, n


def apply_key(key, m):
    """
    Apply the key, given as a tuple (e,n) or (d,n) to the message.

    This can be used both for encryption and decryption.

    :param tuple key: (e,n) or (d,n)
    :param int m: the message as a number 1 < m < n (roughly)
    :return: the message with the key applied. For example,
             if given the public key and a message, encrypts the message
             and returns the ciphertext.
    :author: Jack
    """
    pass  # Delete this line and complete this method


def break_key(pub):
    """
    Break a key.  Given the public key, find the private key.
    Factorizes the modulus n to find the prime numbers p and q.

    :param pub: a tuple containing the public key (e,n)
    :return: a tuple containing the private key (d,n)
    """
    e, n = pub

    i = 0
    p = next_prime(MIN_PRIME, i)
    q = int(n / p)
    while not prime(q) or (q - 1) % e == 0:
        i += 1
        p = next_prime(MIN_PRIME, i)
        q = int(n / p)
        

    z = (p - 1) * (q - 1)
    d = factorize(e, z)

    return d, n


# Add additional functions here, if needed.


def prime(n : int) -> bool:
    """
    Determines if n is prime

    :param n: a number to test if prime
    :return: boolean representing if n is prime
    :author: Lucas
    """
    if n > 1:
        for i in range(2, int(n / 2) + 1):
            if (n % i) == 0:
                return False
    else:
        return False

    return True


def next_prime(min: int, n : int):
    """
    Finds the next prime within the min value.

    :param min: an int that is the min value we test for to find the next prime
    :param n: asks for the nth prime in the sequence of primes from the min
    :return: a prime int
    :author: Jack
    """
    pass


def find_prime(max: int, min: int) -> int:
    """
    Finds a prime with the max being the max value to test for.

    :param max: an int that is the max value that we can test up to for finding a prime
    :return: a prime int
    :author: Jack
    """
    pass


def factorize(a, n):
    """
    Factorizes the expression (a * t) mod n == 1 to find t.

    :return: t or -1 if a is not invertible
    :author: Lucas
    """
    t = 0
    r = n

    new_t = 1
    new_r = a
    while new_r != 0:
        quotient = int(r / new_r)
        t, new_t = (new_t, t - quotient * new_t)
        r, new_r = (new_r, r - quotient * new_r)

    if r > 1:
        return -1
    if t < 0:
        t += n

    return t


main()
