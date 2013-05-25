import re, pyrex

from timeit import timeit

r1 = re.compile('a*b')
r2 = pyrex.rex('a*b')

def time(r, i):
    return timeit(lambda: r.match('a'*i), number=1)*1e6

for i in range(1, 10000):
    print('{}\t{:8.0f}\t{:8.0f}'.format(
        i, time(r1, i), time(r2, i)))
