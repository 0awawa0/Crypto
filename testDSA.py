from Asymmetric import DSA
from datetime import datetime
import hashlib
from Math import primality


def testProbablePrimeGeneration():
    t = []
    for _ in range(10):
        start = datetime.now()
        N, L = DSA.APPROVED_LENGTHS[0]
        params = DSA.generateProbablePrimes(N, L, N, hashlib.sha256)
        end = datetime.now()
        t.append((end - start).seconds)

        p = params.primes.p
        q = params.primes.q
        assert primality.millerRabin(p, 10)
        assert primality.millerRabin(q, 10)
        assert (p - 1) % q == 0
    
    avg = sum(t) / len(t)
    print(f"Avg time: {avg} seconds")

def testProbablePrimeVerification():
    for i in range(25):
        N, L = DSA.APPROVED_LENGTHS[0]
        params = DSA.generateProbablePrimes(N, L, N)
        assert DSA.verifyProbablePrimesGenerationResult(params)

def testProvablePrimeGeneration():
    t = []
    for _ in range(10):
        start = datetime.now()
        N, L = DSA.APPROVED_LENGTHS[0]
        firstSeed = DSA.getFirstSeed(N, N)
        params = DSA.generateProvablePrimes(N, L, firstSeed)
        end = datetime.now()
        t.append((end - start).seconds)
    
    avg = sum(t) / len(t)
    print(f"Avg time: {avg} seconds")


def testUnverifiableG():
    N, L = DSA.APPROVED_LENGTHS[0]
    firstSeed = DSA.getFirstSeed(N, L)
    primes = DSA.generateProvablePrimes(N, L, firstSeed).primes
    g = DSA.generateUnverifiableG(primes)
    print(g)


def testProvablePrimeVerification():
    for _ in range(25):
        N, L = DSA.APPROVED_LENGTHS[0]
        firstSeed = DSA.getFirstSeed(N, N)
        params = DSA.generateProvablePrimes(N, L, firstSeed)
        assert DSA.verifyProvablePrimesGenerationResult(params)


def testVerifiableG():

    for i in range(100):
        N, L = DSA.APPROVED_LENGTHS[0]
        firstSeed = DSA.getFirstSeed(N, L)
        result = DSA.generateProvablePrimes(N, L, firstSeed)
        while result.status == False:
            firstSeed = DSA.getFirstSeed(N, L)
            result = DSA.generateProvablePrimes(N, L, firstSeed)
        g = DSA.generateVerifiableG(result, 1)
        assert DSA.verifyRootGeneration(g)

        result = DSA.generateProbablePrimes(N, L, N)
        g = DSA.generateVerifiableG(result, 1)
        assert DSA.verifyRootGeneration(g)
        print(i + 1)


def testRandomParamsVerification():
    
    N, L = DSA.APPROVED_LENGTHS[0]
    for i in range(10):
        params = DSA.generateParams(N, L, False, False)
        assert DSA.partiallyVerifyRootGeneration(params)
    
    for i in range(10):
        params = DSA.generateParams(N, L, False, True)
        assert DSA.partiallyVerifyRootGeneration(params)
    
    for i in range(10):
        params = DSA.generateParams(N, L, True, False)
        assert DSA.partiallyVerifyRootGeneration(params)
    
    for i in range(10):
        params = DSA.generateParams(N, L, True, True)
        assert DSA.partiallyVerifyRootGeneration(params)


if __name__ == "__main__":
    # testProbablePrimeGeneration()
    # testProvablePrimeGeneration()
    # testProbablePrimeVerification()
    # testProvablePrimeVerification()
    # testUnverifiableG()
    # testVerifiableG()
    testRandomParamsVerification()
