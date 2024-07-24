import secrets


def fisher_yates(population, k):
    result = [None] * k  # An n-length list is smaller than a k-length set.
    pool = list(population)
    for i in range(k):
        j = secrets.randbelow(k - i)  # for selecting a random element in the list
        result[i] = pool[j]  # i'th index of result = compass[random]
        pool[j] = pool[k - i - 1]  # compass[random] = compass[length - index - 1] - s
    return result


# Fisher Yates shuffles

"""
An issue that can be found within shuffling algorithms is when a sample space gets too large. A sets permutations can be 
represented by S!. The number of bits required for a shuffle of large magnitudes(ex: 52!) is log2(52!)
"""


def _random_sample(population, k):
    print(" ")
