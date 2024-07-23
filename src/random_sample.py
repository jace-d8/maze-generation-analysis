import secrets


def my_rand_sample(population, k):
    result = [None] * k  # An n-length list is smaller than a k-length set.
    pool = list(population)
    for i in range(k):
        j = secrets.randbelow(k - i)  # for selecting a random element in the list
        result[i] = pool[j]  # i'th index of result = compass[random]
        pool[j] = pool[k - i - 1]  # compass[random] = compass[length - index - 1] - s
    return result
# Fisher Yates shuffle
