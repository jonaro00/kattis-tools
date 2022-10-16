from collections import Counter,defaultdict,deque
from base64 import b64decode, b64encode
from bisect import bisect_left,bisect_right
from datetime import date, datetime, timedelta
from functools import lru_cache,reduce#,cache # py3.9
from itertools import accumulate,chain,combinations_with_replacement,combinations,compress,count,cycle,dropwhile,filterfalse,groupby,islice,permutations,product,repeat,starmap,takewhile,tee,zip_longest
from math import sin,cos,tan,comb,ceil,factorial,gcd,floor,isqrt,sqrt,log,log10,log2,pi,perm,pow,hypot,inf,prod,remainder#,lcm # py3.9
import operator
from re import findall,finditer,match,search,split,sub
from string import ascii_letters,ascii_lowercase,ascii_uppercase,digits
from sys import stdin,stderr,stdout

# ITERTOOLS RECIPIES
def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))
def tail(n, iterable):
    "Return an iterator over the last n items"
    # tail(3, 'ABCDEFG') --> E F G
    return iter(deque(iterable, maxlen=n))
def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)
def all_equal(iterable):
    "Returns True if all the elements are equal to each other"
    g = groupby(iterable)
    return next(g, True) and not next(g, False)
def quantify(iterable, pred=bool):
    "Count how many times the predicate is true"
    return sum(map(pred, iterable))
def ncycles(iterable, n):
    "Returns the sequence elements n times"
    return chain.from_iterable(repeat(tuple(iterable), n))
def flatten(list_of_lists):
    "Flatten one level of nesting"
    return chain.from_iterable(list_of_lists)
def grouper(iterable, n, *, incomplete='fill', fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == 'fill':
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == 'strict':
        return zip(*args, strict=True)
    if incomplete == 'ignore':
        return zip(*args)
    else:
        raise ValueError('Expected fill, strict, or ignore')
def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)
def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))
def partition(pred, iterable):
    "Use a predicate to partition entries into false entries and true entries"
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)
def subslices(seq):
    "Return all contiguous non-empty subslices of a sequence"
    # subslices('ABCD') --> A AB ABC ABCD B BC BCD C CD D
    slices = starmap(slice, combinations(range(len(seq) + 1), 2))
    return map(operator.getitem, repeat(seq), slices)
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element
def unique_justseen(iterable, key=None):
    "List unique elements, preserving order. Remember only the element just seen."
    # unique_justseen('AAAABBBCCDAABBB') --> A B C D A B
    # unique_justseen('ABBCcAD', str.lower) --> A B C A D
    return map(next, map(operator.itemgetter(1), groupby(iterable, key)))
def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.
    If no true value is found, returns *default*
    If *pred* is not None, returns the first item
    for which pred(item) is true.
    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)

#######

# from itertools import pairwise # py3.10
def pairwise(iterable):
    return sliding_window(iterable, 2)

#######

# math hacks

def multiply(*x):
    return reduce(operator.mul, x)

primes = [2, 3, 5] # can add more from primes.txt
def prime_factors(n):
    # 12 -> 2 2 3
    while n > 1:
        for i in chain(primes, range(primes[-1]+1, isqrt(n)+1, 2)):
            if n % i == 0:
                yield i
                n //= i
                break
        else:
            yield n
            return

def divisors(n):
    # 12 -> 1 2 3 4 6 12
    c = Counter(prime_factors(n)).items()
    l = (tuple(b**i for i in range(p+1)) for b, p in c)
    return sorted(starmap(multiply, product(*l)))

#######

# Kattis stuff

def printe(*args, **kwargs):
    # Print to stderr (ignored by Kattis)
    print(*args, **kwargs, file=stderr)

def ii():
    return int(input())

def iis():
    # Input:
    #  1 2
    # Use:
    #  a, b = iis()
    yield from map(int, input().split())

def n_lines_split():
    # Input:
    #  2
    #  a b
    #  c d
    # Yields:
    #  ('a', 'b')
    #  ('c', 'd')
    yield from (input().split() for _ in range(ii()))

#######################################



