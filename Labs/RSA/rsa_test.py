# Use these named constants as you write your code
# To increase the key size add more 1's and 0's to these values
#   E.g. MAX_PRIME = 0b1111111111111111 <- 16 bits
#        MIN_PRIME = 0b1100000000000001 <- 16 bits


import math
import random


MAX_PRIME = 0b11111111  # The maximum value a prime number can have
MIN_PRIME = 0b11000001  # The minimum value a prime number can have 
PUBLIC_EXPONENT = 17  # The default public exponent

def main():
    e, d, n = create_keys()
    pub = (e, n)

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

    p = find_prime(MAX_PRIME, MIN_PRIME)
    q = find_prime(MAX_PRIME, MIN_PRIME)
    while p == q:
        q = find_prime(MAX_PRIME, MIN_PRIME)

    e = PUBLIC_EXPONENT

    n = p * q
    z = (p - 1) * (q - 1)

    d = factorize(e, z)

    return e, d, n


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
    print(f"Trying [p : {p}] and [q : {q}]")
    while not prime(q) or (q - 1) % e == 0:
        i += 1
        p = next_prime(MIN_PRIME, i)
        q = int(n / p)
        print(f"Trying [p : {p}] and [q : {q}]")
        

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
    primes = [193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251]
    if n == -1:
        return primes[random.randrange(0, len(primes))]
    else:
        return primes[n]


def find_prime(max: int, min: int) -> int:
    """
    Finds a prime with the max being the max value to test for.

    :param max: an int that is the max value that we can test up to for finding a prime
    :return: a prime int
    :author: Jack
    """
    return next_prime(min, -1)


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
