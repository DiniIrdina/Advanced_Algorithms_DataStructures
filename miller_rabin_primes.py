# Dini Irdina Ahmad Ubaidah, 31279279
# Credits and References: Tutorial videos, lecture videos and slides, sanity check session, YouTube (JacksonInfoSec)

import math
import random
import sys

def mod_exp(a,n,b):
    """Function for fast modular exponentiation. Retrieved from a YouTube video: https://www.youtube.com/watch?v=3Bh7ztqBpmw&t=81s """
    x = 1
    while n > 0:
        if n & 1 == 1:
            x = (x*a) % b
        a = (a * a) % b
        n >>= 1
    return x

def miller_rabin(n,k):
    """Miller Rabin function that accepts a number and k as input. Determines if the number is a prime or composite (probability of failing is 1/k).
       The function was coded according to the lecture slides."""
    if n & 1 == 0:
        return False   # False means its composite
    if n == 2 or n == 3:
        return True

    s, t = 0, n - 1
    while t & 1 == 0:
        s += 1
        t >>= 1

    for _ in range(k):
        a = random.randrange(2,n-1)

        if mod_exp(a,n-1,n) != 1:
            return False

        previous = mod_exp(a,(2**0)*t,n)
        for i in range(1,s):
            current = mod_exp(previous,2,n)
            if current == 1 and (previous != 1 and previous != n-1):
                return False
            previous = current

    return True

def three_primes(n):
    """Function that generates a set of three odd prime numbers that add up to the input N."""
    remainder = n
    saved_numbers = []
    counter = n - 2
    while counter > 2 and len(saved_numbers) < 3:

        if miller_rabin(counter, round(math.log2(counter))):
            test_remainder = remainder - counter
            if len(saved_numbers) == 0 and test_remainder  <5:  
                counter -= 2
                continue

            elif len(saved_numbers) == 1 and test_remainder  < 3:
                counter -= 2
                continue

            elif counter > remainder:
                counter -= 2
                continue

            else:
                saved_numbers.append(counter)
                remainder -= counter
                if remainder % 2 == 0:
                    counter = remainder - 1
                else:
                    counter = remainder

        else:
            counter -= 2

    saved_numbers.sort()
    return saved_numbers

def write_result(result):
    file = open("output_threeprimes.txt", "w")
    for i in range(len(result)):
        file.write(str(result[i]) + " ")
    file.close()

if __name__ == "__main__":
    input_specs = sys.argv[1]
    output = three_primes(int(input_specs))
    write_result(output)