import math, random

####################################################
#=======    Generating two 16-bit primes   ========#
####################################################

# Pre-generated list of primes
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
          71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139,
          149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
          227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,
          307, 311, 313, 317, 331, 337, 347, 349]

# Random nBit Number Generator Caller
def rng(n):
    while True:
        prime_candidate = getLowLevelPrimeNumber(n)
        if not millerRabinFilter(prime_candidate):
            continue
        else:
            print(f'Your {n}-bit prime integer is {prime_candidate}')
            return prime_candidate

# Random nBit Number Generator
def nBitRandomGenerator(n):
    return random.randrange(2**(n-1)+1, 2**n - 1)

# Phase 1 - Initial filtering of potential non-primes
def getLowLevelPrimeNumber(n):
    while True:
        prime_candidate = nBitRandomGenerator(n)

        for x in primes:
            if prime_candidate % x == 0 and x**2 <= prime_candidate:
                break
        else:
            return prime_candidate

# Phase 2 - Final filtering of potential non-primes
def millerRabinFilter(candidate):
    maxDivisionsByTwoCounter = 0
    ec = candidate-1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwoCounter += 1
    assert(2**maxDivisionsByTwoCounter * ec == candidate-1)

    def trials(round_tester):
        if pow(round_tester, ec, candidate) == 1:
            return False

        for i in range(maxDivisionsByTwoCounter):
            if pow(round_tester, 2**i * ec, candidate) == candidate-1:
                return False
        return True

    # Set number of trials here
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, candidate)
        if trials(round_tester):
            return False
    return True

########## Generating Parameters #################

def gcd(a, b):

    r = [a, b]
    q = []

    s = [1, 0]
    t = [0, 1]

    while r[-1] != 0:
        if len(q) > 0:
            s.append(s[-2] - q[-1] * s[-1])
            t.append(t[-2] - q[-1] * t[-1])

        q.append(r[-2] // r[-1])
        r.append(r[-2] % r[-1])

    return (
        a * s[-1] + b * t[-1],
        s[-1],
        t[-1],
    )

def square_and_multiply(x, n, c):
    result = x
    binary_power = iter('{0:b}'.format(c))
    next(binary_power)
    for i in binary_power:
        result **= 2
        if (i == '1'):
            result *= x
        result %= n
    return result

def nBitChunks(message, nBits):
	n = nBits
	chunks = [message[i:i+n] for i in range(0, len(message), n)]
	return chunks

def encrypt(message, n, e):
	encrypted_chunks = []
	chunky_message = nBitChunks(message, 3)
	chunky_message = [message.encode('utf-8') for message in chunky_message]
	chunky_message = [message.hex() for message in chunky_message]
	chunky_message = [int(message, 16) for message in chunky_message]
	for message_chunk in chunky_message:
		message_chunk = square_and_multiply(message_chunk, n, e)
		encrypted_chunks.append(message_chunk)
	return encrypted_chunks
	 
def decrypt(message, n, d):
	decrypted_chunks = []
	for message_chunk in message:
		message_chunk = square_and_multiply(message_chunk, n, d)
		decrypted_chunks.append(message_chunk)
	decrypted_chunks = [hex(message) for message in decrypted_chunks]
	decrypted_chunks = [message[2:] for message in decrypted_chunks]
	decrypted_chunks = [bytearray.fromhex(message).decode() for message in decrypted_chunks]
	decrypted_message = "".join(decrypted_chunks)
	return decrypted_message
	
if __name__ == '__main__':
    p = rng(16)
    q = rng(16)
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randint(2, 2 ** 16)
        g, _, _ = gcd(e, phi)

        if g == 1:
            break

    _, d, _ = gcd(e, phi)

    if d < 0:
        d += phi