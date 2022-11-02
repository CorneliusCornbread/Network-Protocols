# Use these named constants as you write your code
# To increase the key size add more 1's and 0's to these values
#   E.g. MAX_PRIME = 0b1111111111111111 <- 16 bits
#        MIN_PRIME = 0b1100000000000001 <- 16 bits


import math


MAX_PRIME = 0b11111111  # The maximum value a prime number can have
MIN_PRIME = 0b11000001  # The minimum value a prime number can have 
PUBLIC_EXPONENT = 17  # The default public exponent

def main():
    e, d, n = create_keys()
    pub = (e, n)
    pri = (d, n)

    if e == PUBLIC_EXPONENT and n == 37249:
        print("Test Passed [create_keys()]")
    else:
        print("Test Failed [create_keys()]")

    brk_d, brk_n = break_key(pub)
    if brk_d == d and brk_n == n:
        print("Test Passed [break_key()]")
    else:
        print("Test Failed [break_key()]")


def create_keys():
    """
    Create the public and private keys.

    :return: the keys as a three-tuple: (e,d,n)
    :author: Lucas
    """

    p, q = (find_prime(MAX_PRIME, MIN_PRIME), find_prime(MAX_PRIME, MIN_PRIME))
    e = PUBLIC_EXPONENT

    n = p * q # 37249
    z = (p - 1) * (q - 1) # 36864

    d = factorize(e, z)

    print(f"d : {d}")
    print(f"(d * e) % z : {(d * e) % z}")

    return e, d, n


def break_key(pub):
    """
    Break a key.  Given the public key, find the private key.
    Factorizes the modulus n to find the prime numbers p and q.

    :param pub: a tuple containing the public key (e,n)
    :return: a tuple containing the private key (d,n)
    """
    e, n = pub

    d = None

    return d, n

# Add additional functions here, if needed.


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
    return 193


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
