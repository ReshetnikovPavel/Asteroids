import random


def make_rand_vector():
    vec = [random.gauss(0, 1) for i in range(2)]
    mag = sum(x ** 2 for x in vec) ** .5
    return [x / mag for x in vec]
